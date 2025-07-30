# qhaven/scanner.py
from __future__ import annotations

import ast
import hashlib
import sqlite3
from concurrent.futures import ProcessPoolExecutor
from fnmatch import fnmatch
from pathlib import Path
from typing import List, Set
from tqdm import tqdm

from .rules import Rule

EXCLUDE_NAMES = {".git", ".venv", "site-packages", "node_modules", "vendor", "__pycache__"}
MAX_SIZE = 5 * 1024 * 1024  # 5 MB
CACHE_DB = ".qhaven_cache.db"
IGNORE_FILE = ".qhavenignore"

def _load_ignore_patterns(root: Path) -> List[str]:
    ignore_path = root / IGNORE_FILE
    if not ignore_path.exists():
        return []
    return [
        line.strip()
        for line in ignore_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

def _compute_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def _init_cache(db_path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(str(db_path))
    conn.execute(
        "CREATE TABLE IF NOT EXISTS files (path TEXT PRIMARY KEY, hash TEXT NOT NULL)"
    )
    return conn

def _should_scan(
    path: Path,
    root: Path,
    patterns: List[str],
    exclude_names: Set[str],
    include_deps: bool,
    ignore_paths: Set[Path],
) -> bool:
    if any(path.is_relative_to(ig) for ig in ignore_paths):
        return False
    names = exclude_names - ({"site-packages", ".venv"} if include_deps else set())
    if any(part in names for part in path.parts):
        return False
    if path.stat().st_size > MAX_SIZE:
        return False
    rel = str(path.relative_to(root))
    if any(fnmatch(rel, pat) for pat in patterns):
        return False
    return True

def _scan_file(args: tuple[Path, Path, List[Rule]]) -> List[dict]:
    path, root, rules = args
    data = path.read_bytes()
    if b"\x00" in data:
        return []
    text = data.decode("utf-8", errors="ignore")

    findings: list[dict] = []
    for rule in rules:
        for m in rule.re_obj.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            col = m.start() - text.rfind("\n", 0, m.start())
            findings.append({
                "file": str(path.relative_to(root)),
                "line": line,
                "column": col,
                "algorithm": rule.name,
                "deadline": rule.deadline,
                "replacement": rule.replacement,
                "sample_url": rule.sample_url,
                "severity": rule.severity,
                "cwe": rule.cwe,
            })

    try:
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for alias in getattr(node, "names", []):
                    for rule in rules:
                        if alias.name.lower().startswith(rule.name.lower()):
                            findings.append({
                                "file": str(path.relative_to(root)),
                                "line": node.lineno,
                                "column": 0,
                                "algorithm": rule.name,
                                "deadline": rule.deadline,
                                "replacement": rule.replacement,
                                "sample_url": rule.sample_url,
                                "severity": rule.severity,
                                "cwe": rule.cwe,
                            })
    except (SyntaxError, ValueError):
        pass
    return findings

def scan_repo(
    root: str | Path,
    rules: List[Rule],
    include_deps: bool = False,
    ignore_paths: Set[Path] | None = None,
    verbose: bool = False,
    no_cache: bool = False,
) -> List[dict]:
    root = Path(root).resolve()
    ignore_paths = {p.resolve() for p in (ignore_paths or set())}
    patterns = _load_ignore_patterns(root)

    files = [p for p in root.rglob("*") if p.is_file()]
    to_scan: List[Path] = []

    if no_cache:
        to_scan = [
            p for p in files
            if _should_scan(p, root, patterns, EXCLUDE_NAMES, include_deps, ignore_paths)
        ]
    else:
        conn = _init_cache(root / CACHE_DB)
        for p in files:
            if not _should_scan(p, root, patterns, EXCLUDE_NAMES, include_deps, ignore_paths):
                continue
            h = _compute_hash(p)
            row = conn.execute("SELECT hash FROM files WHERE path=?", (str(p),)).fetchone()
            if row is None or row[0] != h:
                to_scan.append(p)
            conn.execute("REPLACE INTO files (path, hash) VALUES (?,?)", (str(p), h))
        conn.commit()
        conn.close()

    findings: List[dict] = []
    tasks = [(p, root, rules) for p in to_scan]
    with ProcessPoolExecutor() as pool:
        for result in tqdm(pool.map(_scan_file, tasks), total=len(tasks), desc="Scanning", unit="file"):
            findings.extend(result)

    seen: Set[tuple] = set()
    unique: List[dict] = []
    for f in findings:
        key = (f["file"], f["line"], f["algorithm"])
        if key in seen:
            continue
        seen.add(key)
        unique.append(f)

    return unique
