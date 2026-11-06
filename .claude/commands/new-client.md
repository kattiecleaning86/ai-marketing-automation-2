---
description: Run the full organic social workflow for a client — /new-client Client Name | website | YYYY-MM
argument-hint: "<Client name> | <website> | <YYYY-MM>"
---

Run the complete `organic-marketing-engine` skill (all 12 stages, from brief to approval package) for:

$ARGUMENTS

Follow `.claude/skills/organic-marketing-engine/SKILL.md` and `CLAUDE.md` exactly. Work autonomously: ask me only for business decisions or client facts you cannot find publicly. Never publish anything. Save every deliverable in `clients/<client-slug>/`, run the QA and export tools, commit and push, then tell me in plain language what is ready for my approval.

If no arguments were given, ask me for the client name, website and target month (default: next month), or offer to create a blank brief with `python tools/new_client.py`.
