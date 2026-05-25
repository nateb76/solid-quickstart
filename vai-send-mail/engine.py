"""
Batch mailing engine. Pure logic — no Streamlit imports.
Writes state to a JSON Lines status file after every row.
Designed to be resumable: on restart, skip rows already marked 'sent'.
"""

import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from jinja2 import Template

from validation import validate_row
from postgrid_client import PostGridClient, MockPostGridClient, LetterResult
from ai_checks import (
    check_address_sanity,
    check_salutation,
    generate_triage_summary,
    vision_check_letter,
    DEFAULT_MODEL,
)

RUNS_DIR = Path(__file__).parent / "runs"
RUNS_DIR.mkdir(exist_ok=True)

STATUS_PENDING = "pending"
STATUS_VALIDATED = "validated"
STATUS_RENDERED = "rendered"
STATUS_SENT = "sent"
STATUS_FAILED = "failed"
STATUS_NEEDS_REVIEW = "needs_review"


def generate_run_id(template_name: str, filename: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_template = template_name.lower().replace(" ", "_")
    safe_file = Path(filename).stem.lower().replace(" ", "_")[:20]
    return f"{safe_template}_{safe_file}_{ts}"


def get_status_file_path(run_id: str) -> Path:
    return RUNS_DIR / f"{run_id}.jsonl"


def find_existing_run(template_name: str, filename: str) -> Path | None:
    """Look for an existing status file for this template+file combo."""
    safe_template = template_name.lower().replace(" ", "_")
    safe_file = Path(filename).stem.lower().replace(" ", "_")[:20]
    prefix = f"{safe_template}_{safe_file}_"

    candidates = sorted(RUNS_DIR.glob(f"{prefix}*.jsonl"), reverse=True)
    if candidates:
        return candidates[0]
    return None


def load_status_file(path: Path) -> list[dict]:
    """Load all records from a JSONL status file."""
    records = []
    if not path.exists():
        return records
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def _append_record(path: Path, record: dict):
    """Append a single JSON record to the status file."""
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def _build_to_address(row_data: dict) -> dict:
    return {
        "firstName": row_data.get("first_name", ""),
        "lastName": row_data.get("last_name", ""),
        "addressLine1": row_data.get("address_line1", ""),
        "addressLine2": row_data.get("address_line2", ""),
        "city": row_data.get("city", ""),
        "provinceOrState": row_data.get("state", ""),
        "postalOrZip": row_data.get("zip", ""),
        "country": "US",
    }


def _build_from_address(sender_info: dict) -> dict:
    return {
        "firstName": sender_info.get("first_name", ""),
        "lastName": sender_info.get("last_name", ""),
        "companyName": sender_info.get("company_name", ""),
        "addressLine1": sender_info.get("address_line1", ""),
        "addressLine2": sender_info.get("address_line2", ""),
        "city": sender_info.get("city", ""),
        "provinceOrState": sender_info.get("state", ""),
        "postalOrZip": sender_info.get("zip", ""),
        "country": "US",
    }


def _is_name_non_standard(first: str, last: str) -> bool:
    """Heuristic: flag names that look like businesses or anomalies."""
    combined = f"{first} {last}"
    if combined.isupper() and len(combined) > 5:
        return True
    business_markers = ["LLC", "INC", "CORP", "& ", "SONS", "TRUST", "ESTATE"]
    upper_combined = combined.upper()
    return any(m in upper_combined for m in business_markers)


class BatchEngine:
    def __init__(
        self,
        df: pd.DataFrame,
        template_content: str,
        required_tokens: list[str],
        column_mapping: dict[str, str],
        sender_info: dict,
        postgrid_client=None,
        run_id: str | None = None,
        api_key: str | None = None,
        ai_model: str | None = None,
        vision_sample_size: int = 20,
        vision_all: bool = False,
        use_mock: bool = True,
    ):
        self.df = df
        self.template = Template(template_content)
        self.required_tokens = required_tokens
        self.column_mapping = column_mapping
        self.sender_info = sender_info
        self.api_key = api_key
        self.ai_model = ai_model or DEFAULT_MODEL
        self.vision_sample_size = vision_sample_size
        self.vision_all = vision_all

        if postgrid_client is not None:
            self.client = postgrid_client
        elif use_mock:
            self.client = MockPostGridClient()
        else:
            raise ValueError("Must provide a PostGridClient or use_mock=True")

        self.run_id = run_id or generate_run_id("batch", "data")
        self.status_file = get_status_file_path(self.run_id)
        self._existing_records = load_status_file(self.status_file) if self.status_file.exists() else []
        self._sent_indices = {
            r["row_index"] for r in self._existing_records if r["status"] == STATUS_SENT
        }

        self._vision_sample_indices: set[int] = set()
        self._running = False
        self._stop_requested = False

    @property
    def total_rows(self) -> int:
        return len(self.df)

    @property
    def already_sent(self) -> int:
        return len(self._sent_indices)

    def request_stop(self):
        self._stop_requested = True

    def _resolve_row_data(self, row: pd.Series) -> dict:
        """Apply column mapping and return a dict with canonical token names."""
        data = {}
        for col, val in row.items():
            canonical = self.column_mapping.get(col, col)
            data[canonical] = str(val) if pd.notna(val) else ""
        return data

    def _select_vision_sample(self, validated_indices: list[int], flagged_indices: list[int]):
        """Select which rows get vision-checked."""
        if self.vision_all:
            self._vision_sample_indices = set(validated_indices + flagged_indices)
        else:
            sample_from = validated_indices
            k = min(self.vision_sample_size, len(sample_from))
            sampled = set(random.sample(sample_from, k)) if k > 0 else set()
            self._vision_sample_indices = sampled | set(flagged_indices)

    def run(self):
        """Execute the batch. Writes status after each row. Resumable."""
        self._running = True
        self._stop_requested = False

        validated_indices = []
        flagged_indices = []

        for idx in range(len(self.df)):
            if self._stop_requested:
                break
            if idx in self._sent_indices:
                continue

            row = self.df.iloc[idx]
            row_data = self._resolve_row_data(row)

            merged_html = self.template.render(**row_data)

            reasons = validate_row(merged_html, row_data, self.required_tokens)

            if reasons:
                flagged_indices.append(idx)
                record = self._make_record(idx, row_data, STATUS_NEEDS_REVIEW, reasons)
                _append_record(self.status_file, record)
                continue

            validated_indices.append(idx)

        if self._stop_requested:
            self._running = False
            return

        self._select_vision_sample(validated_indices, flagged_indices)

        for idx in validated_indices:
            if self._stop_requested:
                break
            if idx in self._sent_indices:
                continue

            row = self.df.iloc[idx]
            row_data = self._resolve_row_data(row)
            merged_html = self.template.render(**row_data)

            ai_address_result = None
            ai_salutation_result = None
            vision_result = None
            vision_checked = idx in self._vision_sample_indices
            extra_reasons = []

            if self.api_key:
                if _is_name_non_standard(
                    row_data.get("first_name", ""),
                    row_data.get("last_name", ""),
                ):
                    sal_result = check_salutation(row_data, self.api_key, self.ai_model)
                    ai_salutation_result = sal_result.detail
                    if not sal_result.passed and not sal_result.error:
                        extra_reasons.append(f"AI salutation flag: {sal_result.detail}")

            if extra_reasons:
                record = self._make_record(
                    idx, row_data, STATUS_NEEDS_REVIEW, extra_reasons,
                    ai_salutation_result=ai_salutation_result,
                )
                _append_record(self.status_file, record)
                continue

            to_addr = _build_to_address(row_data)
            from_addr = _build_from_address(self.sender_info)

            result: LetterResult = self.client.create_letter(
                html_content=merged_html,
                to_address=to_addr,
                from_address=from_addr,
                description=f"Row {idx}: {row_data.get('first_name', '')} {row_data.get('last_name', '')}",
            )

            if result.success:
                record = self._make_record(
                    idx, row_data, STATUS_SENT, [],
                    letter_id=result.letter_id,
                    pdf_url=result.pdf_url,
                    ai_address_result=ai_address_result,
                    ai_salutation_result=ai_salutation_result,
                    vision_checked=vision_checked,
                    vision_result=vision_result,
                )
            else:
                record = self._make_record(
                    idx, row_data, STATUS_FAILED,
                    [f"PostGrid error: {result.error}"],
                    letter_id=result.letter_id,
                    pdf_url=result.pdf_url,
                )

            _append_record(self.status_file, record)

        self._running = False

    def get_triage_summary(self) -> str:
        """Generate AI triage summary of failures."""
        records = load_status_file(self.status_file)
        failures = [
            r for r in records
            if r["status"] in (STATUS_FAILED, STATUS_NEEDS_REVIEW)
        ]
        if not failures:
            return "All letters passed validation and were sent successfully."
        return generate_triage_summary(failures, self.api_key, self.ai_model)

    def _make_record(
        self,
        idx: int,
        row_data: dict,
        status: str,
        reasons: list[str],
        letter_id: str | None = None,
        pdf_url: str | None = None,
        ai_address_result: str | None = None,
        ai_salutation_result: str | None = None,
        vision_checked: bool = False,
        vision_result: str | None = None,
    ) -> dict:
        return {
            "row_index": idx,
            "recipient_name": f"{row_data.get('first_name', '')} {row_data.get('last_name', '')}".strip(),
            "status": status,
            "stage": "test" if getattr(self.client, "is_test_mode", True) else "live",
            "failure_reasons": reasons,
            "token_issues": [],
            "address_flags": [],
            "ai_address_result": ai_address_result,
            "ai_salutation_result": ai_salutation_result,
            "vision_checked": vision_checked,
            "vision_result": vision_result,
            "postgrid_letter_id": letter_id,
            "postgrid_pdf_url": pdf_url,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
