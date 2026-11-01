# Security

Exitly is designed to hold sensitive admin access, so it follows these principles:

- Least-privilege OAuth scopes
- Secrets in environment variables or a secrets manager, never in git
- Admin approval before destructive actions
- Append-only, hash-chained audit log

**Status:** the code in this repository is a hackathon demo using sample data and simulated revocations. Do not connect real production credentials to it.

## Reporting a vulnerability

Please open a private security advisory on GitHub (Security tab) or email `[add contact email]`. Do not post exploit details in public issues.
