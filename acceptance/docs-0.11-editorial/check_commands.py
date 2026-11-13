"""Parse complete CLI examples without invoking handlers or Fabric."""
from pathlib import Path
import argparse
import re
import shlex
import sys

runtime = Path(sys.argv[1]).resolve()
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(runtime / 'src'))
from weaver_cli.main import build_parser
parser = build_parser()
files = [root / 'docs/reference/ai-agents.md']
files += [root / p for p in __import__('subprocess').check_output(['git', 'diff', '--name-only', '3239dd004c52327c1319a0275c49ae6bacc9336c'], cwd=root, text=True).splitlines() if p.startswith('docs/') and p.endswith('.md')]
commands = []
for path in sorted(set(files)):
    text = path.read_text()
    # Generated signatures are syntax inventories, not commands to execute.
    text = re.sub(r'<!-- BEGIN GENERATED.*?<!-- END GENERATED.*?-->', '', text, flags=re.S)
    for block in re.findall(r'```(?:bash|sh)\n(.*?)```', text, re.S):
        for line in block.replace('\\\n', ' ').splitlines():
            if line.strip().startswith('weaver ') and '<command>' not in line:
                commands.append((path.relative_to(root).as_posix(), line.strip()))
    if path.name == 'ai-agents.md':
        for command in re.findall(r'`(weaver [^`]+)`', text):
            # Bare command names in prose are links/references, not invocations.
            if command not in {'weaver execute'}:
                commands.append((path.relative_to(root).as_posix(), command))
for path, command in commands:
    if '<command>' in command:
        continue  # Explicit syntax placeholder, not a runnable example.
    try:
        parser.parse_args(shlex.split(command)[1:])
    except SystemExit as exc:
        if exc.code != 0:
            raise
print(f'PASS: {len(commands)} complete CLI examples parsed from {len(set(p for p,c in commands))} pages; no handlers executed.')
# Guard the exceptions explicitly rather than promoting universal flag rules.
for command in ['check --workspace-config workspace-config.dev.yml', 'workflow verify --json']:
    try:
        parser.parse_args(shlex.split(command))
    except SystemExit as exc:
        assert exc.code == 2
    else:
        raise AssertionError(command)
print('PASS: check rejects workspace-config and workflow rejects json.')
