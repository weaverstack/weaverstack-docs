# Developer-site explanatory prose revision

Baseline: `c84bf21842c6e98e72b97cac65f12e1cddd37a6d`.
Owning draft: weaverstack/weaverstack-docs #17, `docs/release-0.11`.

## Changes

Revised 31 developer pages, plus the repository's `PROSE.md`. The public changes are explanations, introductions and transitions, not a new site structure or a product-site copy pass.

- Lakehouse: Python first task, Spark SQL, validation, Shortcuts, incremental processing, runtime and section entrance.
- Warehouse: incremental-task starting state; existing effective explanations elsewhere retained.
- Semantic models: native TMDL, shared policy, composition, custom annotations, managed sources, standalone TMDL, validation and section entrance.
- Reports: section entrance, deployment, destination mappings and result interpretation.
- Estate: development cycle, operation, recovery, mappings, Catalogue/Health, Dashboard, cross-catalogue work, selective runs, concurrency and workflows/deployment.
- Concepts: local lifecycle explanations and descriptive compatibility links, preserving explicit fragment IDs. No navigation group added.

The revision explains the situation and relevant behaviour before the procedure, describes example starting states without repeated preservation orders, and connects recommendations to their reasons. Concrete steps, warnings and generated interfaces remain direct. `PROSE.md` no longer tells authors to lead every task with actions before explanation.

## Verification

- `git diff --check`: passed.
- `.venv/bin/python -m mkdocs build --strict`: passed after combined edits and again after the final Dashboard/cross-catalogue wording changes.
- Read-only comparison of every changed developer page against the baseline: 215 fenced blocks, 63 complete historical terminal captures and 10 Initialise example blocks were byte-identical. Explicit span IDs were retained; the renamed runtime subsection retains its previous fragment through an explicit heading ID.
- Built-output local-link check across all 31 changed pages: 5,992 links checked, no missing local files or HTML fragments.
- Actual browser review of all 31 changed routes at 1440×1000 and 390×844: 62 distinct route/viewport cases, no page-level horizontal overflow. Openings were read from rendered article text; selected screenshots were visually inspected. The final Dashboard and cross-catalogue text was rechecked after its final rebuild. This is not a claim of full-page screenshots for every route or a replay of every interaction.
- Loopback HTTP and private tailnet HTTPS both returned 200 with the new shared-policy introduction.
- No commands, generated examples or historical captures changed; no Fabric operations or new runtime acceptance replay were performed.

The earlier `check_developer_fixes.py` was attempted, but its fixed historical assertion of exactly nine pages changed from `36ad90f...` is no longer applicable to this wider revision. It stopped at that assertion before its checks ran. It was not weakened or presented as passing. The current-baseline preservation and rendered-link checks above cover this prose-only delta; previous source/parser and service evidence remains attributed to its original execution. The previously blocked full validation batch was not run.

## Delivery boundary

This is a developer-docs draft update, not publication authority. No PR merge, release, live Fabric mutation, workflow change or production deployment is part of this revision. The existing private docs preview serves the rebuilt site while its Mac remains awake and connected.
