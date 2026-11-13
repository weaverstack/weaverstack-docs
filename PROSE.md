# Documentation prose

This guide governs public documentation in this repository. It complements the product-source prose guide; it does not redefine product behaviour.

## Default

Write for an engineer trying to complete a task, understand Weaver or look up an exact interface. Give enough context, reasons and examples to help the reader succeed. Put implementation design in the Weaver source repository and maintenance planning in root-level repository files.

## Principles

1. **State the current model.** Describe implemented behaviour directly. Do not document the cleaner product you wish existed.
2. **Use plain, public vocabulary.** Name Weaver documents, logical and physical items, the catalogue, operations and Fabric surfaces as users encounter them. Do not derive public categories from modules or classes.
3. **Give each page one job.** Getting started offers setup; item tasks produce one useful result; estate tasks coordinate working items; Reference owns exact interfaces and behaviour. Retained concept/deep-dive pages explain decisions at the point of use.
4. **Explain the work before directing it.** Introduce the subject, the relevant situation and what the example will help the reader understand. Within worked steps, give the action and its observable result. A list of operations is not an introduction.
5. **Put precision with its owner.** Link to Reference for syntax, defaults, selection, state transitions, outcomes and failure boundaries instead of repeating partial contracts.
6. **Define meaningful scope once.** Distinguish host-specific behaviour, examples and versioned interfaces where the distinction changes a decision. Describe the supported scope directly; keep review provenance in maintainer evidence.
7. **Prefer defaults and inference.** Examples should omit fields that merely restate defaults and should let Weaver infer dependencies where supported. Keep declarations required by current source.
8. **Keep examples small and neutral.** Use parcel and logistics names. Never publish production project, tenant, workspace or item identifiers.
9. **Keep the real constraint.** Succinctness must not remove destructive scope, ordering, rollback limits, partial-state consequences or the action needed to recover.
10. **Do not expose the maintenance process.** Public pages do not mention planned coverage, later phases, missing future pages or agent instructions.

## Explain, then guide

Begin guides with a recognisable situation: a failed load, a shared table, a development change or a release decision. Explain what the reader provides, what Weaver does and what happens next before introducing bindings, identities or persisted state. Continue a named example rather than restarting with an abstract taxonomy. Reference tables remain precise and economical.

Write as an experienced engineer explaining the work to another engineer. Reader-centred writing is not the same as directing the reader. An explanation develops a thought: how something behaves, why a distinction matters, or what makes one choice appropriate. It does not have to become a command to be useful.

Match the language to the passage:

- **Introductions** establish the subject and the purpose of the example. They need not list every operation or supply a motivational paragraph before every task.
- **Explanations** connect behaviour, reasons and consequences. A recommendation explains its reason rather than becoming a standing order.
- **Worked steps** give concrete instructions, complete commands or files, and expected observations. Imperatives are appropriate here.
- **Reference** describes exact inputs, effects, defaults and boundaries. It need not imitate a tutorial or a conversation.
- **Warnings** remain direct where security, data loss or state integrity depends on the reader's action. Copyable AI-agent briefs also deliberately give instructions.

For example, “Use an item-wide run by default” gives a rule. Explaining that an item-wide Load follows the installed item graph, whereas plain named Load does not automatically add or order dependencies, gives the reader a reason for that choice. The worked example can then instruct them to run the appropriate command.

Likewise, “Apply shared modelling standards” announces an exercise. Explaining that several models can share conventions while retaining local exceptions introduces the capability the exercise demonstrates. “Can this run use less simultaneous work? Add --concurrency 2” is still an instruction, not an explanation of concurrency.

Describe prerequisites as the starting state of the example and say what it adds. Repeated “Continue”, “Keep”, “Retain”, “Add only” and “Omit” can make a guide sound like constraints for an editing agent. Preserve an explicit instruction when a step could overwrite existing work; otherwise explain what is already present and what remains unchanged.

After a command, interpret its result. Name the relevant observation and what it establishes rather than merely telling the reader to “inspect the outcome” or “use the findings to decide”.

Name who acts where it matters. Prefer ordinary verbs and one relationship per sentence to nominalisations or compressed slash-separated concepts. Do not mechanically add pronouns, split every sentence or ban punctuation. Keep meaningful mechanisms rather than replacing them with assurances.

Put requirements beside the operation that needs them, with exact detail linked to Reference. Correct an overbroad sentence instead of appending a wall of caveats. Keep reset/deletion scope explicit at the action. Explain the division of responsibility: configuration chooses destinations, identity permissions control access and confirmation flags approve specific plans.

Support claims with source inspection, offline tests, historical captures or live measurements as appropriate. Give measurements their workload and timing context. Explain authored validations where readers need to check business rules. Preserve historical capture provenance; regenerate interfaces with their tools rather than editing generated facts.

## Match the surface

**Developer explanation.** Establish the work and explain the relevant behaviour before directing the reader through it. State requirements where they matter without making every paragraph a checklist. Keep clear warnings for destructive actions and real security or compatibility limits. Reference owns detailed semantics; maintainer evidence owns review history.

**Product copy is a different surface.** Product pages and organisational articles explain why capabilities matter and may invite the reader to act. Their imperatives are not automatically defects. Developer documentation teaches the work rather than carrying a promotional cadence into a manual. Both surfaces support claims with mechanisms or evidence.

**Enough explanation to teach.** Optimise guides for reader understanding and successful action, not maximum information density or minimum word count. Use named actors, reasons and examples where they help. Preserve concise passages that already work.

Source comments and CLI diagnostics have a narrower job. Comments preserve non-obvious invariants and engineering reasons. Help states an option’s effect; errors identify the condition, affected thing and known next action. Keep those surfaces concise rather than importing their brevity into explanatory guides.

