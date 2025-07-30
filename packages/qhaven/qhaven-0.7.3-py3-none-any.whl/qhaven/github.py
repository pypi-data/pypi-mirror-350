from __future__ import annotations
import subprocess, requests
from pathlib import Path
from typing import List
API = "https://api.github.com"

def _run(cmd: List[str], cwd: Path):
    subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.DEVNULL)

def commit_stub(repo_path: Path, findings, branch: str):
    _run(["git", "checkout", "-b", branch], cwd=repo_path)
    for f in findings:
        fp = repo_path / f["file"]
        fp.write_text(fp.read_text() + f"\n// ⚠ QHaven: replace {f['algorithm']} with {f['replacement']}\n", "utf-8")
    _run(["git", "add", "-A"], cwd=repo_path)
    _run(["git", "commit", "-m", "QHaven stub patch"], cwd=repo_path)

def push(repo_path: Path, branch: str):
    _run(["git", "push", "-u", "origin", branch], cwd=repo_path)

def open_pr(owner, repo, branch, token, findings):
    url = f"{API}/repos/{owner}/{repo}/pulls"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    data = {"title": f"QHaven: stub PQC fixes for {findings} calls", "head": branch, "base": "main", "body": "Automated patch by QHaven"}
    r = requests.post(url, headers=headers, json=data, timeout=30)
    r.raise_for_status(); print("PR:", r.json()["html_url"])