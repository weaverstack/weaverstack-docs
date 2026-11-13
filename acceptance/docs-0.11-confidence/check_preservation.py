"""Verify this prose pass preserves executable blocks and retained evidence."""
from pathlib import Path
import json
import re
import subprocess

root = Path(__file__).resolve().parents[2]
base = "83e3252c5371175e33f9862980747ad22ba297a4"
files = subprocess.check_output(
    ["git", "diff", "--name-only", base], cwd=root, text=True
).splitlines()
patterns = {
    "shell_blocks": r"```(?:bash|sh)[^\n]*\n.*?```",
    "historical_captures": r"<!-- cli-capture:.*?<!-- /cli-capture -->",
    "generated_sections": r"<!-- BEGIN GENERATED.*?<!-- END GENERATED.*?-->",
}
results = []
for name in files:
    if not name.startswith("docs/") or not name.endswith(".md"):
        continue
    before = subprocess.check_output(["git", "show", f"{base}:{name}"], cwd=root, text=True)
    after = (root / name).read_text()
    results.append({"file": name, **{
        label: re.findall(pattern, before, re.S) == re.findall(pattern, after, re.S)
        for label, pattern in patterns.items()
    }})
assert results
assert all(all(value for key, value in row.items() if key != "file") for row in results), results
output = root / "acceptance/docs-0.11-confidence/preservation.json"
output.write_text(json.dumps(results, indent=2) + "\n")
print(f"PASS: {len(results)} changed public pages preserve exact shell blocks, historical CLI captures and generated sections.")
