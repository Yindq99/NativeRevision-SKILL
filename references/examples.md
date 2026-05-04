# Native Revision Examples

## Example 1: Service Responsibility Transfer

User instruction:

```text
Move token validation to the Auth Service. The API gateway should call Auth Service instead of describing token validation rules locally.
```

Residual revision:

```md
The API gateway is not responsible for token validation. Do not define token validation rules here. Auth Service is now responsible for signature checks, expiration checks, issuer validation, and key rotation.
```

Why it is weak:

- It exposes the edit instruction.
- It describes a migration instead of the stable current interface.
- It overuses negative role definition.

Native revision:

```md
For authenticated routes, the API gateway submits token metadata to Auth Service and uses the returned validation result, subject identity, scopes, and retryable error status when routing the request.
```

Why it is better:

- It defines the current operational interface directly.
- It preserves the gateway's routing responsibility.
- It avoids restating internal validation rules that belong to another service.

## Example 2: Output Contract Preservation

User instruction:

```text
Have billing exports use the Invoice Service for invoice IDs, but keep the existing export JSON shape.
```

Residual revision:

```md
The billing exporter no longer manages invoice IDs. Invoice Service is now responsible for all invoice identifiers and invoice validation.
```

Possible contract drift:

```json
{
  "invoice_service_status": {},
  "invoice_records": []
}
```

Native revision:

```md
Populate the existing `invoice_id`, `invoice_status`, and `invoice_errors` fields from Invoice Service responses. Preserve the export JSON keys unless a separate schema migration is provided.
```

## Example 3: Safety Rule Insertion

User instruction:

```text
Add a rule that the agent must not run destructive git commands.
```

Residual revision:

```md
Do not run destructive git commands because the user does not want data loss.
```

Native revision:

```md
Before running git commands, classify whether the command can discard local work. Commands such as `git reset --hard`, `git clean`, or forced checkout require explicit user approval with the exact command and affected paths.
```

## Example 4: Terminology Migration

User instruction:

```text
Rename Job to Task in the CLI documentation, but keep command flags compatible.
```

Residual revision:

```md
Job is no longer used; Task is the new term.
```

Native revision:

```md
Use Task as the user-facing term in prose. Preserve existing CLI flags such as `--job-id` unless a compatibility migration is explicitly requested.
```
