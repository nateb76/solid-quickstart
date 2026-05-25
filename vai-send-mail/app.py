"""
vAI Send Mail — Streamlit UI
Reads engine status files and renders the batch mailing workflow.
"""

import json
import os
import threading
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv

from theme import inject_css, render_title
from templates_loader import (
    discover_templates,
    extract_tokens,
    normalize_columns,
    apply_column_mapping,
    validate_token_coverage,
    load_spreadsheet,
    DEFAULT_COLUMN_MAP,
)
from engine import (
    BatchEngine,
    find_existing_run,
    generate_run_id,
    get_status_file_path,
    load_status_file,
    RUNS_DIR,
)
from postgrid_client import PostGridClient, MockPostGridClient

load_dotenv()

st.set_page_config(
    page_title="vAI Send Mail",
    page_icon="✉",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()


def _get_secret(env_var: str, session_key: str) -> str:
    val = os.environ.get(env_var, "")
    if not val:
        val = st.session_state.get(session_key, "")
    return val


def _run_engine_thread(engine: BatchEngine):
    engine.run()


def main():
    render_title()

    if "run_active" not in st.session_state:
        st.session_state.run_active = False
    if "run_id" not in st.session_state:
        st.session_state.run_id = None
    if "engine" not in st.session_state:
        st.session_state.engine = None
    if "column_mapping" not in st.session_state:
        st.session_state.column_mapping = dict(DEFAULT_COLUMN_MAP)
    if "triage_summary" not in st.session_state:
        st.session_state.triage_summary = None

    if st.session_state.run_active and st.session_state.run_id:
        _render_running_screen()
    elif st.session_state.run_id and not st.session_state.run_active:
        _render_report_screen()
    else:
        _render_setup_screen()


def _render_setup_screen():
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Upload Client List")
        uploaded_file = st.file_uploader(
            "Drop your .xlsx or .csv file here",
            type=["xlsx", "xls", "csv"],
            key="file_upload",
        )

    with col2:
        st.subheader("Letter Template")
        templates = discover_templates()
        if not templates:
            st.warning("No templates found in templates/ directory.")
            return

        template_name = st.selectbox(
            "Select letter type",
            options=list(templates.keys()),
            key="template_select",
        )

    if not uploaded_file or not template_name:
        st.info("Select a file and template to begin.")
        return

    template_path = templates[template_name]
    required_tokens = extract_tokens(template_path)

    df = load_spreadsheet(uploaded_file)
    df_normalized = normalize_columns(df)
    available_cols = list(df_normalized.columns)

    col_mapping = apply_column_mapping(available_cols, st.session_state.column_mapping)
    matched, unmatched = validate_token_coverage(required_tokens, available_cols, col_mapping)

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.subheader("Pre-Flight Validation")

    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("Total Rows", len(df_normalized))
    mc2.metric("Columns Found", len(available_cols))
    mc3.metric("Tokens Matched", f"{len(matched)}/{len(required_tokens)}")
    mc4.metric("Unmatched", len(unmatched))

    if unmatched:
        st.error(f"**Unmatched tokens:** {', '.join(unmatched)}")
        st.caption("Map these in the Column Mapping section below, or add the columns to your spreadsheet.")

    with st.expander("Column Mapping", expanded=bool(unmatched)):
        st.caption("Map non-standard spreadsheet columns to required template tokens.")
        mapping_text = st.text_area(
            "Mapping (JSON format)",
            value=json.dumps(st.session_state.column_mapping, indent=2),
            height=150,
        )
        if st.button("Update Mapping"):
            try:
                st.session_state.column_mapping = json.loads(mapping_text)
                st.rerun()
            except json.JSONDecodeError:
                st.error("Invalid JSON format.")

    with st.expander("Token Details"):
        t1, t2 = st.columns(2)
        with t1:
            st.markdown("**Template Requires:**")
            for t in required_tokens:
                icon = "✓" if t in matched else "✗"
                color = "green" if t in matched else "red"
                st.markdown(f":{color}[{icon}] `{t}`")
        with t2:
            st.markdown("**Spreadsheet Provides (normalized):**")
            for c in sorted(available_cols):
                st.markdown(f"  `{c}`")

    existing_run = find_existing_run(template_name, uploaded_file.name)
    if existing_run:
        st.info(f"Previous run found: `{existing_run.name}`. You can resume it.")
        resume = st.checkbox("Resume previous run", value=False)
    else:
        resume = False

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.subheader("Run Configuration")

    cfg1, cfg2 = st.columns(2)

    with cfg1:
        mode = st.radio(
            "Mode",
            ["Test (Mock PostGrid)", "Test (Real PostGrid - Test Key)", "Live (Real PostGrid - Live Key)"],
            index=0,
            help="Test mode renders letters without mailing. Live mode actually sends mail.",
        )

        go_live = False
        if "Live" in mode:
            st.warning("**LIVE MODE** — Letters will be physically mailed and charged.")
            go_live = st.checkbox(
                "I confirm: send real mail",
                value=False,
                key="go_live_confirm",
            )

    with cfg2:
        vision_sample = st.number_input("Vision sample size", min_value=0, max_value=100, value=20)
        vision_all = st.checkbox("Vision-check ALL letters", value=False)
        ai_model = st.text_input("AI model", value="claude-haiku-4-5-20251001")

    with st.expander("Sender (Return) Address"):
        s1, s2 = st.columns(2)
        with s1:
            sender_first = st.text_input("First Name", value="", key="sender_first")
            sender_last = st.text_input("Last Name", value="", key="sender_last")
            sender_company = st.text_input("Company", value="", key="sender_company")
        with s2:
            sender_addr1 = st.text_input("Address Line 1", value="", key="sender_addr1")
            sender_city = st.text_input("City", value="", key="sender_city")
            sender_state = st.text_input("State", value="", key="sender_state")
            sender_zip = st.text_input("ZIP", value="", key="sender_zip")

    with st.expander("API Keys (if not in .env)"):
        st.caption("Keys are held in session memory only — never written to disk.")
        postgrid_test_key = st.text_input(
            "PostGrid Test Key",
            type="password",
            key="postgrid_test_input",
            value=st.session_state.get("postgrid_test_key", ""),
        )
        postgrid_live_key = st.text_input(
            "PostGrid Live Key",
            type="password",
            key="postgrid_live_input",
            value=st.session_state.get("postgrid_live_key", ""),
        )
        anthropic_key = st.text_input(
            "Anthropic API Key",
            type="password",
            key="anthropic_input",
            value=st.session_state.get("anthropic_api_key", ""),
        )
        if postgrid_test_key:
            st.session_state["postgrid_test_key"] = postgrid_test_key
        if postgrid_live_key:
            st.session_state["postgrid_live_key"] = postgrid_live_key
        if anthropic_key:
            st.session_state["anthropic_api_key"] = anthropic_key

    can_go = len(unmatched) == 0
    if "Live" in mode and not go_live:
        can_go = False

    go_tooltip = ""
    if unmatched:
        go_tooltip = f"Cannot start: unmatched tokens: {', '.join(unmatched)}"
    elif "Live" in mode and not go_live:
        go_tooltip = "Enable the live-mode confirmation toggle to proceed"

    if st.button(
        "Begin Mailing Run",
        type="primary",
        disabled=not can_go,
        help=go_tooltip or "Start the batch",
        use_container_width=True,
    ):
        template_content = template_path.read_text(encoding="utf-8")

        sender_info = {
            "first_name": sender_first,
            "last_name": sender_last,
            "company_name": sender_company,
            "address_line1": sender_addr1,
            "city": sender_city,
            "state": sender_state,
            "zip": sender_zip,
        }

        use_mock = "Mock" in mode
        postgrid_client = None

        if not use_mock:
            if "Live" in mode:
                key = _get_secret("POSTGRID_LIVE_KEY", "postgrid_live_key")
            else:
                key = _get_secret("POSTGRID_TEST_KEY", "postgrid_test_key")
            if not key:
                st.error("PostGrid API key required for non-mock mode.")
                return
            postgrid_client = PostGridClient(key)

        anthropic_key_resolved = _get_secret("ANTHROPIC_API_KEY", "anthropic_api_key")

        if resume and existing_run:
            run_id = existing_run.stem
        else:
            run_id = generate_run_id(template_name, uploaded_file.name)

        engine = BatchEngine(
            df=df_normalized,
            template_content=template_content,
            required_tokens=required_tokens,
            column_mapping=col_mapping,
            sender_info=sender_info,
            postgrid_client=postgrid_client,
            run_id=run_id,
            api_key=anthropic_key_resolved,
            ai_model=ai_model,
            vision_sample_size=vision_sample,
            vision_all=vision_all,
            use_mock=use_mock,
        )

        st.session_state.engine = engine
        st.session_state.run_id = run_id
        st.session_state.run_active = True
        st.session_state.triage_summary = None

        thread = threading.Thread(target=_run_engine_thread, args=(engine,), daemon=True)
        thread.start()
        st.rerun()


def _render_running_screen():
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.subheader("Run in Progress")

    run_id = st.session_state.run_id
    status_path = get_status_file_path(run_id)
    records = load_status_file(status_path)

    engine = st.session_state.engine
    total = engine.total_rows if engine else 0

    sent = sum(1 for r in records if r["status"] == "sent")
    failed = sum(1 for r in records if r["status"] == "failed")
    needs_review = sum(1 for r in records if r["status"] == "needs_review")
    processed = sent + failed + needs_review
    remaining = total - processed

    progress = processed / total if total > 0 else 0
    st.progress(progress)

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Sent", sent)
    m2.metric("Failed", failed)
    m3.metric("Needs Review", needs_review)
    m4.metric("Remaining", remaining)
    m5.metric("Progress", f"{progress * 100:.1f}%")

    if records:
        recent = records[-20:]
        display_data = []
        for r in reversed(recent):
            display_data.append({
                "Row": r["row_index"],
                "Recipient": r["recipient_name"],
                "Status": r["status"],
                "Reason": "; ".join(r.get("failure_reasons", [])) or "-",
            })
        st.dataframe(pd.DataFrame(display_data), use_container_width=True, hide_index=True)

    is_engine_done = engine and not engine._running and processed > 0

    if remaining > 0 and not is_engine_done:
        if st.button("Stop Run"):
            if engine:
                engine.request_stop()
            st.session_state.run_active = False
            st.rerun()

        time.sleep(2)
        st.rerun()
    else:
        st.success(f"Run complete: {sent} sent, {failed} failed, {needs_review} need review.")
        st.session_state.run_active = False

        if engine and st.session_state.triage_summary is None:
            with st.spinner("Generating AI triage summary..."):
                st.session_state.triage_summary = engine.get_triage_summary()

        st.rerun()


def _render_report_screen():
    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.subheader("Batch Report")

    run_id = st.session_state.run_id
    status_path = get_status_file_path(run_id)
    records = load_status_file(status_path)

    if not records:
        st.warning("No records found for this run.")
        if st.button("Start New Run"):
            st.session_state.run_id = None
            st.rerun()
        return

    sent = [r for r in records if r["status"] == "sent"]
    failed = [r for r in records if r["status"] == "failed"]
    needs_review = [r for r in records if r["status"] == "needs_review"]

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Processed", len(records))
    m2.metric("Sent", len(sent))
    m3.metric("Failed", len(failed))
    m4.metric("Needs Review", len(needs_review))

    if st.session_state.triage_summary:
        st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
        st.markdown("**AI Triage Summary**")
        st.markdown(
            f'<div class="card">{st.session_state.triage_summary}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    bad_letters = failed + needs_review
    if bad_letters:
        st.subheader("Bad Letter Report")
        bad_data = []
        for r in bad_letters:
            bad_data.append({
                "Row": r["row_index"],
                "Recipient": r["recipient_name"],
                "Status": r["status"],
                "Reasons": "; ".join(r.get("failure_reasons", [])),
                "PDF Preview": r.get("postgrid_pdf_url", "-"),
            })
        bad_df = pd.DataFrame(bad_data)
        st.dataframe(bad_df, use_container_width=True, hide_index=True)

        csv_bad = bad_df.to_csv(index=False)
        st.download_button(
            "Download Bad Letters (CSV)",
            data=csv_bad,
            file_name=f"bad_letters_{run_id}.csv",
            mime="text/csv",
        )

    if sent:
        with st.expander(f"Sent Letters ({len(sent)})"):
            sent_data = []
            for r in sent:
                sent_data.append({
                    "Row": r["row_index"],
                    "Recipient": r["recipient_name"],
                    "Letter ID": r.get("postgrid_letter_id", "-"),
                    "PDF": r.get("postgrid_pdf_url", "-"),
                })
            st.dataframe(pd.DataFrame(sent_data), use_container_width=True, hide_index=True)

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    full_jsonl = "\n".join(json.dumps(r) for r in records)
    st.download_button(
        "Download Full Audit Log (JSONL)",
        data=full_jsonl,
        file_name=f"audit_{run_id}.jsonl",
        mime="application/jsonl",
    )

    full_csv = pd.DataFrame(records).to_csv(index=False)
    st.download_button(
        "Download Full Audit Log (CSV)",
        data=full_csv,
        file_name=f"audit_{run_id}.csv",
        mime="text/csv",
    )

    if st.button("Start New Run"):
        st.session_state.run_id = None
        st.session_state.run_active = False
        st.session_state.engine = None
        st.session_state.triage_summary = None
        st.rerun()


if __name__ == "__main__":
    main()
