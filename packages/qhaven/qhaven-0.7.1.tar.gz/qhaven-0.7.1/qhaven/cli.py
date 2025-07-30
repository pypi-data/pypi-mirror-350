# qhaven/cli.py
from __future__ import annotations

import argparse
import datetime
import json
import os
from pathlib import Path
from typing import Dict

from .rules        import load_rules
from .scanner      import scan_repo
from .report       import write_pdf, write_sarif
from .report_html  import write_html
from .report_cbom  import write_cbom

# ─────────────────────── Config loader ────────────────────────
def load_cfg(path: str | Path) -> Dict[str, str]:
    """
    Load metadata from JSON, falling back to env vars or empty strings.
    """
    data: Dict[str, str] = {}
    p = Path(path)
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8")) or {}
        except json.JSONDecodeError:
            print(f"⚠️  could not parse metadata file {p}, using defaults/env")
    # Overlay environment variables
    for key in ("fisma_id","fips199","vendor_type","operating_system","hosting","hva_id"):
        env = os.getenv(f"QHAVEN_{key.upper()}")
        if env:
            data[key] = env
    return data

# ───────────────────── Evidence writer ───────────────────────
def write_evidence(
    findings: list[Dict],
    meta: Dict[str, str],
    out_dir: Path
) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    # inventory.json
    (out_dir / "inventory.json").write_text(json.dumps(findings, indent=2))
    # summary.md
    rows = "\n".join(
        f"| {f['severity']} | {f['file']} | {f['line']} | "
        f"{f['algorithm']} | {f['deadline']} | {f['replacement']} |"
        for f in findings
    )
    summary = (
        "# QHaven Report\n"
        f"Generated: {datetime.datetime.utcnow().isoformat(timespec='seconds')} UTC\n\n"
        "| Severity | File | Line | Algorithm | Deadline | Replacement |\n"
        "|----------|------|------|-----------|----------|-------------|\n"
        f"{rows}\n"
    )
    (out_dir / "summary.md").write_text(summary)
    # other formats
    write_pdf(findings,        out_dir / "qhaven.pdf")
    write_sarif(findings,      out_dir / "qhaven.sarif")
    fixes = {i: f["replacement"] for i, f in enumerate(findings)}
    write_html(findings, fixes, out_dir / "qhaven.html")
    write_cbom(findings, meta, out_dir / "qhaven.cbom.json")
    # metadata template
    meta_file = out_dir / "qhaven.cfg"
    meta_file.write_text(json.dumps(meta, indent=2))
    print(f"📝 Metadata template written to {meta_file}")

# ────────────────────────── CLI ──────────────────────────────
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="qhaven",
        description="QHaven: scan a repo for deprecated PQC usage and emit reports."
    )
    sub = p.add_subparsers(dest="command", required=True)
    # scan subcommand
    scan = sub.add_parser("scan", help="Scan a repository and generate evidence")
    scan.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="Path to the repo root (default: current directory)"
    )
    scan.add_argument(
        "--cfg",
        default="qhaven.cfg",
        help="Metadata file to load (default: qhaven.cfg)"
    )
    scan.add_argument(
        "--include-deps",
        action="store_true",
        help="Also scan .venv and site-packages"
    )
    scan.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed scan progress"
    )
    scan.add_argument(
        "--no-cache",
        action="store_true",
        help="Ignore cache and scan all files"
    )
    # metadata override flags
    scan.add_argument("--fisma-id",        help="FISMA ID (e.g. SYS-02468)")
    scan.add_argument("--fips199",         help="FIPS-199 level (Low|Moderate|High)")
    scan.add_argument("--vendor-type",     help="Vendor type (COTS|Custom|Contractor)")
    scan.add_argument("--operating-system",help="Operating system (e.g. RHEL 8.9)")
    scan.add_argument("--hosting",         help="Hosting environment (e.g. AWS-GovCloud)")
    scan.add_argument("--hva-id",          help="HVA ID (optional)")
    return p

def main() -> None:
    args = build_parser().parse_args()

    if args.command == "scan":
        root    = Path(args.repo).resolve()
        out_dir = root / "qhaven-evidence"

        # load and override metadata
        meta  = load_cfg(args.cfg)
        for key in ("fisma_id","fips199","vendor_type","operating_system","hosting","hva_id"):
            val = getattr(args, key)
            if val:
                meta[key] = val

        # load rules and scan
        rules = load_rules()
        print(f"🔍 Loaded {len(rules)} rules; scanning {root}")
        findings = scan_repo(
            root=root,
            rules=rules,
            include_deps=args.include_deps,
            ignore_paths={out_dir},
            verbose=args.verbose,
            no_cache=args.no_cache,
        )

        write_evidence(findings, meta, out_dir)
        print(f"✅ {len(findings)} findings  |  evidence in {out_dir}")

if __name__ == "__main__":
    main()
