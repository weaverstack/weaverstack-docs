# T05: remote mirrored catalogue cannot resolve its source in joined Health

Status: confirmed at runtime `efc046e7cf066daefd27f9268413ae05c3ed64e4`. Not fixed. No runtime source or tests changed.

## Path and consequence

1. `src/weaver/operations/joined.py:85–108`, `place_workspace()`, retains the working workspace's `mirror` but explicitly sets `mirror=None` for another workspace.
2. `src/weaver/operations/health.py:148–184`, `_read()`, reads the catalogue, sees live borrowed objects, then calls `mirrored_source()` with that place's workspace configuration.
3. `src/weaver/operations/mirror.py:792–815`, `mirrored_source()`, raises `CommandError` when the catalogue has mirrors but the configuration has no `mirror` source. Copied LoadStatus is deliberately not treated as current.
4. Joined Health reads each place before constructing the joined assessment (`health.py:301–365`). The failed read becomes `Unread`; providing production as another `--catalogue` does not restore the missing configuration or cause this source resolver to use the other place.
5. The report is incomplete and the unavailable catalogue counts at least Amber. This is not evidence that the remote mirror is current.

## Local reproduction

```bash
/Users/matthiaswong/dev/weaverstack-editorial-runtime/.venv/bin/python \
  acceptance/docs-0.11-editorial/reproduce_remote_mirror.py \
  /Users/matthiaswong/dev/weaverstack-editorial-runtime
```

Actual result:

```text
CONFIRMED: remote place clears mirror; Health._read refuses: health needs the source catalogue for mirrored objects. Set mirror: Warehouse/<name> in workspace configuration.
PASS: working mirror configuration resolves source; remote configuration does not. Offline read boundaries only.
```

The probe uses the runtime's existing borrowed-catalogue representation fixture, a TestSession, and patched catalogue read boundaries. It exercises real workspace resolution and `_read()`/`mirrored_source()` logic. It is not a Fabric test, a Mirror deployment, or an end-to-end joined CLI rerun. The effect of supplying production separately is established by the joined read/control-flow trace above, not a new live experiment.

Related unmodified runtime tests passed: `tests/targeted/test_joined_health_representation.py`, `tests/targeted/test_health_operation_boundary.py`, `tests/test_mirror_plan_boundary.py` (61 tests). The expanded focused suite recorded in the implementation report passed 296 tests.

## Supported invocation and documentation

Assess a mirror from its own working workspace configuration with its `mirror:` source retained. For multiple mirrors, assess each from its own configuration. A source in another workspace is supported on that path; it is not universally rejected.

`docs/reference/operation-behaviour/health.md#remote-mirrored-catalogues` now explains this invocation and the incomplete-report consequence. No general cross-catalogue introduction is burdened with a misleading universal limitation. Runtime correction requires separate authorisation and regression tests; documentation sign-off does not close the defect.
