import os
from dataclasses import dataclass

try:
    import anthropic
except ImportError:
    anthropic = None


@dataclass
class AICheckResult:
    passed: bool
    detail: str
    error: bool = False


DEFAULT_MODEL = "claude-haiku-4-5-20251001"


def _get_client(api_key: str | None = None):
    if anthropic is None:
        return None
    key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
    if not key:
        return None
    return anthropic.Anthropic(api_key=key)


def check_address_sanity(
    address_fields: dict,
    api_key: str | None = None,
    model: str | None = None,
) -> AICheckResult:
    """Ask the model if an address looks plausible."""
    client = _get_client(api_key)
    if client is None:
        return AICheckResult(passed=True, detail="AI unavailable, skipped", error=True)

    model = model or DEFAULT_MODEL
    prompt = (
        "You are validating a US mailing address for plausibility. "
        "Check if the city, state, and ZIP could reasonably go together, "
        "and if the street address looks structurally valid. "
        "Respond with ONLY 'PASS' if it looks plausible, or 'FLAG: <reason>' if something is wrong.\n\n"
        f"Address:\n"
        f"  Line 1: {address_fields.get('address_line1', '')}\n"
        f"  Line 2: {address_fields.get('address_line2', '')}\n"
        f"  City: {address_fields.get('city', '')}\n"
        f"  State: {address_fields.get('state', '')}\n"
        f"  ZIP: {address_fields.get('zip', '')}\n"
    )

    try:
        response = client.messages.create(
            model=model,
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        if text.startswith("PASS"):
            return AICheckResult(passed=True, detail="ok")
        else:
            return AICheckResult(passed=False, detail=text)
    except Exception as e:
        return AICheckResult(passed=True, detail=f"AI error: {str(e)[:100]}", error=True)


def check_salutation(
    name_fields: dict,
    api_key: str | None = None,
    model: str | None = None,
) -> AICheckResult:
    """Ask the model for appropriate salutation when the name looks non-standard."""
    client = _get_client(api_key)
    if client is None:
        return AICheckResult(passed=True, detail="AI unavailable, skipped", error=True)

    model = model or DEFAULT_MODEL
    first = name_fields.get("first_name", "")
    last = name_fields.get("last_name", "")

    prompt = (
        "You are checking if a recipient name is suitable for a personal letter salutation. "
        f"The name is: first='{first}', last='{last}'. "
        "If this looks like a normal personal name, respond 'PASS'. "
        "If it looks like a business name, all-caps anomaly, or otherwise needs human review, "
        "respond 'FLAG: <brief reason>'. One line only."
    )

    try:
        response = client.messages.create(
            model=model,
            max_tokens=80,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        if text.startswith("PASS"):
            return AICheckResult(passed=True, detail="ok")
        else:
            return AICheckResult(passed=False, detail=text)
    except Exception as e:
        return AICheckResult(passed=True, detail=f"AI error: {str(e)[:100]}", error=True)


def generate_triage_summary(
    failure_list: list[dict],
    api_key: str | None = None,
    model: str | None = None,
) -> str:
    """Generate a one-paragraph triage summary of batch failures."""
    client = _get_client(api_key)
    if client is None:
        return "AI triage unavailable (no API key configured)."

    if not failure_list:
        return "No failures to triage."

    model = model or DEFAULT_MODEL
    summary_input = "\n".join(
        f"Row {f.get('row_index', '?')}: {', '.join(f.get('failure_reasons', ['unknown']))}"
        for f in failure_list[:50]
    )

    prompt = (
        "You are analyzing batch mailing failures for an insurance agency. "
        f"There are {len(failure_list)} total failures. Here are up to 50:\n\n"
        f"{summary_input}\n\n"
        "Write a single paragraph (3-4 sentences) summarizing the main patterns, "
        "most common failure type, and a recommended action. Be specific about counts."
    )

    try:
        response = client.messages.create(
            model=model,
            max_tokens=250,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text.strip()
    except Exception as e:
        return f"AI triage failed: {str(e)[:100]}"


def vision_check_letter(
    pdf_image_bytes: bytes,
    api_key: str | None = None,
    model: str | None = None,
) -> AICheckResult:
    """Send a rasterized letter image to the model for layout verification."""
    client = _get_client(api_key)
    if client is None:
        return AICheckResult(passed=True, detail="AI unavailable, skipped", error=True)

    model = model or DEFAULT_MODEL
    import base64
    b64 = base64.b64encode(pdf_image_bytes).decode("utf-8")

    try:
        response = client.messages.create(
            model=model,
            max_tokens=150,
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "This is a rendered mailing letter. Check for: "
                            "1) Text overflow or clipping 2) Address block misalignment "
                            "3) Broken layout or overlapping elements 4) Any obvious rendering errors. "
                            "Respond with ONLY 'PASS' if the letter looks correct, "
                            "or 'FLAG: <specific issue>' if there's a problem."
                        ),
                    },
                ],
            }],
        )
        text = response.content[0].text.strip()
        if text.startswith("PASS"):
            return AICheckResult(passed=True, detail="ok")
        else:
            return AICheckResult(passed=False, detail=text)
    except Exception as e:
        return AICheckResult(passed=True, detail=f"Vision error: {str(e)[:100]}", error=True)
