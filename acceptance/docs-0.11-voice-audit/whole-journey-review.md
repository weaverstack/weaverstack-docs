# Whole primary developer-journey prose review

Baseline: `896dd1311972c4602790bc207c0142a67adb8970`, the earlier 31-page pass. The Start here correction was separately committed as `e300b767c694439ba67e4938ff1fcbd4b3551d80`; the remainder follows on the same draft branch for #17.

## Scope and correction

The previous pass changed flagged pages but omitted obvious entrances. This pass enumerated the full primary journey before sign-off: Home plus all 40 Markdown pages directly under Getting started, Lakehouse, Warehouse, Semantic models, Reports and Estate. Full explanatory prose was reviewed, including prerequisite paragraphs, conceptual boundaries, text between commands and result interpretation. Exact steps and safety instructions were deliberately retained. Reference/generated interfaces and the full retained Basics/Advanced/concept corpus are not claimed as reviewed by this pass.

Against the baseline, 27 primary pages were revised and 14 deliberately retained. This is a coverage record, not a claim that removing imperatives guarantees good prose. Parent reviewed the combined model/Report diffs; a complementary editor read all 11 model/Report pages in full and revised nine of them.

All paths below are relative to `docs/`.

| Page | Disposition | Reason |
| --- | --- | --- |
| `index.md` | Revised | Explanation at the front door instead of “Keep writing… Start…”; item descriptions explain their subjects. |
| `getting-started/index.md` | Revised | Introduces the examples before the actual installation and route-selection steps. |
| `getting-started/installation.md` | Revised | Introduces the package and runtime prerequisite; removes duplicate package description. Actual installation commands remain direct. |
| `getting-started/first-project.md` | Revised | Retained entrance explains the Warehouse example and validation continuation instead of assigning a task. Compatibility anchors remain. |
| `lakehouse/index.md` | Retained | Existing explanatory opening and navigation links serve different jobs appropriately. |
| `lakehouse/python.md` | Revised | Closing transition explains the existing SQL transformation; explains when declaration edits take effect. |
| `lakehouse/spark-sql.md` | Retained | Full prose explains the current-status query, its existing installation and expected result. Instructions belong to the actual query check. |
| `lakehouse/tests.md` | Revised | Starting state and source-file versus recorded installed-mode results are explained. Failure/restoration steps remain direct. |
| `lakehouse/incremental.md` | Revised | External-source prerequisites and data-only versus post-Build catch-up distinction explained without preservation orders. |
| `lakehouse/shortcuts.md` | Revised | Explains the connection-only scope and logical source identity; separates it from the complete processing example. |
| `lakehouse/runtime.md` | Revised | Explains the page's runtime subject and existing bindings rather than instructing the reader to use the page. Publication steps and runtime requirements remain. |
| `warehouse/index.md` | Retained | Already explains the SQL declaration and installed work; remaining invitations are navigation. |
| `warehouse/first-project.md` | Revised | Opening and event-Table explanation describe how a SELECT becomes maintained data rather than issuing “Keep…” orders. |
| `warehouse/tests.md` | Revised | Describes the working example's loaded data and validations rather than repeating setup instructions. |
| `warehouse/incremental.md` | Retained | Explains candidates, deletes and bookmarks between concrete source-change steps. External-target and destructive-data safeguards remain appropriate. |
| `warehouse/schema-and-protection.md` | Retained | Explains schema, keys and recoverability; direct instructions protect source data and identify the actual metadata edit. |
| `semantic-models/index.md` | Retained | Explains operating modes and consequences; remaining directives are navigation. |
| `semantic-models/native-tmdl.md` | Revised | Starting conditions, selected Build result, measure comparison and deployed versus local observations explained. |
| `semantic-models/shared-policy.md` | Revised | Explains which policy sections contribute, why duplication is optional and where the merged result can be observed. |
| `semantic-models/composition.md` | Revised | Explains additive bindings, source-only base and broad-selector refusal; policy application is conditional on adding it. |
| `semantic-models/custom-annotations.md` | Revised | Explains handler discovery and the actual separate-model continuation; executable-code and restoration warnings preserved. |
| `semantic-models/from-tmdl.md` | Revised | Explains single-file authoring, same-name identity, generated results and existing service connection. |
| `semantic-models/managed-sources.md` | Revised | Interprets source rows as model input and explains connection ambiguity rather than saying “keep one”. |
| `semantic-models/validation.md` | Revised | Explains the two checks, input comparability and command responsibilities; removes duplicated source-mode prose and generic evidence-inspection orders. Test records; Health reads. |
| `reports/index.md` | Retained | Existing explanation distinguishes local association and deployed binding, with appropriate selection rules. |
| `reports/deploy.md` | Revised | Explains what the complete native payload contributes and the starting workspace conditions. |
| `reports/environments.md` | Revised | Explains inline versus estate starting configurations and why workspace identity matters in the binding check. Overwrite and disposable-workspace instructions preserved. |
| `estate/index.md` | Retained | Establishes connected-work questions; remaining invitations are section navigation. |
| `estate/connected-items.md` | Revised | Explains the cross-item situation before the Shortcut and why both selected items matter to ordering. |
| `estate/environments.md` | Retained | Opening now explains destinations and runtime/source responsibilities. Remaining commands form the concrete mapping procedure. |
| `estate/catalogue-and-health.md` | Retained | Explains current state and named findings, with concrete evidence and a decision table. Catalogue-write warning is a real integrity constraint. |
| `estate/catalogue-dashboard.md` | Retained | Explains Dashboard lifecycle and recorded state; remaining UI directions are interaction instructions and deployment steps. |
| `estate/across-catalogues.md` | Retained | Explains dependency context versus execution scope and how catalogues join. Scoped examples then direct concrete actions. |
| `estate/development-cycle.md` | Revised | Explains installed-source boundaries, model-inclusive starting state and the optional Mirror baseline between worked commands. |
| `estate/operate.md` | Retained | Explains state-based operation choices. Its decision guidance and concrete Load/Test/Health steps appropriately instruct. |
| `estate/mirror.md` | Revised | Explains borrowed baseline and mirrored destination configuration rather than another question-and-command opening. Destructive warnings and confirmations preserved. |
| `estate/selective-runs.md` | Revised | Explains why omitted producer work must already be current instead of appending a generic preservation instruction. |
| `estate/concurrency.md` | Revised | Explains when independent work can benefit and how measurements distinguish contention from improvement. |
| `estate/performance.md` | Revised | Introduces causes of elapsed time, explains controlled comparisons and scopes benchmark interpretation instead of issuing generic measurement maxims. |
| `estate/recovery.md` | Revised | Explains the existing model-recovery project and bindings; actual recovery and destructive confirmation steps remain direct. |
| `estate/automation-and-deployment.md` | Retained | Explains workflow/Session/bundle responsibilities, with appropriate authorisation, integrity and secret-store requirements at concrete steps. |

## Verification

- Strict MkDocs build and diff whitespace check passed on the combined revision.
- Comparison against the baseline across all 41 primary pages: 255 fenced blocks, 79 historical CLI captures, 16 Initialise example blocks and one inline SVG unchanged. Heading lines and existing explicit span IDs unchanged.
- Built-output local links checked across all 41 pages: 7,628, with no missing file or HTML-fragment targets.
- Browser review re-entered through Home and Start here, then Installation, Warehouse first task, Lakehouse Python, connected items, Mirror, performance, shared model policy and model validation, at desktop and mobile sizes: 20 distinct cases, no page-level horizontal overflow. Selected screenshots were visually inspected. This is not a replay of all interactions or service execution.
- Earlier 62-case browser evidence belongs to the earlier revision; it is not claimed as a fresh 82-case review here.
- Commands, generated examples, historical captures, runtime and production resources were not changed. No previously blocked full validation replay was run.

The existing private preview serves the rebuilt site. Delivery remains an update to draft #17, not a merge or production deployment. Editorial judgment is not established by the numerical checks; the page inventory prevents another omitted front door, while the continuous reads assess the actual explanations.
