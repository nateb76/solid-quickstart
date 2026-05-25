import os
import re
from pathlib import Path

import pandas as pd

TEMPLATES_DIR = Path(__file__).parent / "templates"

TOKEN_PATTERN = re.compile(r"\{\{\s*(\w+)\s*\}\}")

DEFAULT_COLUMN_MAP = {
    "insured_fname": "first_name",
    "insured_lname": "last_name",
    "policy_no": "policy_number",
    "addr1": "address_line1",
    "addr2": "address_line2",
    "zipcode": "zip",
    "zip_code": "zip",
    "postal_code": "zip",
    "st": "state",
}


def discover_templates() -> dict[str, Path]:
    """Return {friendly_name: path} for every .html in templates/."""
    templates = {}
    if not TEMPLATES_DIR.exists():
        return templates
    for f in sorted(TEMPLATES_DIR.glob("*.html")):
        friendly = f.stem.replace("_", " ").title()
        templates[friendly] = f
    return templates


def extract_tokens(template_path: Path) -> list[str]:
    """Return the list of unique {{token}} names in a template."""
    content = template_path.read_text(encoding="utf-8")
    return sorted(set(TOKEN_PATTERN.findall(content)))


def normalize_column(col: str) -> str:
    """Normalize a spreadsheet column header to canonical snake_case."""
    col = col.strip().lower()
    col = re.sub(r"\s+", "_", col)
    col = re.sub(r"[^a-z0-9_]", "", col)
    return col


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy of df with normalized column names."""
    df = df.copy()
    df.columns = [normalize_column(c) for c in df.columns]
    return df


def apply_column_mapping(columns: list[str], mapping: dict[str, str]) -> dict[str, str]:
    """Given normalized column names and a mapping dict, return {original_col: canonical_token}."""
    result = {}
    for col in columns:
        if col in mapping:
            result[col] = mapping[col]
        else:
            result[col] = col
    return result


def validate_token_coverage(
    required_tokens: list[str],
    available_columns: list[str],
    column_mapping: dict[str, str],
) -> tuple[list[str], list[str]]:
    """
    Check which required tokens are satisfied by the available columns (after mapping).
    Returns (matched_tokens, unmatched_tokens).
    """
    mapped_names = set(column_mapping.values())
    mapped_names.update(available_columns)

    matched = [t for t in required_tokens if t in mapped_names]
    unmatched = [t for t in required_tokens if t not in mapped_names]
    return matched, unmatched


def load_spreadsheet(file) -> pd.DataFrame:
    """Load a .xlsx or .csv file into a DataFrame."""
    name = file.name if hasattr(file, "name") else str(file)
    if name.endswith(".xlsx") or name.endswith(".xls"):
        df = pd.read_excel(file, dtype=str)
    else:
        df = pd.read_csv(file, dtype=str)
    df = df.fillna("")
    return df
