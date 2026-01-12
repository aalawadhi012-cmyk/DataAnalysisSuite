import streamlit as st
import pandas as pd
import numpy as np

import io
import json
import zipfile
from datetime import datetime

from src.utils.io import get_dataframe_from_session


def _safe_json(obj):
    try:
        json.dumps(obj)
        return obj
    except TypeError:
        if isinstance(obj, dict):
            return {k: _safe_json(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_safe_json(v) for v in obj]
        return str(obj)


def _build_eda_summary(df: pd.DataFrame) -> dict:
    summary = {}
    summary["overview"] = {
        "rows": int(df.shape[0]),
        "cols": int(df.shape[1]),
        "numeric_cols": int(df.select_dtypes(include="number").shape[1]),
        "categorical_cols": int(df.select_dtypes(exclude="number").shape[1]),
        "duplicates": int(df.duplicated().sum()),
    }

    miss_count = df.isna().sum()
    miss_pct = (miss_count / len(df) * 100) if len(df) else miss_count
    miss_tbl = pd.DataFrame({
        "column": df.columns,
        "missing_count": miss_count.values,
        "missing_pct": miss_pct.values,
        "dtype": df.dtypes.astype(str).values
    }).sort_values("missing_count", ascending=False)

    summary["missing"] = {
        "total_missing_cells": int(miss_count.sum()),
        "columns_with_missing": int((miss_count > 0).sum()),
        "missing_table_top20": miss_tbl.head(20).to_dict(orient="records"),
    }

    num_df = df.select_dtypes(include="number")
    if num_df.shape[1] >= 2:
        corr = num_df.corr(method="pearson")
        corr_pairs = (
            corr.where(np.triu(np.ones(corr.shape), k=1).astype(bool))
            .stack()
            .reset_index()
        )
        corr_pairs.columns = ["feature_1", "feature_2", "correlation"]
        top_abs = corr_pairs.reindex(corr_pairs["correlation"].abs().sort_values(ascending=False).index).head(20)
        summary["correlation"] = {
            "method": "pearson",
            "top_abs_pairs_top20": top_abs.round(6).to_dict(orient="records"),
        }
    else:
        summary["correlation"] = {"method": "pearson", "note": "Not enough numeric columns."}

    return summary


def render():
    st.subheader("09) Export")
    st.markdown(
        '<div class="muted">Export current dataset and reports only when you choose an option.</div>',
        unsafe_allow_html=True
    )
    st.markdown("")

    df, meta = get_dataframe_from_session(st.session_state)
    if df is None:
        st.markdown('<div class="card">No dataset loaded.</div>', unsafe_allow_html=True)
        return

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # -------------------------
    # User chooses what to export
    # -------------------------
    st.markdown("### Choose export type")
    export_type = st.radio(
        "What do you want to download?",
        ["CSV (dataset)", "JSON (report)", "Excel (dataset)", "ZIP (dataset + report)"],
        index=0
    )

    st.markdown("")
    include_index = st.checkbox("Include index", value=False)

    # -------------------------
    # CSV
    # -------------------------
    if export_type == "CSV (dataset)":
        sep = st.selectbox("CSV separator", [",", ";", "\t", "|"], index=0)
        csv_bytes = df.to_csv(index=include_index, sep=sep).encode("utf-8")

        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name=f"dataset_{ts}.csv",
            mime="text/csv"
        )

    # -------------------------
    # JSON report
    # -------------------------
    elif export_type == "JSON (report)":
        eda_summary = _build_eda_summary(df)
        package = {
            "meta_from_session": _safe_json(meta or {}),
            "eda_summary": _safe_json(eda_summary),
            "generated_at": ts,
        }
        json_bytes = json.dumps(package, ensure_ascii=False, indent=2).encode("utf-8")

        st.download_button(
            label="Download JSON report",
            data=json_bytes,
            file_name=f"report_{ts}.json",
            mime="application/json"
        )

    # -------------------------
    # Excel
    # -------------------------
    elif export_type == "Excel (dataset)":
        st.info("If Excel export fails, install openpyxl in your venv: pip install openpyxl")

        try:
            xlsx_buffer = io.BytesIO()
            with pd.ExcelWriter(xlsx_buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=include_index, sheet_name="data")

            st.download_button(
                label="Download Excel (.xlsx)",
                data=xlsx_buffer.getvalue(),
                file_name=f"dataset_{ts}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.exception(e)

    # -------------------------
    # ZIP package
    # -------------------------
    else:  # "ZIP (dataset + report)"
        sep = st.selectbox("CSV separator inside ZIP", [",", ";", "\t", "|"], index=0)

        # Build only when showing ZIP option (not on page load for other types)
        csv_bytes = df.to_csv(index=include_index, sep=sep).encode("utf-8")

        eda_summary = _build_eda_summary(df)
        package = {
            "meta_from_session": _safe_json(meta or {}),
            "eda_summary": _safe_json(eda_summary),
            "generated_at": ts,
        }
        json_bytes = json.dumps(package, ensure_ascii=False, indent=2).encode("utf-8")

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr(f"dataset_{ts}.csv", csv_bytes)
            zf.writestr(f"report_{ts}.json", json_bytes)
            zf.writestr(
                "README.txt",
                f"Export package generated at: {ts}\n"
                f"- dataset_{ts}.csv\n"
                f"- report_{ts}.json\n"
            )

        st.download_button(
            label="Download ZIP package",
            data=zip_buffer.getvalue(),
            file_name=f"export_package_{ts}.zip",
            mime="application/zip"
        )

    st.markdown("")
    st.markdown("### Preview")
    st.dataframe(df.head(20), use_container_width=True)
