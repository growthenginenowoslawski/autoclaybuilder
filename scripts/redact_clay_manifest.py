#!/usr/bin/env python3
"""Redact credential-shaped values from Clay JSON artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


SENSITIVE_KEY_RE = re.compile(
    r"(cookie|authorization|bearer|token|api[_-]?key|apikey|secret|password|passwd|private[_-]?key|session|webhook|slack|google[_-]?sheet)",
    re.IGNORECASE,
)

SENSITIVE_VALUE_RE = re.compile(
    r"(Bearer\s+[A-Za-z0-9._\-]+|sk-[A-Za-z0-9._\-]+|eyJ[A-Za-z0-9._\-]+|xox[baprs]-[A-Za-z0-9._\-]+|https://hooks\.slack\.com/\S+)",
    re.IGNORECASE,
)


def stable_redaction(value: Any) -> str:
    digest = hashlib.sha256(str(value).encode("utf-8", errors="replace")).hexdigest()[:12]
    return f"<redacted:{digest}>"


def redact(value: Any, parent_key: str = "") -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, child in value.items():
            if SENSITIVE_KEY_RE.search(str(key)):
                redacted[key] = stable_redaction(child)
            else:
                redacted[key] = redact(child, str(key))
        return redacted

    if isinstance(value, list):
        return [redact(item, parent_key) for item in value]

    if isinstance(value, str):
        if SENSITIVE_KEY_RE.search(parent_key) or SENSITIVE_VALUE_RE.search(value):
            return stable_redaction(value)
        return SENSITIVE_VALUE_RE.sub(lambda match: stable_redaction(match.group(0)), value)

    return value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()

    with args.input.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        json.dump(redact(data), handle, indent=args.indent, sort_keys=True)
        handle.write("\n")


if __name__ == "__main__":
    main()
