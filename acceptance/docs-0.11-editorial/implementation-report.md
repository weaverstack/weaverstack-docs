# Weaver 0.11 documentation editorial implementation report

## Scope and revisions

This is the developer-documentation portion of the supplied editorial brief. Product-site/article edits and raw enterprise experiment reconciliation remain with the parent agent. No runtime source, CI workflow, packaging/release configuration, VERSION, historical capture, tenant setting, capacity or live Fabric resource was changed. No merge, release or publication was performed.

Starting heads, freshly fetched and confirmed as open drafts:

- Docs main: `0c4d7888e3e694b63ecb5aa3aa79331f1c7078fb`.
- Draft #16, `docs/permissions`, base main: `ee4a8f9f7ae4f5d8cb555a7a0bf6067eb0bae4aa`.
- Draft #17, `docs/release-0.11`, base docs/permissions: `3239dd004c52327c1319a0275c49ae6bacc9336c`.
- Runtime source baseline v0.10.0: `13a6fb359164d64b18da87f14c213c7064261a40`; reviewed snapshot and refreshed origin/main: `efc046e7cf066daefd27f9268413ae05c3ed64e4`.
- Demo helper source: parent product worktree `/Users/matthiaswong/dev/.worktrees/weaverstack-011-editorial-site`, starting #275 head `13da9c688446c262ad38a381aefba56caf5c22d0`, with the parent's in-progress product prose. Its runtime/helper files were read, never edited here.

Isolated owning worktrees:

- `/Users/matthiaswong/dev/weaverstack-docs-editorial16`, local branch `docs/editorial-permissions`.
- `/Users/matthiaswong/dev/weaverstack-docs-editorial17`, local branch `docs/editorial-release`.
- `/Users/matthiaswong/dev/weaverstack-editorial-runtime`, detached frozen source, locally installed dependencies only.

Existing user/agent checkouts were left untouched, including the runtime root's unrelated `.claude/launch.json` modification.

Implementation heads:

- #16 corrections: `7bc1ccb04397458961f12ba10ed1cee4167b9fbf` (permission matrix and installation).
- #17 rendered content: `a1d26e4` (technical/editorial reconciliation), route retention/gate: `2a9d865a86759ef1a79a7f87ec7f833a32a3a2e9`.
- This report and validation/probe files are an additional acceptance-only commit. The exact final pushed PR head is read back from GitHub after that commit and returned in the delivery response; embedding a commit's own hash in its tracked report is not possible.

#16 was kept separate and merged forward into #17 with ordinary merge commits, preserving both existing stacks and draft bases. No rebase or force push is required. Before any update, fetch and compare both named remote branches with the starting heads; abort if either changed concurrently. Push only the two existing draft branches, then read back each PR head/base/draft status.

## Outcomes and teaching changes

The complete feature/T01–T10 ledger is [coverage-ledger.md](coverage-ledger.md). The confirmed runtime boundary is [T05-remote-mirror.md](T05-remote-mirror.md), separate from editorial sign-off.

Representative changes:

| Surface | Before | After and purpose |
| --- | --- | --- |
| AI/Execute | Agent can inspect data “without changing state”; withholding `--yes` prevents emptying a target | Engine submission can write; Weaver bookkeeping is separate. Permissions constrain the agent, confirmations do not. |
| AI workflow | Put workspace config and JSON on every command | Complete development loop uses supported flags; local Check has no workspace config; Workflow has no JSON. Configuration discovery is explained. |
| Catalogue | Starts by defining configured Warehouse/state storage | Starts with investigating a failed load, then explains where records live. Source/configuration/installed-state distinctions remain. |
| Across catalogues | “Nothing else is declared”, followed by compressed binding/path/ancestry mechanism | Continues Planning's named Shortcut to Operations' Table, then explains Health and why both catalogues are needed. Context is separate from selected work. |
| Mirror | Logical/physical identities precede the development task | Starts with changing a Table against existing data, keeps project files and development mapping, then explains local materialisation. One clear reset warning remains. |
| Dashboard | Eight page purposes compressed into one opening sentence | Starts with what ran/needs attention; Workspaces/Items lead into failure investigation, with exact deployment requirements beside the task. |
| Permissions | Contributor enough for everything | Ordinary Build/Load default plus exact ownership, Admin, data-access, query and shared-runtime requirements. |

