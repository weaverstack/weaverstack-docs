# Developer journey fixes: D1–D7

Baseline: docs `36ad90f4dcb677d8c04285916af3ab86268b9cdf` on the current owning branch. Runtime evidence is the unchanged checkout `~/dev/weaverstack-editorial-runtime` at `efc046e7cf066daefd27f9268413ae05c3ed64e4`.

## Delivered

- D1: correct P-1001's first event depot from North to East in the installed Parcel Folder declaration. Explain preview selection, Build/Load/Test/Health, query the event history, and interpret why the latest status stays In transit / Central. No invented terminal capture or live-run claim.
- D2: turn Health findings into decisions: stale validation → Test; pending/stale load → Load then Test; edited definition → Check/Build; failure/inventory inconsistency → inspect/recover. Explain why processing success still needs authored business validation.
- D3: put Planning-only catch-up and validation before the deliberate two-team run. Preserve catalogue context, selector defaults, access/runtime requirements, publication waits and failure rules.
- D4: use required StatusEvent, not optional Reference.Service. Correct the earlier event locally; compare OperationsDev against source Operations and the unchanged borrowed LakehouseCurrentStatus branch. Preserve reset/materialisation/failure warnings and the separate cross-workspace path.
- D5: investigate Operations' connected items, follow an item into Orchestration, then distinguish last-run outcomes from Health findings. Generated demonstrations remain unchanged.
- D6: name the current-status and known-status questions before first-success validations. Native TMDL now explains why the deployed Delivery Count of 2 is a useful before/after check and links to repeatable validation.
- D7: Execute is inside the copyable standing instructions, including explicit development item/configuration, supported JSON/non-interactive flags, a read-only first query, mutation approval, permission boundaries and unknown-outcome handling.

## Source proof and limits

The focused checker copies frozen installed-example source into scratch, applies the exact published substitutions and parses the resulting connected project without dispatching a command. Only `Lakehouse/Landing/Files/Parcel.Events` and `Warehouse/Operations/Parcel.StatusEvent` change physical signatures. Dependency edges stay unchanged. CurrentStatus is a descendant of StatusEvent; LakehouseCurrentStatus is not. These relationships support the local/borrowed comparison; `src/weaver/build_bundle/incremental.py:222–289` classifies signature changes and propagates impact to selected descendants.

The original validations live in `src/weaver/fragments/examples/Parcel/{Lakehouse/Landing,Warehouse/Operations}/{tests,assumptions}/`. CurrentStatusMatches expects P-1001 In transit / Central and P-1002 Delivered / South. Known-status assumptions inspect Status, not the depot. A local SQLite relational oracle over the edited CSV confirms those two latest rows and the corrected East depot; this is not Spark/Fabric execution or proof of live installation. Frozen source bytes remain unchanged.

`developer-checks.json` retains exact commands and tool output. The focused checker verifies all nine changed pages, 95 local link destinations, every historical capture byte-for-byte against baseline, and four added command forms through `build_parser().parse_args` only. No CLI handler, Build preview, Load, Test, Execute or Fabric dispatch was run. The strict MkDocs build and `git diff --check` pass. The Material package emits its existing MkDocs 2 advisory, not a strict-build diagnostic.

No full `run_validation.py` batch, runtime/CI/VERSION changes, generated reference/capture changes, production/Fabric operations, or preview-server changes. Existing T05 workaround material is outside this diff and remains unchanged. Parent owns subsequent rendered/HTTP QA and push.
