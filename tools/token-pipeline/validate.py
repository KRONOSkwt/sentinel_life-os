#!/usr/bin/env python3
"""Validate tokens.json against schema and check consistency"""
import json
import sys
from pathlib import Path

def validate_tokens(path: str) -> bool:
    try:
        with open(path) as f:
            tokens = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}", file=sys.stderr)
        return False

    errors = []

    # Required top-level keys
    for key in ["colors", "spacing", "radius", "typography"]:
        if key not in tokens:
            errors.append(f"Missing top-level key: {key}")

    # Spacing values must be positive numbers
    for key, value in tokens.get("spacing", {}).items():
        if not isinstance(value, (int, float)) or value <= 0:
            errors.append(f"Invalid spacing.{key}: {value}")

    # Radius values must be positive numbers
    for key, value in tokens.get("radius", {}).items():
        if not isinstance(value, (int, float)) or value <= 0:
            errors.append(f"Invalid radius.{key}: {value}")

    # Color values: allow strings (hex, rgba, box-shadow) and numbers (blur)
    for group, values in tokens.get("colors", {}).items():
        for key, value in values.items():
            if isinstance(value, (int, float)):
                # Numeric values like blur are acceptable
                continue
            if not isinstance(value, str):
                errors.append(f"Invalid color {group}.{key}: not a string or number")

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return False

    print("Tokens validation: PASS")
    return True

if __name__ == "__main__":
    tokens_path = sys.argv[1] if len(sys.argv) > 1 else "libs/shared/tokens/tokens.json"
    success = validate_tokens(tokens_path)
    sys.exit(0 if success else 1)