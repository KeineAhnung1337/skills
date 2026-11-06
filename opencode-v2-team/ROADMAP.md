# Follow-up coding workflow ideas

Deferred while the current setup is published to the repository. These ideas are recorded for later; they are not implemented.

1. Add `/bootstrap` to inspect a target repository's manifests, CI, tests, and examples, then prepare accurate project instructions.
2. Add `/fix`, `/feature`, `/review`, and `/verify` commands that route work through the appropriate specialists and require observable verification.
3. Create a project-specific verification script shared by the agents and CI, covering relevant formatting, lint, type, and test checks.
4. Add small skills for the actual technology stack, with proven examples and verification steps. Explicitly allow approved skills in specialist permissions.
5. Exercise the running application for changes across module boundaries, including relevant UI, API, database, or background-job behavior.
6. Automate task reports for changed files, check results, unresolved findings, total tokens, retries, and elapsed time.

Suggested next increment: repository bootstrap, the four workflow commands, and a verified project check entry point.
