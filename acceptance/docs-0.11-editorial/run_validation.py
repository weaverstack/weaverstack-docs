"""Run local documentation checks and retain exact commands and output."""
from pathlib import Path
import json
import os
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
runtime, product = (Path(p).resolve() for p in sys.argv[1:3])
docs_python = root / '.venv/bin/python'
product_python = runtime / '.venv/bin/python'
env = dict(os.environ, WEAVER_CHECKOUT=str(runtime), PYTHONPATH=str(runtime / 'src'))
env['TMPDIR'] = '/Users/matthiaswong/.hermes/profiles/fors/cache/scratch'
commands = [[str(docs_python), '-m', 'mkdocs', 'build', '--strict']]
for name in ['cli', 'python', 'catalogue', 'semantic']:
    commands.append([str(product_python), f'tools/generate_{name}_reference.py', '--check', '--weaver-checkout', str(runtime)])
commands.append([str(product_python), 'tools/generate_dashboard_demo.py', '--check', '--weaver-checkout', str(product)])
for name in ['estate', 'reference', 'docs_refresh', 'journey']:
    command = [str(product_python), f'tools/check_{name}_examples.py', '--weaver-checkout', str(runtime)]
    if name == 'docs_refresh':
        command += ['--runtime-revision', 'efc046e7cf066daefd27f9268413ae05c3ed64e4']
    commands.append(command)
commands += [[str(docs_python), 'tools/check_item_routes.py', '--developer-site', 'site', '--product-site', str(product / 'docs')], [str(docs_python), 'tools/check_item_routes.py', '--self-test'], [str(docs_python), 'tools/test_item_route_assets.py']]
for name in ['cli', 'python', 'catalogue', 'semantic']:
    commands.append([str(docs_python), f'tools/test_generate_{name}_reference.py'])
commands += [[str(product_python), 'acceptance/docs-0.11-editorial/check_commands.py', str(runtime)], [str(product_python), 'acceptance/docs-0.11-editorial/reproduce_remote_mirror.py', str(runtime)], ['git', 'diff', '--check']]
results = []
for command in commands:
    result = subprocess.run(command, cwd=root, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    results.append({'command':command, 'returncode':result.returncode, 'output':result.stdout})
    (root / 'acceptance/docs-0.11-editorial/validation.json').write_text(json.dumps(results, indent=2) + '\n')
    print(result.returncode, ' '.join(command), flush=True)
    if result.returncode:
        print(result.stdout, flush=True)
print(f'{sum(r["returncode"] == 0 for r in results)}/{len(results)} checks passed')
sys.exit(any(r['returncode'] for r in results))
