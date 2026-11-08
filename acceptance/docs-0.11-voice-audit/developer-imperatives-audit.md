# Developer documentation: explanation versus instruction

## Reviewed revision and scope

Repository: `weaverstack/weaverstack-docs`.
Reviewed HEAD: `c84bf21842c6e98e72b97cac65f12e1cddd37a6d`.

This is a source editorial audit, not a rewrite or technical acceptance run. Product-site copy is out of scope. No public prose, commands, captures, runtime behaviour or configuration were changed. No build, push or publication was performed. This report is an uncommitted review deliverable.

The entrance pass inspected the opening material of 40 Markdown pages under Getting started, Lakehouse, Warehouse, Semantic models, Reports and Coordinate your estate. Selected bodies were read for context, alongside a complementary full-page review of ten estate/concept pages. This is not a claim that every paragraph of the entire documentation site was audited. Generated help and historical terminal captures are not prose-editing targets. Reference was sampled to distinguish appropriate contract language from guide prose, not comprehensively audited.

## Verdict

The problem is recurring across the developer journey, particularly in introductions and transitions. The pages often announce an exercise or issue a recommendation where they should explain a subject, a decision or a relationship. A helpful second-person voice has too often been implemented as an instruction to the reader.

It is not uniformly bad. Worked sequences mostly need their direct instructions. Several explanatory paragraphs already teach well. Nor is every opening verb a defect: an outcome-first first task can be effective when it immediately establishes what the example demonstrates.

The useful distinction is the job of the passage:

- An introduction establishes the subject, situation and purpose of the example.
- An explanation gives the reader a model for reasoning about behaviour.
- A procedure directs a concrete action and supplies an expected observation.
- Reference specifies an exact contract.
- A safety warning directs behaviour at a consequential boundary.

Counting verbs, inserting “you”, adding passive voice, or expanding every sentence would not address this distinction.

## Findings

### DD01 — High: introductions announce exercises instead of explaining capabilities

Examples:

- `docs/semantic-models/shared-policy.md:3`: “Apply the same formatting and calculation structure to several models without copying the convention into each native project. Shared policy is TMDL; custom Python is not required.”
- `docs/semantic-models/composition.md:3`: “Reuse a source foundation without deploying it as a physical base model. Give each output its own additions, Report and validations.”
- `docs/semantic-models/native-tmdl.md:3`: “Deploy native PBIP/TMDL, query a measure, then hide relationship foreign keys with one modelling rule.”
- `docs/lakehouse/incremental.md:3`: “Update one carrier file, remove another, and Load the installed pipeline again.”

These are plausible task summaries. Used repeatedly as introductions, however, they make the manual sound like a succession of assignments. The reader encounters the exercise before understanding the capability it demonstrates. Shared standards and model variants especially deserve a short explanation of the modelling problem before the first file operation.

Illustrative direction for shared policy, not approved replacement copy:

> Several models often share formatting and modelling conventions, even when their measures and data differ. A shared TMDL policy holds those common declarations in one place. This example applies that policy to Parcel, then shows how its local overlay can override one format.

The correction is the explanatory sequence, not merely changing “Apply” to “You can apply”.

### DD02 — High: question-and-command openings simulate a conversation without developing one

- `docs/estate/environments.md:3`: “Where should the same project deploy? Keep its documents and logical item names unchanged.”
- `docs/estate/concurrency.md:3`: “Can this run use less simultaneous work? Add `--concurrency 2` to limit it to two scheduled nodes. Leave the setting out when the normal configured limits are appropriate.”
- `docs/estate/selective-runs.md:3`: “Can you rerun only this Table and the work it affects? Start with a named Load preview, then add upstream or downstream work when that is the intended scope.”

A rhetorical question is followed immediately by an instruction. That pattern changes the surface tone but still skips explanation. The concurrency opening, for example, presents the flag before establishing the distinction between ready work, scheduled concurrency and available compute.

These pages need short contextual introductions, not a ban on questions. The command and example value belong in the worked section that follows.

### DD03 — High: prerequisites are repeatedly expressed as preservation orders

