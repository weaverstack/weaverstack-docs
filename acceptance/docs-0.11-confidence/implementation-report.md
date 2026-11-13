# Developer documentation confidence pass

## Ownership

Starting heads: #17 `83e3252c5371175e33f9862980747ad22ba297a4`; #16 `7bc1ccb04397458961f12ba10ed1cee4167b9fbf`. Frozen runtime: `efc046e7cf066daefd27f9268413ae05c3ed64e4`.

D11 was committed in #16 as `7442917e4dc24f580364727b219a4c9de49064af`, then ordinarily merged into #17 by `d3d27e502ebb120944b48e8f477ed97caf9fd034`. Other edits belong to #17; final head is in the delivery response. Remote bases unchanged; no pushes or publication. `dispositions.json` supplies the exact D01–D12 ledger.

## Outcomes and placement

- Dashboard: replace lifecycle exclusions with reading catalogues in place and managing the model/Report separately. Exact independence is in `reference/cli/catalogue-dashboard.md`; requirements lead deployment.
- Operate: replace “Health does not…” with Build → Load → Test → Health. Completed changes remain after failure; inspect failed steps for partial changes and use Recovery.
- Across catalogues: explain context versus selected execution; keep working-catalogue defaults and exact selectors. Correct the adjacent estate-index caption.
- AI: lead with development actions; consolidate least-privilege permissions and approval policy; finish with scoped Health findings and authored Tests/Assumptions. Preserve exact commands, output fields, versions and compatibility/stream contracts. Execute bookkeeping links its existing CLI reference.
- Permissions: lead with Contributor/read access; retain one tenant-admin answer and the verified matrix. Remove only the duplicate ownership rebuttal.
- Health: retain T05 under “Limitation and workaround”: assess from the mirror's own configuration with `mirror:` set; joined remote mirror remains unassessed even with production supplied, and joined scope is incomplete. Internal cause belongs here: remote workspace resolution clears the mirror configuration.

## D02 research and backlog

Searched both repositories for best-effort, Fabric Apps and support-policy wording; inspected available history with `git log --all -S 'best effort'`; read introducing Dashboard documentation commit `8bf0ca500b70bbdc8dee3b420ace042e09f6f270` (#7). It introduced the two sentences under the HTML Content heading. The commit explains playable pages/rendering, not formal support terms. No separate formal policy or committed Fabric Apps promise was found in the frozen runtime or available repository history.

Evidence does not settle whether “best effort” meant formal policy or informal status. Conservatively retained that restriction in named `reference/cli/catalogue-dashboard.md#support-and-compatibility`, linked from the guide. Concrete visual requirements and export alternatives remain beside use. Maintainer backlog: clarify Report support terms and evaluate the earlier idea of supplementing/replacing it with Fabric Apps. Neither is a public roadmap commitment.

## Technical consistency and adjacent sweep

Read frozen `declaration/item_dependencies.py` (`_inferred_references`, `_shortcut_reference`): physical references have no Build-time project producer. Read `catalogues.py:230–324`: join matches workspace name, kind and item name, then source object. `core-concepts/dependencies.md` now distinguishes Build inference from joined Health/Load/Test. Existing precise Health join wording was kept.

Changed nearby `estate/environments.md` (configuration, installed bindings, deliberate Mirror), `estate/development-cycle.md` (installed-source sequence, partial changes, existing-target preview), `estate/index.md` and one mixed borrowed/local sentence in `estate/mirror.md`.

Reviewed and kept `docs/index.md` including metadata/captions; `estate/recovery.md`; `core-concepts/catalogue.md`; relevant CLI summary/selection and Execute reference passages. Their negative statements preserve concrete syntax, failure, data-loss or compatibility rules. Product comparison is parent-owned; there is no developer comparison page. This is a bounded adjacent review, not a whole-site audit.

Replaced conflicting terse/defensive instructions in canonical `PROSE.md`: public explanations teach; comments/diagnostics stay concise; evidence-backed benefits/recommendations are welcome. Public maintenance-process commentary remains excluded. Read Style Manual sentences and Microsoft style/voice guidance. Existing delivery skill did not contradict this direction and needed no duplicate policy.

## Safeguards retained

Mirror destination catalogue/selected-target reset; cross-workspace Lakehouse versus same-workspace Warehouse scope; remote unselected ownership and live/retained Mirror rows. Recovery/Wipe/Reload partial-state and reset consequences. Single-pass deterministic cycles and exact Health timestamp rules. Model ownership; Execute Queries Read+Build and service-principal limits; default-Environment Admin; shared Environment Read/capacity/network; shortcut effective identity. Execute mutation; explicit development configuration; production prohibition and plan approval. Existing release coverage and old evidence unchanged.

## Verification

`validation.json`: **20/20 pass** using the existing validation bundle, with output redirected here to preserve old evidence. Includes strict build, four generated-reference checks, Dashboard demo check with existing product helper, four offline example suites, integrated routes, route/generator tests, CLI parser checks, offline T05 reproduction and diff check.

Routes: 114 original pages, 872 fragments, 35 canonical pages, 28 compatibility routes and 5,184 links; no errors. CLI: 81 complete examples on 14 pages parsed without handlers. T05 reproduced with offline read boundaries; own-configuration source resolution passes.

`check_preservation.py` and `preservation.json`: all 12 changed public pages retain exact shell blocks, historical CLI captures and generated sections relative to starting #17.

`browser-review.json`: nine routes at 1440×900 and 390×844, no document overflow or broken images. Visually inspected desktop AI and mobile Dashboard openings; read rendered AI journey and Health workaround. Not a full interaction/accessibility audit.

Initial validation caught an incorrect new Execute link; corrected to the existing CLI owner and reran all checks. `validation-initial.json` retains failure. Two builds total (initial failed strict build, corrected final build); no further rebuild planned. Existing 8891 server left running unchanged. No runtime, CI, generated captures, live Fabric or tenant changes.
