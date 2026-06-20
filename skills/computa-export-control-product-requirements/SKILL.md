---
name: computa-export-control-product-requirements
description: Focused Computa Export Control product and requirements skill for turning vague or massive requests into researched user goals, workflows, acceptance criteria, non-goals, creative opportunities, edge cases, risks, and owner decisions before 4D Chess execution.
---

# Computa Export Control Product Requirements

Use this to clarify what should be built before deciding how to build it.

If invoked directly and `docs/computa-artifacts/activity-log.csv` exists or can be initialized, append `research_task_started` before requirements work and `research_task_completed`, `research_task_blocked`, or `research_task_deferred` after it, with `scope_name=product-requirements` and `artifact_path=requirements/`.

## Product Work

Analyze:

- user goals and likely end users
- core jobs-to-be-done and workflows
- current pain points and implied requirements
- constraints, non-goals, success metrics, rollout needs, and quality bar
- edge cases, permission states, error states, accessibility, privacy, analytics, security, and operational concerns
- creative opportunities that may improve the result beyond the literal request

Use web/product research when current market, UX conventions, compliance, or competitive behavior matters.

## Outputs

Write under `requirements/`:

- `requirements-brief.md`: goals, users, workflows, constraints, non-goals, success criteria.
- `acceptance-criteria.md`: testable acceptance criteria and edge cases.
- `creative-options.md`: optional product/design/technical ideas with rationale and risk.
- `owner-decisions.md` and `.csv`: decisions the user or project owner must make.
- `scope-control.md`: must-have, should-have, could-have, explicitly out-of-scope.
- `measurement-plan.md`: metrics, analytics, logging, QA, and verification signals where relevant.

## Rules

- Be creative, but do not hide which ideas are optional.
- Turn ambiguity into explicit questions, assumptions, and decision points.
- Prefer requirements that can be tested.
- Keep implementation recommendations modular and readable.
- Separate user-facing behavior from internal architecture and tooling.
