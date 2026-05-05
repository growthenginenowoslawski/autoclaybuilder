#!/usr/bin/env python3
"""Score basic Clay table config parity from redacted source and target manifests."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


IGNORED_FIELD_KEYS = {
    "id",
    "createdAt",
    "updatedAt",
    "creator",
    "workspaceId",
    "tableId",
    "cellCount",
}


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def fields_by_id(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    fields = manifest.get("fields") or []
    return {field["id"]: field for field in fields if isinstance(field, dict) and field.get("id")}


def normalize_field(field: dict[str, Any], field_map: dict[str, str]) -> dict[str, Any]:
    def remap(value: Any) -> Any:
        if isinstance(value, str):
            for source_id, target_id in field_map.items():
                value = value.replace(target_id, source_id)
            return value
        if isinstance(value, list):
            return [remap(item) for item in value]
        if isinstance(value, dict):
            return {key: remap(child) for key, child in value.items() if key not in IGNORED_FIELD_KEYS}
        return value

    return remap({key: value for key, value in field.items() if key not in IGNORED_FIELD_KEYS})


def compare_fields(
    source: dict[str, dict[str, Any]],
    target: dict[str, dict[str, Any]],
    field_map: dict[str, str],
) -> list[dict[str, Any]]:
    mismatches: list[dict[str, Any]] = []
    for source_id, source_field in source.items():
        target_id = field_map.get(source_id)
        if not target_id:
            mismatches.append({"sourceFieldId": source_id, "type": "missing_field_map"})
            continue
        target_field = target.get(target_id)
        if not target_field:
            mismatches.append({"sourceFieldId": source_id, "targetFieldId": target_id, "type": "missing_target_field"})
            continue

        source_norm = normalize_field(source_field, field_map)
        target_norm = normalize_field(target_field, field_map)
        if source_norm != target_norm:
            mismatches.append(
                {
                    "sourceFieldId": source_id,
                    "targetFieldId": target_id,
                    "type": "config_mismatch",
                    "sourceName": source_field.get("name"),
                    "targetName": target_field.get("name"),
                }
            )
    return mismatches


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("target", type=Path)
    parser.add_argument("--field-map", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    source_manifest = load_json(args.source)
    target_manifest = load_json(args.target)
    field_map = load_json(args.field_map)

    source_fields = fields_by_id(source_manifest)
    target_fields = fields_by_id(target_manifest)
    mismatches = compare_fields(source_fields, target_fields, field_map)

    total = len(source_fields)
    matched = max(total - len(mismatches), 0)
    score = matched / total if total else 0.0
    report = {
        "score": round(score, 6),
        "matchedFields": matched,
        "sourceFieldCount": total,
        "targetFieldCount": len(target_fields),
        "status": "perfect_config_parity" if score == 1.0 else "config_mismatch",
        "mismatches": mismatches,
    }

    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