## Language

Write as one senior engineer to another. Use direct sentences and concrete nouns. Support recommendations and benefits with mechanisms or evidence rather than unsupported adjectives such as “powerful”, “seamless”, “robust”, “safe”, “predictable” and “enterprise-grade”.

Do not use “current versions of Weaver” unless a real version distinction matters. Do not say readers “can rely on” a behaviour; define the behaviour or recorded state. Avoid history and arguments against hypothetical alternatives unless compatibility or migration depends on them.

Use `Weaver document` for authored Tables, Folders, Views, Tests, Assumptions, Shortcuts, Warehouse programmables and schema metadata. Do not introduce `resource` or `artefact` as a user-facing umbrella term.

## Reader model and motivation

Begin from Lakehouse, Warehouse, Semantic models or Reports. Within each item,
let one working outcome create the need for the next page. Tests are taught in
that item's context; exact common semantics remain in Reference. Shared mappings,
dependencies, state, recovery and tuning belong under Coordinate your estate.
Do not mistake placing existing pages in new groups for a connected journey.

Introduce normal TMDL first, then one useful built-in annotation in the native
model task. Shared policy follows naturally; custom Python and composition are
later model tasks. Overlays and annotations remain the model counterpart to SQL/
Python engineering declarations, explained in the retained document concept.

Weaver is Fabric-first. Present authoring tasks in the order Lakehouse, Warehouse,
semantic model, Report. Use Fabric before Power BI when naming the platforms.
Standalone Power BI deployment is a supported setup detail, not a separate
first-class product or the first numbered route.

Integrate semantic models and Reports into the ordinary project, Build, Load,
Test, Health, development and recovery flow. Each item has its own first-success route. Semantic-model extensions stay in
that item group rather than an unrelated Advanced hub. Native Power BI filenames,
selectors and format details retain their exact technical names in Reference.

Explain the reason for each capability in the task that benefits from it: one
configuration switches environments, one dependency graph orders source loads
and model refreshes, one Health report covers the managed estate. Let that
practical consequence carry the motivation. Do not add promotional adjectives,
repeated slogans or a paragraph about why the reader should be impressed.

Keep setup differences and consequential limits beside the relevant action.
Keep exhaustive exceptions and compatibility detail in Reference. Do not make
the opening of every task defend against hypothetical misunderstandings.

## Page types

### Getting started

Use one ordered route with complete commands or files and an expected result at each step. Keep theory, alternatives and exhaustive options out of the path.

### Item entrances and tasks

Keep overviews short: familiar work, effort removed, first useful task. Full
execution belongs to task pages, not duplicated miniature manuals in indexes.
A task has one start state, one useful result and one natural next task. Introduce
what the example demonstrates, then use complete runnable source and explain
what Weaver handled. Do not hide all
interesting depth behind setup or force every item to display every command.

### Coordinate your estate

Start with two working items and the practical need to connect, map or inspect
these together. Teach ordinary development before optional Mirror; keep destructive
scope beside the action. Link exact execution and failure rules to Reference.

### Retained concepts and deeper mechanisms

Keep complete explanations searchable and link them from the task that creates
the question. Stable URLs are useful; relocating everything is not a goal.

### Reference

Be economical, complete and searchable. Specify accepted syntax, defaults, precedence, selection, ordering, state changes, outcomes and failures where relevant. Include examples or explanations when they make the contract easier to use. Record exact compatibility boundaries alongside current machine representations.

## Examples and code

Code must be complete enough to run in the stated context. Give fenced blocks a language. Keep metadata inside complete SQL or Python source when that is how users author it.

Descriptive metadata remains descriptive; do not imply that a metadata reference creates an execution dependency. Use explicit `Dependencies` as an override where inference is supported, but preserve explicit declarations where current product rules require them.

## First success and progressive depth

Keep the current architecture. Begin from familiar Python, SQL or native Power BI work and explain the purpose of the first example. Its steps produce one working result; the accompanying explanation shows what Weaver handled and which question comes next. A senior voice is approachable and precise, not dry or exhaustive. Keep full contracts in Reference rather than making them an admission requirement.

State the project, required files and active configuration. Leave checkpoint maps, fixture variants, testing oracles and why examples are different in maintenance evidence; name a real source change plainly when the next task needs it. Keep actual permissions, trusted-code warnings and destructive scope at the action that depends on them.

Make passing validation the ordinary path. Put deliberate failures, diagnostic selectors and restoration exercises behind clearly optional exploration; retain safe restoration and operation-specific failure boundaries. Judge flow through complete rendered reader routes, not sentence/page counts or exact-sentence assertions.

## Review

For each changed passage, ask:

1. Which reader task, decision or lookup does this serve?
2. What source and test evidence supports each behavioural claim?
3. Is this the authoritative owner, or should it link elsewhere?
4. Did the edit blur specified behaviour, host behaviour, current output or an example?
5. Can anything be removed without losing a prerequisite, consequence or recovery action?

Then read the introduction and transitions continuously, without the command output. Does the prose develop understanding, or merely distribute assignments? Does it explain a recommendation's reason and interpret the example's result? Compare it with a relevant passage that already teaches well, such as the independent expected-result explanation in the Warehouse testing guide or the consumer-bookmark explanation in the Lakehouse incremental guide.

Do not judge voice by imperative counts, added pronouns, passive-voice substitutions or sentence length. Preserve concise explanations that work, direct procedural steps and meaningful warnings. A passing build, parser check or CI run verifies a different part of the work; it does not establish that the explanation reads well.
