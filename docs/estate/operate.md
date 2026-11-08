# Run and inspect an estate

After changing a project or repairing a source problem, use Health to see which work needs attention. Build installs your source changes; Load processes data and refreshes models; Test runs the installed validations. Check Health again after the work completes.

Keep the project from the [development loop](development-cycle.md). The Landing/Operations commands below use `workspace-development.yml`. If you added [source-backed models](../semantic-models/managed-sources.md), retain their targets in this same configuration. Run from the same project root throughout.

## 1. Inspect the starting state

```bash
weaver health --workspace-config workspace-development.yml
```

Without an item selector, Health covers the whole installed estate. It is read-only and reports Load, Tests and Build state as Green, Amber or Red, naming findings that need attention. By default it also compares installed claims with physical inventory.

Read the named finding before choosing a command:

- If a source has loaded since its validation last passed, rerun Test. The old pass has not checked the new data.
- If Load work is pending or stale, use the catch-up Load below, then Test the result.
- If you edited a project definition, Check and Build it first; Load and catalogue-mode Test still use the installed definition.
- If a load failed or installed objects are missing or inconsistent, inspect the failed step or inventory finding and follow [Recovery](recovery.md). Repeating Test will not repair that state.

For example, `Parcel.CurrentStatusMatches` becoming Amber after a successful StatusEvent Load calls for validation, not another source load.

For changed definitions, [Check, preview and Build](development-cycle.md) before this installed-state sequence. Source-data and model/Report definitions require separate Build calls. Reports participate in Build only; they have no independent Load or Test.

## 2. Run installed data work

For the normal item-wide run:

```bash
weaver load --workspace-config workspace-development.yml
```

Load selects the installed Table and Folder work and registered semantic-model refreshes. Managed dependencies order selected source work before model refreshes. Reports use the model’s data rather than having their own Load. Load uses the definitions and destinations installed in the catalogue. After editing project files, run Build before loading them.

For routine catch-up after Build or when Health reports pending or stale load work, narrow the run to non-Green loadable objects:

```bash
weaver load --stale --workspace-config workspace-development.yml
```

`--stale` uses the same Load-health assessment as Health. It preserves dependency ordering among selected item-wide work but does not pull Green upstream work into the run. An empty stale selection succeeds without changing the estate.

Completed changes remain in place when a run fails. Inspect the failed steps for partial changes, correct the cause, then use [Recover failed work](recovery.md) to rerun the work that needs attention.

## 3. Run installed validations

```bash
weaver test --workspace-config workspace-development.yml
```

A successful Load tells you that processing completed, not that the data meets your rules. In Parcel, the installed Tests compare current statuses with independently expected rows; the Assumptions look for unrecognised event statuses. A failed validation found a discrepancy or violation. A validation that could not run is an execution problem: inspect its error before changing the rule.

Health includes these recorded results alongside load and deployment findings. Author rules in the relevant [Lakehouse](../lakehouse/tests.md), [Warehouse](../warehouse/tests.md) or [model validation task](../semantic-models/validation.md). Test supports Python/Spark SQL, Warehouse SQL and semantic-model DAX; a model-owned Test can also compare a measure with an independent source SQL calculation. Build installs edited rules before catalogue-mode Test uses them. Source/file mode lets you check authored validations separately without recording catalogue status or history.

## 4. Inspect the resulting state

```bash
weaver health --workspace-config workspace-development.yml
```

Green means the assessed Load, Tests and Build subjects have no current finding. Amber identifies work that is pending, stale or otherwise needs attention without a current failure. Red identifies a recorded failure or inconsistent installed state. Act on the finding rather than the overall colour alone.

To operate only the Parcel items when the Catalogue also contains other projects, give the same scope to Load, Test and Health:

```bash
weaver load Lakehouse/Landing Warehouse/Operations --workspace-config workspace-development.yml
weaver test Lakehouse/Landing Warehouse/Operations --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "54-estate-test", "title": "Test · both sides of the Parcel connection"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Test · both sides of the Parcel connection">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Test

  Read catalogue                                                                                           2.7s
Workspace  Parcel Development
Catalogue  Warehouse/Catalogue
Targets
  Lakehouse/Landing
  Warehouse/Operations

  Build run graph                                                                                          0.0s
  Wait for Spark session                                                                                  35.8s
→   Test Lakehouse/Landing/Parcel.CurrentStatusMatches
→   Test Lakehouse/Landing/Parcel.EventStatusIsKnown
→   Test Warehouse/Operations/Parcel.CurrentStatusMatches
→   Test Warehouse/Operations/Parcel.StatusIsKnown
<span class="terminal-status-green">✓   Test Warehouse/Operations/Parcel.StatusIsKnown                                                         1.9s</span>
<span class="terminal-status-green">✓   Test Warehouse/Operations/Parcel.CurrentStatusMatches                                                  5.5s</span>
<span class="terminal-status-green">✓   Test Lakehouse/Landing/Parcel.EventStatusIsKnown                                                      12.7s</span>
<span class="terminal-status-green">✓   Test Lakehouse/Landing/Parcel.CurrentStatusMatches                                                    14.7s</span>
  Execute                                                                                                 12.8s
  Record what the run did                                                                                  0.0s
<span class="terminal-status-green">✓ Test                                                                                                    59.9s</span>

<span class="terminal-status-green">test passed</span>

Test summary
<span class="terminal-status-green">    4 passed</span>
    0 failed
  Workflow: 05dc2c23a84c45899e318715a6a41a54
</code></pre>
</figure>
<!-- /cli-capture -->

```bash
weaver health --item Lakehouse/Landing --item Warehouse/Operations --workspace-config workspace-development.yml
```

<!-- cli-capture: {"id": "56-scoped-estate-health", "title": "Health · Parcel estate after validation"} -->
<p class="terminal-intro">The command returned:</p>
<figure class="weaver-terminal" aria-label="Health · Parcel estate after validation">
<figcaption>Terminal output <span class="terminal-exit">exit 0</span></figcaption>
<pre tabindex="0" aria-label="Terminal output"><code>Health

  Read catalogue                                                                                           2.6s
  Check installed items                                                                                    0.1s
  Read installed objects                                                                                   3.0s
<span class="terminal-status-green">✓ Health                                                                                                   5.8s</span>

<span class="terminal-status-green">Weaver Health  Green</span>

<span class="terminal-status-green">Load    Green</span>
  Last load activity   0h 3m ago
<span class="terminal-status-green">  8 succeeded</span>

<span class="terminal-status-green">Tests   Green</span>
<span class="terminal-status-green">  4 succeeded</span>

<span class="terminal-status-green">Build   Green</span>
  Installed estate consistent (29 objects)

Slowest loads
  Lakehouse/Landing/Tables/Parcel.Event          12.8s
  Lakehouse/Landing/Tables/Parcel.CurrentStatus  7.6s
  Warehouse/Operations/Parcel.StatusEvent        5.0s
  Warehouse/Operations/Parcel.LiveStatus         5.0s
  Lakehouse/Landing/Files/Parcel.StatusFiles     2.9s

Largest changes
  Warehouse/Operations/Parcel.LakehouseCurrentStatus  read 2  +2 ~0 -0 !0
</code></pre>
</figure>
<!-- /cli-capture -->

For a complete source-and-model example, follow [Connect a semantic model to source data](../semantic-models/managed-sources.md).

Use [Troubleshooting](../basics/troubleshooting.md) when the final report is not Green. If an item-wide run is broader than the intended work, [run part of an estate](selective-runs.md). To cap simultaneous scheduled work for one invocation, [control concurrency](concurrency.md). Both are optional controls, not prerequisites for normal operation. See [Operation behaviour](../reference/operation-behaviour/index.md) and the [CLI reference](../reference/cli.md) for selection, freshness, inventory controls, named execution and machine-readable output.
