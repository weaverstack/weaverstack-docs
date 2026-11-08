# 0.11 developer-documentation coverage ledger

Evidence: runtime v0.10.0 `13a6fb359164d64b18da87f14c213c7064261a40` compared with frozen `efc046e7cf066daefd27f9268413ae05c3ed64e4`. `git log` and per-feature source/test changes were inspected. Product-site prose, enterprise experiment evidence and publication are owned by the parent agent, not this docs-only change.

## Release coverage

| Change | Runtime evidence at frozen head | Documentation owner and disposition | Validation |
| --- | --- | --- | --- |
| First `Schema__Object` separator (#254) | `c882a3e7`, declaration/model.py, installed.py; test_first_separator_name_declaration.py | Existing naming reference retained: first separator splits schema; subsequent separators belong to object; schema restriction retained. Release summary links it. Already covered by docs #12. | Focused naming tests; reference parser gate |
| Python workflow (#256) | `7fc253be`, workflow.py, operations/workspace.py; test_workflow_context_cycle.py | Python Session reference and core-concepts/sessions-and-workflows retained. Introduction now teaches shared run purpose. Load/Test records correlate; no invented Build/Health records or blanket notebook parity. Already docs #13. | Focused workflow tests; reference/journey gates |
| Test stale (#257) | `e6e6d7e9`, operations/test.py and CLI; Health-based selection | Existing Test behaviour retained: failed, invalid, Pending or stale validations; distinct from existing Load stale. Already docs #14, included in release summary. | Reference and journey gates |
| Execute (#258) | `ae493a31`, operations/execute.py; test_execute_cycle.py | CLI Execute and agents distinguish engine submission from Weaver bookkeeping; command/file alternatives and target/result matrix preserved. Already docs #15, now reconciled with new guide. | Execute tests; command parse gate |
| Installation lookup (#259) | `252bc5ce`, installed lookup path | Concise release-fix sentence in reference/index; no new tutorial. | Source/tag comparison |
| Folder mount publication (#264) | `332c2f0d`, runtime/folder_load.py, lakehouse.py; test_folder_change_feed_cycle.py | Release fixes describe publication through readers' mount, not remount-per-publication. Existing Folder journey retained. | Focused Folder tests |
| Shared Environment and Report-only catalogue (#265) | `6b62937f`, initialise.py, onboarding/project.py; test_initialise_resources_declaration.py | CLI Initialise, lakehouse/runtime, Mirror example: reference-only shared Environment, Read access, same capacity/network security; Report-only catalogue without Environment retained. | Focused Initialise tests; CLI parser; Microsoft primary source |
| Build/source-shape fixes (#265) | build_bundle/prune.py and runtime.py; semantic_models/binding.py; sessions/semantic_sources.py | Release summary covers housekeeping exclusion, new shortcut column readiness and Build/prune ordering. No new universal model-generation guarantees. | Source comparison; existing model requirements retained |
| Cycle tolerance (#266) | `b459ffd2`, graph.py; joined Health representation tests | Corrected dependencies, connected-items, Test/Assumption authoring, Load and across-catalogues. Data graph may cycle; deterministic once/run, no convergence; physical mutation actions cannot circularly wait. | Joined Health tests; contradiction search |
| Joined Health (#267) | `73901961`, operations/joined.py, operations/health.py, health.py | Across-catalogues and Health reference retained. Context and incomplete assessment explicit; source cross-workspace rejection removed. T05 separately confirmed and documented. | Joined Health tests and offline T05 probe |
| Joined Load/Test and barriers (#268/#269) | `a495b7e2`, `6cce4ac1`, joined.py and operation implementations | Across-catalogues teaches context versus selection; owner execution/records, workflow ID and readiness barriers retained. Recovery/selective-run journeys reviewed, retained unchanged where accurate. | Estate/reference/journey parser and offline gates |
| Cross-workspace Lakehouse Mirror (#270) | `5e5d3d17`, operations/mirror.py; test_mirror_plan_boundary.py | Mirror, concepts, advanced guidance and Health agree: Lakehouse crosses; Warehouse same workspace; unselected remote items unclaimed; live/deleted retained rows distinguished. Older incremental-build claim corrected. Reset warning preserved. | Mirror tests; relevant examples parsed |
| Multi-catalogue Dashboard (#270) | `5e5d3d17`, catalogue_dashboard package and renderer | Task-led introduction; eight page names; Direct Lake <=10 and Import >10, not unlimited; connection requirements next to deployment. Existing demo is current and includes Workspaces. | Generator drift check with #275 helper; rendered demo destinations verified |
| Static export (#271) | `efc046e7`, catalogue_dashboard export implementation | Dashboard export: model snapshot at export, Read+Build and tenant setting, writable local/OneLake path, offline local file versus inaccessible storage distinguished. | CLI/Python generated references and example parsing |

The original Dashboard, Mirror/materialisation, Build selection, native Power BI deployment and Load stale were not relabelled as entirely new 0.11 capabilities. The reference summary explicitly labels the development snapshot; PyPI install instructions still select the published release.

## T01–T10 disposition

| Item | Disposition |
| --- | --- |
| T01 Execute | Resolved in docs. No read-only claim; no assertion that arbitrary code cannot write catalogue rows. Generated signatures unchanged. |
| T02 Agents | Resolved. Restricted identity rather than config/confirmation as security; explicit dev config where supported; Check separate; workflow lacks JSON; Health not business proof. Complete CLI examples and copyable commands parsed. |
| T03 Cycles | Resolved in docs. Removed old universal item-cycle refusal and simple-ring edge algorithm; retained physical-plan constraint. Health suppression does not hide failed/Pending/overdue state. |
| T04 Mirror | Resolved in docs. Scope, source resolution, unselected remote ownership, retained rows, reset consequence agree. Existing correct same-name example retained. |
| T05 Remote mirror | Confirmed runtime blocker, not fixed. Separate T05 report and reproducible offline probe. Supported own-configuration invocation documented in Health reference. |
| T06 Permissions | Resolved in draft #16 and inherited by #17. Current Microsoft sources verify model ownership, default Environment Admin, Execute Queries Read+Build and SP restrictions, shortcut effective identity, shared Environment capacity/network. Installation overclaim removed. |
| T07 Context/selection | Resolved in docs. Repeated catalogue context is not selection; no-item default is working catalogue. Per-owner records and correlation retained. Product article command owned by parent. |
| T08 Article/platform | Outside this subagent's ownership; no product edits. Parent owns claims, organisational narrative and raw experiment evidence. No experiment figures introduced in docs. |
| T09 Dashboard/export | Resolved in docs. Current demo helper dependency verified; historical capture unchanged; local exported file not a live page or availability promise. Parent owns product captions. |
| T10 Routes/generation | Resolved locally. Canonical AI route/#json-output intact; all retained JSON fragments have contextual direct aliases. Route inventory updated. Static demo gate now checks real files and fragments rather than falsely rejecting valid assets; regression test proves missing assets/fragments still fail. CLI/Python/catalogue regenerated with zero content drift, semantic checked, demo checked using product #275 helper. |

## Editorial inventory

Changed task/concept paragraphs: agents, permissions, catalogue concept, Mirror concept/walkthrough/advanced guidance, Dashboard, across-catalogues, Sessions/workflows and operate. Updated canonical PROSE with purpose → task → mechanism, named actors, local requirements, exact security boundaries and evidence types.

Reviewed and deliberately retained: estate/recovery, selective-runs, catalogue-and-health and automation/deployment journeys; their task-led progression, source correction before retry, operation boundaries and explicit scope were already appropriate. Naming details and precise generated tables stayed precise. Historical terminal streams, manifest and demo dataset provenance were not edited. No Story, mission, branding, CI, packaging, runtime or live Fabric changes.