- `docs/lakehouse/incremental.md:5`: “Continue the [Landing project](tests.md) in the same folder. Keep Events, Event, CurrentStatus and their validations. Add a separate `Parcel.StatusFiles` Folder and incremental `Parcel.LiveStatus` Table for changing carrier snapshots.”
- `docs/semantic-models/shared-policy.md:5`: “Continue the [native Parcel model](native-tmdl.md#hide-relationship-foreign-keys) … Add only the policy and format override below, keeping your workspace configuration.”
- `docs/estate/automation-and-deployment.md:5`: “Continue the working Landing/Operations project and `workspace-development.yml` … retain those bindings too … Omit that Build when your project has no Power BI items.”

The underlying information matters: readers need to know the starting state, additions and what remains unchanged. The cumulative “Continue / Keep / Add only / Retain / Omit” rhythm sounds like constraints supplied to an editing agent.

Where no active safeguard is needed, describe the starting state and the extension. For example, the incremental task starts with a working Landing pipeline and adds two separately named objects; the existing pipeline remains unchanged. Keep explicit preservation instructions beside steps where overwriting or deleting is a real risk.

### DD04 — High: the development-cycle recommendation is issued before its reason

`docs/estate/development-cycle.md:64`:

> Use an item-wide run by default. Plain named Load does not add or order dependencies.

The second sentence is an important technical distinction, but the passage asks the reader to adopt a rule before explaining why it is the ordinary choice. An explanation should connect the default recommendation to execution behaviour: an item-wide run follows the installed item graph, whereas plain named Load narrows selection without automatically adding or ordering dependencies.

The revised introduction at lines 3–5 is substantially better. This remaining paragraph shows why fixing the first two paragraphs alone does not settle the page's voice.

### DD05 — Medium: interpretation after a run becomes a generic inspection order

`docs/estate/selective-runs.md:163`:

> Event ran before CurrentStatus. Inspect each outcome; attempted is not the same as succeeded.

This is the point where the guide should help the reader interpret the result. “Inspect each outcome” is a generic assignment rather than an explanation of what the output establishes. The surrounding paragraph usefully supplies the expected statuses and identifies Operations as outside the invocation; that concrete interpretation should carry the explanation.

Do not remove outcome verification. Place the actual check with its observable result, rather than appending a general maxim to every run.

### DD06 — Medium: concept prose switches into command mood mid-explanation

- `docs/core-concepts/build-load-and-test.md:39`: “Reports have definitions, not a Load or Test target; refresh and validate their model.”
- Same page, line 58: “Build Lakehouse/Warehouse definitions first, then semantic models and Reports in a separate call against the same project; a workflow can contain both steps.”
- `docs/estate/across-catalogues.md:43`: “Give Weaver both catalogues and it matches that Shortcut to the Table recorded by Operations.”

These passages are explaining lifecycle boundaries and a join mechanism, not introducing new procedural steps. They should finish explaining the relationship. For example: refresh and validation belong to a Report's semantic model; supplying both catalogues lets Weaver match the recorded Shortcut to the recorded producer.

The required source-data/model Build separation must remain precise. The worked sequence is appropriately taught in the development task. This is a local prose correction, not a reason to expand every concept paragraph.

### DD07 — Medium: Dashboard lifecycle is expressed as an unexplained management rule

`docs/estate/catalogue-dashboard.md:12`:

> The Dashboard reads the catalogues in their existing workspaces. Manage its semantic model and Report separately with `weaver catalogue-dashboard` and the Fabric interface.

“Manage … separately” directs behaviour before making the separation clear. The useful introductory information is that the Dashboard's model and Report have their own management lifecycle while reading the catalogues of the projects they describe. Deployment and removal steps can then instruct the reader.

The opening also uses “use”, “Run”, “Start” and “Use” in lines 8–10. Some are useful navigation, but together they make an overview feel like a quick-start checklist. This is lower priority than missing teaching in the core development pages.

### DD08 — Medium: explanatory runtime distinctions are organised as directives

`docs/lakehouse/runtime.md`:

- Line 3: “Publish the Python packages once, then keep editing and building your project.”
- Line 54 heading: “Keep the runtime and project changes separate”.
- Line 56: “Republish after changing Environment libraries or the Weaver package mode/version.”

The body already contains valuable explanation: ordinary project edits do not require Environment republication, whereas package changes do. That distinction should lead the explanation instead of being phrased mainly as advice to maintain two processes.

Do not remove “publish” from the actual first-publication procedure, the matching-version requirement, or instructions needed to make a hosted Spark session work. A heading such as “Runtime updates and project updates” could identify the subject without inventing another command.

### DD09 — Low: a compatibility landing page sounds like internal routing

`docs/core-concepts/index.md:8–24` repeatedly uses “Continue”, “Open estate task” and fragment-specific “Continue:” links to the same estate entrance.

This page is search-excluded and retained for compatibility, so it is not a primary journey problem. Nevertheless, direct entrants receive routing instructions without a useful account of where the material lives. One brief explanation and descriptive link could retain existing fragment IDs without repeating commands.

Do not turn this into a new concept hub or navigation redesign.

### DD10 — Contributing editorial cause: the prose policy is too easy to apply mechanically

`PROSE.md:14`:

> **Lead with actions and outcomes.** In task pages, state the prerequisite, action and observable result before mechanism detail.

Later guidance correctly asks for a recognisable situation and enough explanation to teach (`PROSE.md:22–26`, `38`, `73–81`). The earlier rule nevertheless gives an editor an easy recipe: begin with an imperative, then append mechanism. The repeated task-summary openings are consistent with that recipe.

An eventual correction should distinguish introducing the task from directing its steps. The rule should not be replaced with an equally absolute ban on imperative openings or a mandatory motivational paragraph on every page.

## Material to preserve

### Appropriate instructions

- `docs/estate/development-cycle.md:17`: “Open `Lakehouse/Landing/Files/Parcel__Events.py`. In the `EVENTS` CSV constant, replace just this row:” — a concrete step with an exact source change.
- `docs/estate/mirror.md:25`: “Compare the plan with the names above; answer `y` only if they match.” — a consequential confirmation boundary.
- `docs/core-concepts/catalogue.md:91`: “Query the `_` schema to inspect an estate, but do not edit catalogue rows by hand.” — a state-integrity warning followed by its reason.
- `docs/semantic-models/custom-annotations.md:9`: “Do not Check or Build an untrusted project.” — a trusted-executable-code warning.
- Instructions inside the copyable AI-agent brief — their intended audience is an executing agent, so directive language is appropriate.
- Generated CLI help, historical output and exact interface requirements — not candidates for a general voice rewrite.

### Explanations that already work

- `docs/warehouse/index.md:3`: a T-SQL SELECT and metadata comment become a maintained Table and recorded work.
- `docs/warehouse/incremental.md:3`: the SQL supplies candidate rows/delete keys; Weaver supplies the merge and consumer progress.
- `docs/warehouse/tests.md:33`: independent expected rows expose a defect in the View's window function.
- `docs/lakehouse/incremental.md:9`: separate consumers have separate bookmark boundaries.
- `docs/semantic-models/validation.md:3`: “A successful refresh says the model ran, not that its measure is right.” The following mode explanation is useful and should not be rewritten merely to match a new stylistic formula.
- `docs/estate/development-cycle.md:3–5`: the revised opening now explains ordinary development before introducing the example.

## Recommended correction order

1. Introductions and prerequisite transitions across the main developer journey: DD01–DD03.
2. Explanatory decisions and interpretation in development/operation pages: DD04–DD05.
3. Local concept and runtime passages: DD06–DD08.
4. Low-traffic compatibility copy: DD09.
5. Clarify the prose policy alongside the edits so the pattern does not return: DD10.

Review each finished page continuously. A replacement that merely changes “Use X” to “X can be used” is not an editorial fix. Equally, a long invented motivation before every command would overcorrect. Preserve the working example, technical scope and meaningful safety requirements.

## Coverage record

Entrance pass: all 40 Markdown pages directly under `docs/getting-started`, `docs/lakehouse`, `docs/warehouse`, `docs/semantic-models`, `docs/reports` and `docs/estate`, including the retained first-project entrance.

Main contextual body review: Getting started and installation; Lakehouse index, Python, runtime, incremental, Spark SQL, Shortcuts and tests; Warehouse index, first project, incremental, tests and schema/protection; Semantic models index, native TMDL, shared policy, composition, managed sources, custom annotations, standalone TMDL and validation; Reports index, deployment and environments; estate selective runs, concurrency, recovery and automation/deployment. Source examples and captures were treated as context, not voice findings. Large source reads were retained in tool output; the audit does not assert a new technical verification of those examples.

Complementary full-page review: `estate/index.md`, `estate/development-cycle.md`, `estate/operate.md`, `estate/environments.md`, `estate/across-catalogues.md`, `estate/mirror.md`, `estate/catalogue-dashboard.md`, `core-concepts/index.md`, `core-concepts/build-load-and-test.md`, `core-concepts/catalogue.md`. The parent re-read source for the cited findings in the complementary review.

Reference samples: `reference/ai-agents.md`, `reference/weaver-documents/table.md`, `reference/cli/load.md`; retained concept sample `core-concepts/weaver-documents.md`. Repository `AGENTS.md` and `PROSE.md` were reviewed. No product-site audit or general reference rewrite is included.
