# Native Revision Skill

> Make agent edits read like native documentation instead of prompt-shaped patches.

Native Revision is an AI agent skill for revising existing prompts, specs, configs, README files, schemas, and agent instructions without leaving instruction residue. It helps Codex, Claude Code, OpenClaw, and other `SKILL.md`-compatible agents preserve contracts while applying local changes.

## Introduction

Agentic editing often succeeds at the headline request while leaving visible modification traces:

- Negative contrast used as a role definition.
- Migration-note phrasing in stable documentation.
- Local prohibitions that simply restate the user's edit instruction.
- Output fields renamed without a downstream migration.
- Existing workflows compressed into vague summaries.

For example:
- "You are not X, but Y."
- "This is now handled by Z."
- "Do not define A; call B instead."

These edits expose the user's instruction and can damage prompts, schemas, and documents-as-programs. Native Revision gives the agent a repeatable workflow for converting edit instructions into artifact-native patches.

## Table of Contents

- [Installation](#installation)
- [What It Covers](#what-it-covers)
- [Quick Start](#quick-start)
- [Local Lint](#local-lint)
- [Repository Layout](#repository-layout)
- [Contribution](#contribution)

## Installation

Clone or copy this repository, then place the `native-revision` folder where your agent loads skills.

### Claude Code

Personal skill:

```bash
mkdir -p ~/.claude/skills
cp -R native_revision ~/.claude/skills/native-revision
```

Project skill:

```bash
mkdir -p .claude/skills
cp -R native_revision .claude/skills/native-revision
```

Claude Code skills are folders containing `SKILL.md`; the directory name becomes the slash command.

### Codex

Personal skill:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R native_revision "${CODEX_HOME:-$HOME/.codex}/skills/native-revision"
```

Project-local skill packs may also place the folder under a project skills directory if your Codex setup loads one.

### OpenClaw

Shared skill:

```bash
mkdir -p ~/.openclaw/skills
cp -R native_revision ~/.openclaw/skills/native-revision
```

Workspace skill:

```bash
mkdir -p skills
cp -R native_revision skills/native-revision
openclaw skills list
```

OpenClaw also supports `<workspace>/.agents/skills`, `~/.agents/skills`, and configured extra skill folders.

### Other Agents

Any AgentSkills-compatible tool can use this package if it supports a directory containing `SKILL.md` with YAML frontmatter. If the agent has no skill loader, paste `SKILL.md` into the agent's project instructions and keep `references/` nearby for manual lookup.

## What It Covers

| Area | Protection |
| --- | --- |
| Instruction residue | Avoids visible paraphrases of user edit prompts |
| Patch-like language | Replaces negative contrast and migration-note wording with stable current-state language |
| Contract preservation | Protects JSON keys, tool names, schema fields, headings, examples, and output formats |
| Scope control | Prevents local architecture edits from becoming full-file rewrites |
| Prompt/spec behavior | Keeps operational details that downstream agents still need |
| Reviewability | Produces localized, explainable diffs |

## Quick Start

Ask your agent:

```markdown
Use $native-revision to update this API gateway spec so Auth Service owns token validation. Preserve the gateway's routing responsibilities and the existing JSON response contract, and avoid instruction-residual wording.
```

The agent should:

- Extract the edit intent first.
- Identify protected contracts.
- Patch only relevant sections.
- Avoid migration-note language.
- Verify the result before finalizing.

## Local Lint

Run the helper script to flag likely residue and contract drift:

```bash
python3 native_revision/scripts/native_revision_lint.py original.md revised.md --instruction instruction.txt
```

Machine-readable output:

```bash
python3 native_revision/scripts/native_revision_lint.py original.md revised.md --instruction instruction.txt --json
```

The script checks common residue markers, high overlap with the edit instruction, removed Markdown headings, removed JSON keys, and removed tool names. Treat findings as review prompts, not automatic failures.

By default, fenced code blocks are ignored so teaching examples do not count as findings. Add `--include-code-blocks` when the revised artifact itself stores executable prompt text or output text inside code fences.

## Repository Layout

```text
native_revision/
├── SKILL.md
├── README.md
├── references/
│   ├── examples.md
│   └── native-editing-checklist.md
└── scripts/
    └── native_revision_lint.py
```

## Contribution

Useful improvements include:

1. More examples of instruction-residual edits.
2. Better residue patterns for Chinese, English, and mixed technical docs.
3. Contract extractors for specific schema formats.
4. Real before/after fixtures from prompts, skills, configs, and README files.

Review any third-party skill before installing it, especially if it includes executable scripts.
