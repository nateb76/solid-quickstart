# vAI Send Mail

A batch mailing application for insurance agencies. Merges a spreadsheet of clients against a chosen letter template, validates every letter before anything is mailed, sends approved letters through the PostGrid print-mail API, runs AI verification on a sample, and reports which letters failed and why — with links to rendered PDFs.

## Setup

### Prerequisites

- Python 3.11+
- macOS (Apple Silicon or Intel) — also works on Linux

### Installation

```bash
cd vai-send-mail
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Configuration

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

You need:
- **PostGrid Test Key** (`test_...`) — renders letters as PDFs without mailing
- **PostGrid Live Key** (`live_...`) — actually sends physical mail (optional until you go live)
- **Anthropic API Key** — powers the AI verification layer (optional; the app works without it)

Alternatively, you can paste keys directly into the app's "API Keys" section at runtime — they're held in memory only, never written to disk.

## Running

```bash
streamlit run app.py
```

## Workflow: Test → Live

1. **Upload** your client spreadsheet (.xlsx or .csv)
2. **Select** the letter template from the dropdown
3. **Review** the pre-flight validation — fix any column mapping issues
4. **Run in Test mode** (default) — this uses a mock PostGrid or the test key, producing preview PDFs without mailing
5. **Review the report** — check the bad-letter list, fix data issues in your spreadsheet
6. **Run in Live mode** — toggle the mode selector, confirm the Go-Live checkbox, and send real mail

## Adding a New Letter Template

Drop a new `.html` file into the `templates/` directory. It appears in the dropdown automatically on next launch.

Templates use Jinja2 `{{token}}` syntax. Available tokens (canonical names):

- `first_name`, `last_name`
- `address_line1`, `address_line2`
- `city`, `state`, `zip`
- `policy_number`
- `agency_name`
- `date`

You can add any additional tokens — the app will detect them and require matching columns in the spreadsheet.

## Column Mapping

Insurance exports have inconsistent headers. The app:
1. Normalizes all headers (lowercase, underscores)
2. Applies a configurable mapping dict for genuinely different names
3. Shows you what's missing before the run can start

Edit the mapping in the "Column Mapping" expander in the UI, or modify `DEFAULT_COLUMN_MAP` in `templates_loader.py`.

## Resumability

The engine writes a checkpoint after every single row. If the process crashes:
1. Re-upload the same file and select the same template
2. The app detects the previous run and offers to resume
3. Already-sent rows are never re-sent

## Compliance Note

This application enforces correctness of the **merge and delivery process** — it validates that templates are populated correctly, addresses are structurally valid, and letters render properly.

**It does not validate the legal sufficiency of letter content.** Confirming that notice language, timing, and delivery method meet your state's insurance regulatory requirements is the user's responsibility. Each letter template is version-controlled so the exact language sent is auditable.

The JSONL status file in `runs/` serves as the proof-of-mailing trail. Preserve these files for your records.

## Architecture

```
app.py           → Streamlit UI (display only, reads status files)
engine.py        → Batch processing engine (no Streamlit imports, runs independently)
validation.py    → Text-gate checks (regex/structural, no AI)
ai_checks.py     → AI verification (address, salutation, vision, triage)
postgrid_client.py → PostGrid API wrapper with retry logic
templates_loader.py → Template discovery and column normalization
theme.py         → Bene Gesserit visual theme (CSS injection)
```

The engine and UI are fully decoupled. The engine writes to the status file; the UI reads it. You can close the browser and the run continues. Reopen the browser and you reattach to the live progress.
