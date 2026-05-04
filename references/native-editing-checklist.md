# Native Editing Checklist

Use this checklist when reviewing an edit to an existing prompt, spec, README, config, schema, or agent skill.

## 1. Intent Abstraction

- Required change is written in your own words before editing.
- Removed responsibility is separated from preserved responsibility.
- Editable sections are identified.
- Protected sections are identified.
- Downstream contracts are listed.

## 2. Instruction Residue

Flag a changed sentence when it:

- Closely paraphrases the user's instruction.
- Uses negative contrast as the main role definition.
- Uses handoff or history markers in a stable spec.
- Explicitly names the edit request as the reason for new text.
- Explains why the edit happened instead of what the artifact currently requires.
- Repeats the same boundary as several prohibitions.

## 3. Native Integration

Check that inserted text:

- Uses the same level of detail as neighboring text.
- Fits the same section purpose.
- Uses stable present-tense language.
- Keeps the artifact's original role and workflow vocabulary.
- Avoids making a prompt sound like a changelog or review response.

## 4. Contract Preservation

Compare original and revised versions for unauthorized changes to:

- JSON keys.
- YAML/TOML/config keys.
- Tool names and function names.
- API paths.
- CLI commands.
- Event names.
- Prompt output formats.
- Required failure fields.
- Markdown heading hierarchy.
- Code examples and schemas.

## 5. Scope Control

Accept broad edits only when required by the instruction. Otherwise prefer localized patches.

Flag:

- Full-file style normalization.
- Section reorderings unrelated to the request.
- Deletion of concrete requirements outside the target region.
- Compression of structured outputs into vague summaries.
- Renaming just to match the new wording.

## 6. Final Gate

The edit is ready when:

- The user's intent is satisfied.
- The target artifact reads as a stable current-state document.
- Reviewers cannot easily infer the exact edit prompt from the inserted language.
- Protected contracts remain stable or are explicitly migrated.
- The diff is explainable in one or two sentences.
