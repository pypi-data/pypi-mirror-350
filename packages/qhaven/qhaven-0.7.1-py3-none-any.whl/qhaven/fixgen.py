from __future__ import annotations
import hashlib, json, os, time
from pathlib import Path
from typing import List

import openai
from .rules import Rule

# pick up key from env var OPENAI_API_KEY
openai.api_key = os.getenv("OPENAI_API_KEY", "")

CACHE_PATH = Path("qhaven-fixes.json")
if CACHE_PATH.exists():
    _CACHE = json.loads(CACHE_PATH.read_text())
else:
    _CACHE = {}

def _save():
    CACHE_PATH.write_text(json.dumps(_CACHE, indent=2))

_SYS_MSG = (
    "You are a senior cryptographer. Respond ONLY with valid {lang} "
    "code that replaces the classical algorithm with {replacement} "
    "from the Open Quantum Safe liboqs or its bindings. Keep the snippet "
    "minimal and compile‑ready."
)

def build_messages(snippet: str, algo: str, rule: Rule, lang: str):
    return [
        {"role": "system", "content": _SYS_MSG.format(lang=lang, replacement=rule.replacement)},
        {"role": "user", "content": (
            f"Replace the {algo} usage in the following {lang} snippet with "
            f"the post‑quantum alternative.\n\n```{lang}\n{snippet}\n```" )},
    ]

def get_fix(snippet: str, algo: str, rule: Rule, lang: str) -> str:
    key = hashlib.sha256(f"{lang}|{algo}|{snippet}".encode()).hexdigest()
    if key in _CACHE:
        return _CACHE[key]

    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini", temperature=0,
        messages=build_messages(snippet, algo, rule, lang)
    )
    code = resp.choices[0].message.content.strip().strip("`")
    _CACHE[key] = code
    _save()
    time.sleep(1)  # be nice to the rate‑limit
    return code