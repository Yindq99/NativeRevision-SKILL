---
name: native-revision
description: This skill helps AI coding agents revise existing artifacts so edits read like native documentation and preserve contracts. Use this when modifying prompts, specs, configs, schemas, README files, or agent instructions, or when a user requests a scan or audit for instruction residue, patch-like wording, over-editing, style drift, or contract drift.
---

# Native Revision

Use this skill when editing an existing artifact where the revised file should read as if it was authored for the current design instead of as a visible response to the user's edit instruction.

The goal is not "smallest diff." The goal is a minimal sufficient edit that satisfies the instruction while preserving unrelated semantics, contracts, structure, and native style.

## Core Failure Mode

Detect and prevent instruction residue:

- The revised artifact paraphrases the user's instruction instead of absorbing it.
- New text uses patch-note language, handoff markers, or explicit edit-source markers.
- New text overuses negative contrast as the main role definition.
- New sections explain the historical migration instead of describing the current stable artifact.
- A local edit causes output schema, tool names, section hierarchy, or behavior contracts to drift.

## Workflow

1. Identify the artifact type: prompt, agent skill, workflow spec, API doc, schema, config, README, code comment, user-facing copy, or design doc.
2. Convert the user instruction into edit intent before editing:
   - Required change.
   - Responsibilities or behavior to remove.
   - Responsibilities or behavior to preserve.
   - Protected contracts: JSON keys, schema fields, tool names, command names, headings, examples, test behavior, output format.
   - Editable regions and protected regions.
3. Read the target artifact's local style:
   - Is it procedural, declarative, checklist-based, normative, explanatory, or tutorial-like?
   - Does it use positive role definitions or warning-heavy prohibitions?
   - What terms, heading depth, and output structures are stable?
4. Plan a patch:
   - Name the sections to edit.
   - Name the sections to keep intact.
   - Avoid full-file rewrite unless the instruction explicitly requires it.
5. Generate artifact-native text:
   - Describe the current stable interface, not the historical change.
   - Prefer positive operational language.
   - Use the artifact's existing vocabulary and granularity.
   - Preserve concrete extraction, validation, output, and failure-handling requirements.
6. Verify before finalizing:
   - Required intent is satisfied.
   - Protected contracts still match unless explicitly migrated.
   - No instruction residue remains.
   - Diff is reviewable and localized.
   - The artifact still performs its original non-target duties.

## Phrase Policy

Avoid these forms unless the original artifact already uses them for necessary policy language:

- Negative contrast as the main role definition.
- Direct role negation.
- Local prohibitions that restate an ownership transfer.
- Handoff markers that describe a migration instead of the current interface.
- Explicit edit-source markers.
- Historical labels for prior and revised architectures.
- Meta language about the edit itself.

Prefer stable current-state descriptions:

- "Submit extracted records through `<tool>` and use the returned status and IDs."
- "Route validation through `<component>` before returning the final payload."
- "Keep `<agent>` focused on search, reading, extraction, coverage analysis, and structured submission."
- "Use `<manager>` responses as the source of truth for object IDs, validation status, and retryable failures."

## Contract Preservation

Treat these as protected unless the user explicitly requests migration:

- JSON top-level keys and nested keys.
- Tool names, function names, CLI commands, endpoint paths, event names, and config keys.
- Required output sections and examples.
- Prompt roles, allowed actions, refusal/failure paths, and workflow stages.
- Markdown heading hierarchy and repeated templates.
- Record IDs, audit fields, validation fields, and schema-facing names.

When a contract must change, state that separately to the user and update downstream references or tests in the same task.

## Editing Patterns

### Responsibility Transfer

Use when an instruction moves ownership from one component or agent to another.

Do:

- Replace implementation ownership with a stable tool/interface call.
- Keep the original agent's inputs, outputs, and non-migrated responsibilities.
- Preserve the output schema and mark fields as populated from the new owner when possible.

Do not:

- Insert repeated negative ownership statements.
- Delete all concrete details about what information must be collected.
- Rename output fields just because ownership moved.

### Boundary Tightening

Use when an instruction narrows what the artifact should do.

Do:

- Add concise positive boundaries in the nearest relevant section.
- Preserve existing capabilities outside the narrowed region.

Do not:

- Turn the artifact into a warning list.
- Add broad prohibitions that suppress legitimate existing behavior.

### Style-Native Insertion

Use when adding a new rule or constraint to an existing document.

Do:

- Match the surrounding sentence shape and heading level.
- Insert one precise rule where it belongs.
- Preserve terminology already used nearby.

Do not:

- Add a meta explanation of why the rule was added.
- Use phrases that reveal the user's instruction.

## Review Checklist

Before final response, check:

- Does any changed sentence look like a paraphrase of the user instruction?
- Does any changed sentence explain a migration instead of describing the target state?
- Did any JSON key, tool name, heading, schema, or example change without an explicit request?
- Did the edit delete useful operational detail outside the target scope?
- Can a reviewer understand the diff without reading a full-file rewrite?
- If this is a prompt or skill, would the runtime agent still know exactly what to do?

For a fuller checklist, load `references/native-editing-checklist.md`.
For examples of bad and better revisions, load `references/examples.md`.

## Optional Local Lint

When file access is available, run the helper script after editing:

```bash
python3 ${CLAUDE_SKILL_DIR:-.}/scripts/native_revision_lint.py ORIGINAL REVISED --instruction INSTRUCTION.txt
```

For Codex or other agents without `${CLAUDE_SKILL_DIR}`, use the actual skill path:

```bash
python3 /path/to/native-revision/scripts/native_revision_lint.py ORIGINAL REVISED --instruction INSTRUCTION.txt
```

Use the lint output as a review aid, not as the only source of truth.
