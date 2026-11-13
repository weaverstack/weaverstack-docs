"""Offline T05 representation probe; no Fabric, runtime edits or credentials."""
from pathlib import Path
import importlib
import sys
from unittest.mock import patch

runtime = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(runtime / 'src'), str(runtime / 'tests'), str(runtime / 'tests/targeted')]
from support.workspaces import given_workspace
from weaver.operations.joined import place_workspace
from weaver.sessions.testing import TestSession
from weaver.errors import CommandError
from test_health_operation_boundary import _forked

health = importlib.import_module('weaver.operations.health')
source_rows = _forked()
borrowed = _forked('Customer')
home = given_workspace(mirror='Prod/Warehouse/Weaver')
local = place_workspace(home, home.workspace, 'WeaverDev')
remote = place_workspace(home, 'RemoteDev', 'WeaverDev')
assert local.mirror is not None and remote.mirror is None
session = TestSession(workspace=home)
with patch('weaver.catalogue.connection.catalogue_connection', return_value=object()), patch('weaver.catalogue.state.read_installed_catalogue', return_value=borrowed), patch('weaver.catalogue.state.catalogue_for', return_value=source_rows) as fetch_source:
    _, source = health._read(session, local, steps=False)
    assert source is source_rows
    assert fetch_source.call_count == 1
    try:
        health._read(session, remote, steps=False)
    except CommandError as exc:
        assert 'source catalogue for mirrored objects' in str(exc)
        print('CONFIRMED: remote place clears mirror; Health._read refuses:', exc)
    else:
        raise AssertionError('Expected remote mirror resolution to fail')
    assert fetch_source.call_count == 1
print('PASS: working mirror configuration resolves source; remote configuration does not. Offline read boundaries only.')
