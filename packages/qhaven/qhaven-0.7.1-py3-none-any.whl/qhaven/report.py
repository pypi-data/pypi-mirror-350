from __future__ import annotations
import json, datetime, html, textwrap, pkg_resources
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
)

__all__ = ["write_sarif", "write_pdf"]

def write_sarif(findings: list[dict], out: Path) -> None:
    rules, results = {}, []
    for f in findings:
        rid = f.get("algorithm", "Unknown-Algo")
        rules.setdefault(
            rid,
            {
                "id": rid,
                "name": rid,
                "shortDescription": {"text": rid},
                "fullDescription": {"text": f.get("replacement", "")},
                "helpUri": f.get("sample_url", ""),
                "properties": {"tags": [f.get("cwe", "CWE-327")]},
            },
        )
        results.append(
            {
                "ruleId": rid,
                "level": "error" if f.get("severity", "medium") == "high" else "warning",
                "message": {"text": f"{rid} disallowed by {f.get('deadline', '-')}"},  
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": f.get("file", "<no-file>")},
                            "region": {
                                "startLine": f.get("line", 1),
                                "startColumn": f.get("column", 1),
                            },
                        }
                    }
                ],
            }
        )

    sarif = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "QHaven",
                        "version": pkg_resources.get_distribution("qhaven").version,
                        "rules": list(rules.values()),
                    }
                },
                "invocation": {
                    "executionSuccessful": True,
                    "endTimeUtc": datetime.datetime.utcnow().isoformat(timespec='seconds') + "Z",
                },
                "results": results,
            }
        ],
    }
    out.write_text(json.dumps(sarif, indent=2))


def write_pdf(findings: list[dict], out: Path) -> None:
    styles = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=styles["Normal"], fontSize=9, leading=11)

    doc = SimpleDocTemplate(
        str(out),
        pagesize=landscape(A4),
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        title="QHaven Post-Quantum Inventory",
    )

    # cover page
    story = [
        Paragraph("<font size=26><b>QHaven</b></font>", styles["Title"]),
        Spacer(1, 4 * mm),
        Paragraph("<font size=14>Post-Quantum Cryptographic Inventory</font>", styles["Heading2"]),
        Spacer(1, 16 * mm),
        Paragraph(f"<b>Scan time (UTC):</b> {datetime.datetime.utcnow().isoformat(timespec='seconds')}Z", body),
        Spacer(1, 4 * mm),
        Paragraph(f"<b>Total findings:</b> {len(findings)}", body),
        Spacer(1, 10 * mm),
        Paragraph("<b>Severity legend</b>", styles["Heading3"]),
        Table(
            [["High", "Medium", "Low"]],
            colWidths=[30 * mm] * 3,
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), colors.salmon),
                    ("BACKGROUND", (1, 0), (1, 0), colors.lightgoldenrodyellow),
                    ("BACKGROUND", (2, 0), (2, 0), colors.whitesmoke),
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.grey),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ]
            ),
        ),
        PageBreak(),
    ]

    wrap = lambda t: "<br/>".join(textwrap.wrap(html.escape(t), width=60)) or t
    rows = [
        ["Severity", "File (relative)", "Line", "Algorithm", "Deadline", "Recommendation"]
    ] + [
        [
            f.get("severity", "medium"),
            wrap(f.get("file", "")),
            f.get("line", 1),
            f.get("algorithm", ""),
            f.get("deadline", ""),
            wrap(f.get("replacement", "")),
        ]
        for f in findings
    ]

    tbl = Table(rows, colWidths=[25*mm, 95*mm, 12*mm, 35*mm, 28*mm, 60*mm], repeatRows=1, splitByRow=True)

    header_style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#222831")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
    ]
    sev_bg = {"high": colors.salmon, "medium": colors.lightgoldenrodyellow, "low": colors.whitesmoke}
    for idx, f in enumerate(findings, start=1):
        header_style.append(("BACKGROUND", (0, idx), (-1, idx), sev_bg.get(f.get("severity", "medium"))))
    tbl.setStyle(TableStyle(header_style))

    story.append(tbl)
    doc.build(story, onLaterPages=_footer)


def _footer(canvas, _):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(285 * mm, 10 * mm, f"Page {canvas.getPageNumber()}")
    canvas.restoreState()
