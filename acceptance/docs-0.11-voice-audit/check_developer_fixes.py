"""Focused D1–D7 source/parser checks. No dispatch or service execution."""
import ast
import csv
import io
import json
from pathlib import Path
import re
import shlex
import shutil
import socket
import sqlite3
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = Path(sys.argv[1]).resolve()
PIN = 'efc046e7cf066daefd27f9268413ae05c3ed64e4'
BASE = '36ad90f4dcb677d8c04285916af3ab86268b9cdf'
assert subprocess.check_output(['git', '-C', str(RUNTIME), 'rev-parse', 'HEAD'], text=True).strip() == PIN
sys.path.insert(0, str(RUNTIME / 'src'))
sys.dont_write_bytecode = True

def blocked(*args, **kwargs):
    raise AssertionError('No network allowed')

socket.socket.connect = blocked
socket.create_connection = blocked
from weaver_cli.main import build_parser
from weaver.declaration import parse_item_repository
from weaver.locations import Location

pages = subprocess.check_output(['git', 'diff', BASE, '--name-only', '--', 'docs'], cwd=ROOT, text=True).splitlines()
assert len(pages) == 9, pages
commands = []
links = 0
for relative in pages:
    text = (ROOT / relative).read_text()
    before = subprocess.check_output(['git', 'show', f'{BASE}:{relative}'], cwd=ROOT, text=True)
    # Preservation, including every complete historical terminal capture.
    captures = r'<!-- cli-capture:.*?<!-- /cli-capture -->'
    assert re.findall(captures, text, re.S) == re.findall(captures, before, re.S), relative
    def bash_commands(content):
        return [line for block in re.findall(r'^```bash[^\n]*\n(.*?)^```', content, re.M | re.S)
                for line in block.replace('\\\n', ' ').splitlines() if line.startswith('weaver ')]
    old_commands = set(bash_commands(before))
    commands.extend(c for c in bash_commands(text) if c not in old_commands)
    for target in re.findall(r'\]\(([^)]+)\)', text):
        target = target.split()[0]
        if '://' in target or target.startswith('#'):
            continue
        assert (ROOT / relative).parent.joinpath(target.split('#')[0]).resolve().exists(), (relative, target)
        links += 1
agent = (ROOT / 'docs/reference/ai-agents.md').read_text()
template = re.search(r'^```markdown\n(.*?)^```', agent, re.M | re.S).group(1)
execute = re.search(r'`(weaver execute [^`]+)`', template).group(1)
commands.append(execute)
for command in sorted(set(commands)):
    build_parser().parse_args(shlex.split(command)[1:])
    print('PARSE ONLY:', command)
assert '--workspace-config workspace-config.dev.yml' in execute
assert 'unknown outcome' in template and 'Ask for approval before submitting SQL or Python' in template

fragment = RUNTIME / 'src/weaver/fragments/examples/Parcel'
with tempfile.TemporaryDirectory(prefix='voice-audit-') as temp:
    project = Path(temp)
    for kind in ('Lakehouse', 'Warehouse'):
        shutil.copytree(fragment / kind, project / kind)
    # Continue the installed example's separately named connection.
    connected = (ROOT / 'docs/estate/connected-items.md').read_text()
    sql_blocks = re.findall(r'^```sql[^\n]*\n(.*?)^```', connected, re.M | re.S)
    connection = next(b for b in sql_blocks if 'Table ID: Parcel.LakehouseCurrentStatus' in b)
    (project / 'Warehouse/Operations/Parcel.LakehouseCurrentStatus.sql').write_text(connection)
    yaml_blocks = re.findall(r'^```yaml[^\n]*\n(.*?)^```', connected, re.M | re.S)
    (project / 'Warehouse/Operations/shortcuts.yml').write_text(next(b for b in yaml_blocks if 'logical:' in b))
    original = parse_item_repository(Location(str(project)))
    paths = ['Lakehouse/Landing/Files/Parcel__Events.py', 'Warehouse/Operations/Parcel.StatusEvent.sql']
    for relative in paths:
        path = project / relative
        text = path.read_text()
        page = ROOT / ('docs/estate/development-cycle.md' if relative.endswith('.py') else 'docs/estate/mirror.md')
        language = 'csv' if relative.endswith('.py') else 'sql'
        snippets = re.findall(r'^```' + language + r'[^\n]*\n(.*?)^```', page.read_text(), re.M | re.S)
        old, new = (s.strip() for s in snippets[:2])
        assert text.count(old) == 1
        path.write_text(text.replace(old, new))
    changed = parse_item_repository(Location(str(project)))
    changed_sources = {str(identity) for identity, source in changed.source_documents.items()
                       if source.physical_signature != original.source_documents[identity].physical_signature}
    assert changed_sources == {'Lakehouse/Landing/Files/Parcel.Events', 'Warehouse/Operations/Parcel.StatusEvent'}, changed_sources
    descendants = set(changed.dependency_graph.descendants('Warehouse/Operations/Parcel.StatusEvent'))
    assert 'Warehouse/Operations/Parcel.CurrentStatus' in descendants
    assert 'Warehouse/Operations/Parcel.LakehouseCurrentStatus' not in descendants
    print('SOURCE signatures changed only:', sorted(changed_sources))
    print('MIRROR branch proof: CurrentStatus is a descendant; LakehouseCurrentStatus is unchanged and independent')
    edges = {(e.consumer.object_id.qualified, e.producer.object_id.qualified) for e in changed.dependency_edges}
    assert edges == {(e.consumer.object_id.qualified, e.producer.object_id.qualified) for e in original.dependency_edges}
    print('PARSED changed connected project; dependency edges:', sorted(edges))
    module = ast.parse((project / paths[0]).read_text())
    events = next(ast.literal_eval(n.value) for n in module.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'EVENTS' for t in n.targets))
    rows = list(csv.DictReader(io.StringIO(events)))
    assert rows[0]['Depot'] == 'East'
    assert all(r['Status'] in ('Accepted', 'In transit', 'Delivered') for r in rows)
    # A local relational oracle, not Spark/Fabric output or an Execute result.
    db = sqlite3.connect(':memory:')
    db.execute('create table events(parcel text, sequence int, status text, depot text)')
    db.executemany('insert into events values (?, ?, ?, ?)', [(r['Parcel ID'], int(r['Event sequence']), r['Status'], r['Depot']) for r in rows])
    latest = db.execute('with ranked as (select *, row_number() over (partition by parcel order by sequence desc) as n from events) select parcel, status, depot from ranked where n=1 order by parcel').fetchall()
    assert latest == [('P-1001', 'In transit', 'Central'), ('P-1002', 'Delivered', 'South')]
    print('LOCAL SQL oracle, not service execution: corrected first depot East; latest rows:', latest)
    warehouse = (project / paths[1]).read_text()
    assert "('P-1001', 1, 'Accepted', 'East')" in warehouse
    assert "('P-1001', 2, 'In transit', 'Central')" in warehouse
    assert (fragment / paths[0]).read_text() != (project / paths[0]).read_text()
    assert "P-1001,1,Accepted,North" in (fragment / paths[0]).read_text()
print(json.dumps({'changed_pages': len(pages), 'new_commands_parsed_only': len(set(commands)), 'local_links_checked': links, 'historical_captures': 'unchanged', 'network': 'blocked', 'runtime_dispatch': 'none'}, sort_keys=True))
