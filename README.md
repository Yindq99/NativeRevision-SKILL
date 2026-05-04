# NativeRevision-Skill

> **Make agent edits read like native documentation, not prompt-shaped patches.**

An AI skill for Codex, Claude Code, OpenClaw, and other `SKILL.md`-compatible agents. Native Revision helps agents update prompts, specs, configs, schemas, README files, and agent instructions while preserving contracts and removing instruction residue.

## Introduction

Agentic editing often succeeds at the headline request while leaving visible modification traces:

- Negative contrast used as a role definition.
- Migration-note phrasing in stable documentation.
- Local prohibitions that simply restate the user's edit instruction.
- Output fields renamed without a downstream migration.
- Existing workflows compressed into vague summaries.

For example: (See [examples](references/examples.md) for more details)
- "You are not X, but Y."
- "This is now handled by Z."
- "Do not define A; call B instead."

These edits expose the user's instruction and can damage prompts, schemas, and documents-as-programs. Native Revision gives the agent a repeatable workflow for converting edit instructions into artifact-native patches.

## Table of Contents

- [Native Revision Skill](#native-revision-skill)
  - [Installation](#installation)
  - [What It Covers](#what-it-covers)
  - [Deep Coverage Includes](#deep-coverage-includes)
  - [Quick Start](#quick-start)
  - [Local Lint](#local-lint)
  - [Repository Layout](#repository-layout)
  - [Contribution](#contribution)

## Installation

Clone or copy this repository, then place the skill folder where your agent loads skills. The installed folder should contain `SKILL.md`, `README.md`, `references/`, and `scripts/`.

- <details><summary>Claude Code</summary>

  Personal skill:

  ```bash
  mkdir -p ~/.claude/skills
  cp -R /path/to/NativeRevision-SKILL ~/.claude/skills/native-revision
  ```

  Project skill:

  ```bash
  mkdir -p .claude/skills
  cp -R /path/to/NativeRevision-SKILL .claude/skills/native-revision
  ```

  Claude Code skills are folders containing `SKILL.md`; the directory name becomes the slash command.

</details>

- <details><summary>Codex</summary>

  Personal skill:

  ```bash
  mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
  cp -R /path/to/NativeRevision-SKILL "${CODEX_HOME:-$HOME/.codex}/skills/native-revision"
  ```

  Project skill:

  ```bash
  mkdir -p .agents/skills
  cp -R /path/to/NativeRevision-SKILL .agents/skills/native-revision
  ```

</details>

- <details><summary>OpenClaw</summary>

  Shared skill:

  ```bash
  mkdir -p ~/.openclaw/skills
  cp -R /path/to/NativeRevision-SKILL ~/.openclaw/skills/native-revision
  ```

  Workspace skill:

  ```bash
  mkdir -p skills
  cp -R /path/to/NativeRevision-SKILL skills/native-revision
  openclaw skills list
  ```

  OpenClaw also supports `<workspace>/.agents/skills`, `~/.agents/skills`, and configured extra skill folders.

</details>

- <details><summary>Other Agents</summary>

  Any AgentSkills-compatible tool can use this package if it supports a directory containing `SKILL.md` with YAML frontmatter.

  If your agent has no skill loader, paste `SKILL.md` into the agent's project instructions and keep `references/` nearby for manual lookup.

</details>

## What It Covers

| Area | Coverage |
| --- | --- |
| Instruction residue | Avoids visible paraphrases of user edit prompts |
| Patch-like language | Replaces negative contrast and migration-note wording with stable current-state language |
| Contract preservation | Protects JSON keys, tool names, schema fields, headings, examples, and output formats |
| Scope control | Prevents local architecture edits from becoming full-file rewrites |
| Prompt/spec behavior | Keeps operational details that downstream agents still need |
| Reviewability | Produces localized, explainable diffs |

## Quick Start

Ask your agent to use the skill when revising an existing artifact:

```markdown
Use $native-revision to update this API gateway spec so Auth Service owns token validation.
Preserve the gateway's routing responsibilities and the existing JSON response contract.
Avoid instruction-residual wording.
```

The agent should now:

- Extract the edit intent before changing text.
- Identify protected contracts and editable regions.
- Patch only the relevant sections.
- Write in stable current-state language.
- Verify contract preservation before finalizing.

## Local Lint

Run the helper script to flag likely residue and contract drift:

```bash
python3 scripts/native_revision_lint.py original.md revised.md --instruction instruction.txt
```

Machine-readable output:

```bash
python3 scripts/native_revision_lint.py original.md revised.md --instruction instruction.txt --json
```

The script checks common residue markers, high overlap with the edit instruction, removed Markdown headings, removed JSON keys, and removed tool names. Treat findings as review prompts, not automatic failures.

By default, fenced code blocks are ignored so teaching examples do not count as findings. Add `--include-code-blocks` when the revised artifact itself stores executable prompt text or output text inside code fences.

## Repository Layout

```text
NativeRevision-SKILL/
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
