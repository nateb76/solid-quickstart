import re

US_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC", "PR", "VI", "GU", "AS", "MP",
}

TOKEN_REMNANT = re.compile(r"\{\{[^}]*\}\}|\[[A-Z_]+\]")
DOUBLE_SPACE = re.compile(r"  +")
SPACE_BEFORE_PUNCT = re.compile(r"\s+[,.:;!?]")
ORPHAN_PUNCT = re.compile(r"(?:^|(?<=\n))\s*[,.]")
ZIP_PATTERN = re.compile(r"^\d{5}(-\d{4})?$")


def validate_row(merged_html: str, row_data: dict, required_tokens: list[str]) -> list[str]:
    """
    Run all text-gate checks on a single merged letter.
    Returns a list of failure reasons (empty = pass).
    """
    reasons = []

    reasons.extend(_check_unreplaced_tokens(merged_html))
    reasons.extend(_check_whitespace_defects(merged_html))
    reasons.extend(_check_field_presence(merged_html, row_data, required_tokens))
    reasons.extend(_check_address_structure(row_data))

    return reasons


def _check_unreplaced_tokens(html: str) -> list[str]:
    matches = TOKEN_REMNANT.findall(html)
    if matches:
        return [f"Unreplaced token(s): {', '.join(set(matches))}"]
    return []


def _check_whitespace_defects(html: str) -> list[str]:
    issues = []

    text = re.sub(r"<[^>]+>", " ", html)
    text = re.sub(r"&\w+;", " ", text)

    if DOUBLE_SPACE.search(text):
        issues.append("Double spaces detected in letter content")

    if SPACE_BEFORE_PUNCT.search(text):
        issues.append("Space before punctuation detected (possible blank field)")

    if ORPHAN_PUNCT.search(text):
        issues.append("Orphan punctuation at line start (possible blank field)")

    return issues


def _check_field_presence(html: str, row_data: dict, required_tokens: list[str]) -> list[str]:
    issues = []
    skip_fields = {"address_line2"}

    for token in required_tokens:
        if token in skip_fields:
            continue
        value = str(row_data.get(token, "")).strip()
        if value and value not in html:
            issues.append(f"Field '{token}' value '{value}' not found in merged letter")

    return issues


def _check_address_structure(row_data: dict) -> list[str]:
    issues = []

    addr1 = str(row_data.get("address_line1", "")).strip()
    city = str(row_data.get("city", "")).strip()
    state = str(row_data.get("state", "")).strip().upper()
    zip_code = str(row_data.get("zip", "")).strip()

    if not addr1:
        issues.append("Missing address_line1")
    if not city:
        issues.append("Missing city")
    if not state:
        issues.append("Missing state")
    elif state not in US_STATES:
        issues.append(f"Invalid state code: '{state}'")
    if not zip_code:
        issues.append("Missing ZIP code")
    elif not ZIP_PATTERN.match(zip_code):
        issues.append(f"Invalid ZIP format: '{zip_code}'")

    return issues
