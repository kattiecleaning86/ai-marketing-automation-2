---
description: Record approval decisions for a client's calendar — /approve client-slug YYYY-MM: approve P01-P05, change P06 ...
argument-hint: "<client-slug> <YYYY-MM>: <decisions>"
---

Apply these approval decisions to the client's calendar JSON, following the "Approval follow-ups" section of `.claude/skills/organic-marketing-engine/SKILL.md`:

$ARGUMENTS

Set `approved_by` to my name if I gave it, otherwise "Operator". Rewrite posts that need changes and keep them "Pending Review". Re-run `tools/build_exports.py` and `tools/qa_check.py`, commit and push, and summarise what changed. Never publish anything.
