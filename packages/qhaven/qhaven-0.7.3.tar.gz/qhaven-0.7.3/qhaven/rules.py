from __future__ import annotations
import json, re
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import List

@dataclass(slots=True)
class Rule:
    name: str
    pattern: str
    deadline: str
    replacement: str
    sample_url: str
    cwe: str
    severity: str
    re_obj: re.Pattern[str]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            name=d["name"],
            pattern=d["pattern"],
            deadline=d["deadline"],
            replacement=d["replacement"],
            sample_url=d.get("sample_url", ""),
            cwe=d.get("cwe", "CWE-327"),
            severity=d.get("severity", "medium"),
            re_obj=re.compile(d["pattern"], re.IGNORECASE | re.MULTILINE),
        )

_DEFAULT_JSON = resources.files("qhaven.assets").joinpath("cnsa2.json")

def load_rules(path: str | Path | None = None) -> List[Rule]:
    p = Path(path) if path else Path(_DEFAULT_JSON)
    data = json.loads(p.read_text())
    return [Rule.from_dict(item) for item in data]
