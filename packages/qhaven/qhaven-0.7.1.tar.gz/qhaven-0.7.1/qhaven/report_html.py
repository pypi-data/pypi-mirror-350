# qhaven/report_html.py

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any, Dict, List

from jinja2 import Environment, select_autoescape

# ──────────────────── Jinja2 template ───────────────────────────
_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>QHaven Report</title>
  <style>
    body { font-family: sans-serif; margin: 2rem; }
    table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
    th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; }
    th { background: #004080; color: white; }
    tr:nth-child(even) { background: #f9f9f9; }
    tr:hover { background: #eef; cursor: pointer; }
  </style>
</head>
<body>
  <h1>QHaven Report</h1>
  <p><strong>Generated:</strong> {{ ts }} UTC</p>

  <table id="findings">
    <thead>
      <tr>
        <th>Severity</th>
        <th>File</th>
        <th>Line</th>
        <th>Algorithm</th>
        <th>Deadline</th>
        <th>Replacement</th>
      </tr>
    </thead>
    <tbody>
    {% for f in findings %}
      <tr data-idx="{{ loop.index0 }}">
        <td>{{ f.severity }}</td>
        <td>{{ f.file }}</td>
        <td>{{ f.line }}</td>
        <td>{{ f.algorithm }}</td>
        <td>{{ f.deadline }}</td>
        <td>{{ f.replacement }}</td>
      </tr>
    {% endfor %}
    </tbody>
  </table>

  <script>
    const fixes = {{ fixes|tojson }};
    document.querySelectorAll('#findings tbody tr').forEach(row => {
      row.addEventListener('click', () => {
        const idx = row.getAttribute('data-idx');
        const patch = fixes[idx] || '(no fix available)';
        alert(patch);
      });
    });
  </script>
</body>
</html>
"""

_env = Environment(autoescape=select_autoescape(["html", "xml"]))
HTML_TEMPLATE = _env.from_string(_HTML)


# ──────────────────── Renderer ───────────────────────────────────
def write_html(
    findings: List[Dict[str, Any]],
    fixes: Dict[int, str],
    out_path: Path
) -> None:
    """
    Render an interactive HTML report. Click any row to see the
    replacement code in an alert popup.
    """
    # sanitize findings: replace None with ""
    safe_findings = []
    for f in findings:
        clean: Dict[str, Any] = {}
        for k, v in f.items():
            clean[k] = "" if v is None else v
        safe_findings.append(clean)

    # ensure fixes is serializable
    safe_fixes = {i: ("" if fix is None else fix) for i, fix in fixes.items()}

    ts = datetime.datetime.utcnow().isoformat(timespec="seconds")
    rendered = HTML_TEMPLATE.render(ts=ts, findings=safe_findings, fixes=safe_fixes)
    out_path.write_text(rendered, encoding="utf-8")
