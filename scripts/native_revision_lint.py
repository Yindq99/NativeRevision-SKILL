#!/usr/bin/env python3
"""Lightweight review aid for native artifact revisions.

This script flags common instruction-residue and contract-drift signals.
It is intentionally conservative: treat findings as prompts for review, not
as definitive failures.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path
from typing import Iterable


RESIDUE_PATTERNS = [
    (r"\bnot\b.{0,80}\bbut\b", "negative contrast: not X but Y"),
    (r"\byou are not\b", "negative role definition"),
    (r"\bno longer\b", "migration marker: no longer"),
    (r"\bnow (handled|owned|managed|responsible)\b", "migration marker: now handled"),
    (r"\bas requested\b", "edit-source marker: as requested"),
    (r"\bper (the )?(user'?s )?instruction\b", "edit-source marker: per instruction"),
    (r"\bpreviously\b", "history marker: previously"),
    (r"\bold (architecture|behavior|version|system)\b", "history marker: old"),
    (r"\bnew (architecture|behavior|version|system)\b", "history marker: new"),
    (r"不是.{0,40}而是", "negative contrast: 不是 X 而是 Y"),
    (r"你不是", "negative role definition: 你不是"),
    (r"不再由", "migration marker: 不再由"),
    (r"现在由", "migration marker: 现在由"),
    (r"按(照)?(你的|用户的)?(要求|指令)", "edit-source marker: 按要求/指令"),
    (r"根据(你的|用户的)?(要求|指令)", "edit-source marker: 根据要求/指令"),
]

TOOL_PATTERN = re.compile(r"\b[a-zA-Z][\w-]*---[a-zA-Z][\w-]*\b")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
JSON_KEY_PATTERN = re.compile(r'"([^"\n]{1,120})"\s*:')


def read_text(path: str | None) -> str:
    if not path:
        return ""
    return Path(path).read_text(encoding="utf-8")


def strip_fenced_code_blocks(text: str) -> str:
    lines = text.splitlines()
    stripped: list[str] = []
    in_fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            stripped.append("")
            continue
        stripped.append("" if in_fence else line)
    return "\n".join(stripped)


def changed_added_lines(original: str, revised: str, *, include_code_blocks: bool = False) -> list[str]:
    if not include_code_blocks:
        original = strip_fenced_code_blocks(original)
        revised = strip_fenced_code_blocks(revised)
    diff = difflib.ndiff(original.splitlines(), revised.splitlines())
    return [line[2:] for line in diff if line.startswith("+ ") and line[2:].strip()]


def extract_headings(text: str) -> list[str]:
    return [f"{level} {title.strip()}" for level, title in HEADING_PATTERN.findall(text)]


def extract_json_keys(text: str) -> set[str]:
    return set(JSON_KEY_PATTERN.findall(text))


def extract_tools(text: str) -> set[str]:
    return set(TOOL_PATTERN.findall(text))


def regex_findings(lines: Iterable[str]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for idx, line in enumerate(lines, start=1):
        for pattern, label in RESIDUE_PATTERNS:
            if re.search(pattern, line, flags=re.IGNORECASE):
                findings.append({"line": str(idx), "type": label, "text": line.strip()})
    return findings


def instruction_overlap_findings(instruction: str, lines: Iterable[str]) -> list[dict[str, str]]:
    if not instruction.strip():
        return []
    normalized_instruction = " ".join(instruction.split())
    findings = []
    for idx, line in enumerate(lines, start=1):
        candidate = " ".join(line.split())
        if len(candidate) < 30:
            continue
        ratio = difflib.SequenceMatcher(None, normalized_instruction, candidate).ratio()
        if ratio >= 0.58:
            findings.append(
                {
                    "line": str(idx),
                    "type": "high lexical overlap with instruction",
                    "score": f"{ratio:.2f}",
                    "text": candidate,
                }
            )
    return findings


def missing_items(name: str, before: set[str], after: set[str]) -> list[dict[str, str]]:
    return [{"type": f"missing {name}", "value": item} for item in sorted(before - after)]


def main() -> int:
    parser = argparse.ArgumentParser(description="Review a revision for instruction residue and contract drift.")
    parser.add_argument("original", help="Original artifact path")
    parser.add_argument("revised", help="Revised artifact path")
    parser.add_argument("--instruction", help="File containing the edit instruction", default=None)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--fail-on-findings", action="store_true", help="Exit 1 when findings are present")
    parser.add_argument("--include-code-blocks", action="store_true", help="Also scan fenced code blocks")
    args = parser.parse_args()

    original = read_text(args.original)
    revised = read_text(args.revised)
    instruction = read_text(args.instruction)
    added_lines = changed_added_lines(original, revised, include_code_blocks=args.include_code_blocks)

    original_headings = set(extract_headings(original))
    revised_headings = set(extract_headings(revised))
    original_keys = extract_json_keys(original)
    revised_keys = extract_json_keys(revised)
    original_tools = extract_tools(original)
    revised_tools = extract_tools(revised)

    findings = []
    findings.extend(regex_findings(added_lines))
    findings.extend(instruction_overlap_findings(instruction, added_lines))
    findings.extend(missing_items("heading", original_headings, revised_headings))
    findings.extend(missing_items("JSON key", original_keys, revised_keys))
    findings.extend(missing_items("tool name", original_tools, revised_tools))

    summary = {
        "original_lines": len(original.splitlines()),
        "revised_lines": len(revised.splitlines()),
        "added_nonblank_lines": len(added_lines),
        "removed_headings": sorted(original_headings - revised_headings),
        "removed_json_keys": sorted(original_keys - revised_keys),
        "removed_tool_names": sorted(original_tools - revised_tools),
        "include_code_blocks": args.include_code_blocks,
        "finding_count": len(findings),
        "findings": findings,
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print("Native Revision Lint")
        print("====================")
        print(f"Original lines: {summary['original_lines']}")
        print(f"Revised lines:  {summary['revised_lines']}")
        print(f"Added lines:    {summary['added_nonblank_lines']}")
        print(f"Findings:       {summary['finding_count']}")
        if findings:
            print()
            for finding in findings:
                if "text" in finding:
                    print(f"- {finding['type']}: {finding['text']}")
                else:
                    print(f"- {finding['type']}: {finding['value']}")

    return 1 if args.fail_on_findings and findings else 0


if __name__ == "__main__":
    sys.exit(main())
