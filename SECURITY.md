# Security Policy

## Supported versions

The latest release on the `main` branch is supported. Older releases are not actively patched.

## Reporting a vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities. Instead, report them
privately via [GitHub's security advisory form](https://github.com/ScalefreeCOM/datavault4dbt-agent-skills/security/advisories/new).

Include:
- A description of the vulnerability and its potential impact.
- Steps to reproduce (a minimal example is ideal).
- The affected skill(s) and version.

We aim to acknowledge reports within 5 business days and publish a fix or advisory within 30 days of
confirmation.

## Scope

This repository contains Markdown skill files (no executable code distributed to end-users beyond the
`scripts/validate_skills.py` development tool). The main risk surface is **indirect prompt injection**
— skill instructions that could be influenced by malicious content in client project files the agent
reads. We treat this as in-scope.

Out of scope: vulnerabilities in dbt, datavault4dbt, or the underlying AI agent platform (report those
to the respective projects).