PROSE is the canonical updated editorial policy; AGENTS was not given a competing manifesto. Recovery, selective runs and existing accurate journeys were reviewed without gratuitous rewrites. Reference signatures/inventories remain generator-owned.

## Microsoft source verification

Retrieved current primary documentation during this task:

- [Workspace roles](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces) and [Warehouse roles](https://learn.microsoft.com/en-us/fabric/data-warehouse/workspace-roles): Contributor write/control and Viewer SQL reads; workspace role is not every task prerequisite.
- [Bind semantic model connection](https://learn.microsoft.com/en-us/rest/api/fabric/semanticmodel/items/bind-semantic-model-connection): caller must own the model. Weaver's semantic binding path uses this API.
- [Environment creation/use/sharing](https://learn.microsoft.com/en-us/fabric/data-engineering/create-and-use-environment): only Admin can update the contents once selected as workspace default; cross-workspace attachment requires same capacity and network security settings and Read permission; consuming workspace supplies compute/pool settings.
- [Execute Queries](https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries): Read+Build and query tenant setting; SP not supported with RLS or SSO. API page uses Dataset terminology; portal documentation also uses Semantic Model terminology, which the page distinguishes.
- [Shortcut security](https://learn.microsoft.com/en-us/fabric/onelake/onelake-shortcut-security): access path/effective identity matters; Direct Lake over SQL and T-SQL delegated mode are not universal caller passthrough.
- [Organisational visuals](https://learn.microsoft.com/en-us/fabric/admin/organizational-visuals) and [tenant settings](https://learn.microsoft.com/en-us/fabric/admin/tenant-settings-index): organisational store route retained; no claim about HTML Content certification.

The three supplied dbt editorial examples were consulted for task/reason/example progression, not copied or used to invent competitor claims.

## Exact local validation

Reproducible command bundle and complete command/stdout/return-code evidence: `run_validation.py`, `validation.json` in this directory.

```bash
cd /Users/matthiaswong/dev/weaverstack-docs-editorial17
.venv/bin/python acceptance/docs-0.11-editorial/run_validation.py \
  /Users/matthiaswong/dev/weaverstack-editorial-runtime \
  /Users/matthiaswong/dev/.worktrees/weaverstack-011-editorial-site
```

Final parent rerun: **20 of 20 checks pass**. The initial 19/20 result exposed a stale format assertion; the correction and boundary are detailed below. Passing checks include:

- `python -m mkdocs build --strict`, with no broken-fragment diagnostics.
- CLI/Python/catalogue/semantic `--check` against the frozen runtime. CLI/Python/catalogue were also run with `--write`; output was already current, no hand-edited generated facts.
- Demo `--check` using parent #275 helper: 10 files current, including Workspaces. No generated demo changes needed.
- Estate continuation: 108 commands, five configurations, three selection plans; reference gate: 117 commands, six configurations, 15 operation calls, two DAX files and one native edit; journey gate: 20 pages, 120 commands, five configurations, three Python calls. These are local parser/fixture checks, not engine execution.
- Complete changed-page shell examples and all runnable guide/template commands: 54 parsed examples across 11 pages. Bare command names and the explicit `<command>` syntax placeholder are references, not executable snippets. Negative checks confirm Check rejects workspace config and Workflow rejects JSON. Parser help/version can return SystemExit(0); handlers never execute.
- Route crawl against actual built docs plus parent's product source: 114 original pages, 872 fragments, 35 canonical pages, 28 compatibility routes, no errors. Canonical `/reference/ai-agents/#json-output` exists. All old machine-output section anchors have contextual direct links to the new owner, with no pointer chain.
- Route self-tests (12), new static-asset regression test (1), CLI/Python/catalogue/semantic generator tests and `git diff --check` pass. The asset test was observed failing before the fix; it still rejects absent files/fragments rather than suppressing errors.

Separate source tests, from the frozen runtime worktree:

```bash
.venv/bin/python -m pytest -q \
  tests/test_execute_cycle.py \
  tests/test_workflow_context_cycle.py \
  tests/test_first_separator_name_declaration.py \
  tests/test_initialise_resources_declaration.py \
  tests/test_folder_change_feed_cycle.py \
  tests/targeted/test_joined_health_representation.py \
  tests/targeted/test_health_operation_boundary.py \
  tests/test_mirror_plan_boundary.py
```

Actual result: **296 passed in 13.67s**, core tests, no declared Fabric resources. The earlier narrower Health/Mirror suite passed 61 tests. T05 probe passes while confirming the defect, not fixing it.

#16 separately passed strict MkDocs and diff checks using the locked #17 docs interpreter. `uv` was initially missing from PATH; installed it only in the isolated docs virtualenv, then synced the unchanged lockfile with Python 3.11. No global tooling or repo dependency files changed.

## Rendered review and paths

Final docs build path: `/Users/matthiaswong/dev/weaverstack-docs-editorial17/site/`.

Browser checked actual loopback-served HTML at 1280px desktop and 390px mobile for agents, permissions, across-catalogues, Mirror and Dashboard. Body widths did not exceed viewport widths. Dark desktop/mobile and light mobile screenshots were inspected; the long copyable instructions scroll within their code block. Canonical JSON and legacy Health fragment elements were verified. This is targeted layout/editorial review, not a claim of exhaustive keyboard/no-JavaScript/clipboard/console testing or a deployed-site check.

Raw browser metrics are retained in the session browser workspace; `browser-review.json` records the observed metrics for review. The temporary loopback server is test-only, not a publication.

## Provenance and remaining blockers

1. **T05 runtime defect:** confirmed and documented, not fixed. Own-configuration source resolution works; remote place loses `mirror` before assessment. No live Fabric rerun authorised.
2. **Pre-existing fixture mismatch resolved:** `tools/check_docs_refresh_examples.py` needs its documented `--runtime-revision efc046e7cf066daefd27f9268413ae05c3ed64e4` override. The initial run then failed at the Executive format assertion: it expected the base's `#,##0`, whereas the starting fixture deliberately overrides it with `0 "delivered"`. The parent corrected the exact assertion to require the authored Executive override. The fixture and runtime are unchanged, and the full 20-check bundle now passes. This verifies the documented composition rather than weakening the assertion or altering behaviour to suit it.
3. **Historical capture:** `152-catalogue-dashboard` remains the actual single-catalogue deployment capture from runtime `afb5b31c36498aeb8b70927e7f723de054225d5e`, package `0.9.0.dev (checkout build)`, manifest provenance 16 October. It has not been relabelled as a new multi-catalogue run. The generated demo retains its fixed October dataset timestamp and uses the current renderer; no new live evidence is claimed.
4. **Experiment evidence:** no 50-workspace counts/timings were introduced or independently reconciled by this docs-only subagent. Parent owns the article's evidence ledger and historical measurement decisions.
5. **Publication dependency:** docs strict build does not execute the demo generator and does not require #275's helper. Regenerating/checking the demo does require that helper; local check used the integrated product worktree. Product #275 links to docs #17. Later authorised sequence: land the helper/product source and docs stack in a coordinated window; publish docs routes before product links become public, or coordinate both site publications. Do not equate helper availability with permission to merge/release.

No existing check was weakened to hide the fixture failure. Push/remote verification and draft preservation are reported separately from local build, tests and future publication.
