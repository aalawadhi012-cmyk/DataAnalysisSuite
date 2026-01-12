import streamlit as st
import pandas as pd
from src.utils.io import get_dataframe_from_session


def render():
    st.subheader("02) Overview")
    st.markdown(
        '<div class="muted">High-level dataset summary, structure, and basic statistics.</div>',
        unsafe_allow_html=True
    )
    st.markdown("")

    df, meta = get_dataframe_from_session(st.session_state)

    if df is None:
        st.markdown(
            '<div class="card">No dataset loaded. Please load a dataset first.</div>',
            unsafe_allow_html=True
        )
        return

    # -------------------------
    # Basic structure
    # -------------------------
    n_rows, n_cols = df.shape
    num_cols = df.select_dtypes(include="number").columns
    cat_cols = df.select_dtypes(exclude="number").columns

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
            <div class="card">
              <div class="muted" style="font-size:12px;">Rows</div>
              <div style="font-size:22px;font-weight:800;">{n_rows}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="card">
              <div class="muted" style="font-size:12px;">Columns</div>
              <div style="font-size:22px;font-weight:800;">{n_cols}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""
            <div class="card">
              <div class="muted" style="font-size:12px;">Numeric</div>
              <div style="font-size:22px;font-weight:800;">{len(num_cols)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""
            <div class="card">
              <div class="muted" style="font-size:12px;">Categorical</div>
              <div style="font-size:22px;font-weight:800;">{len(cat_cols)}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------
    # Duplicates
    # -------------------------
    st.markdown("")
    dup_count = df.duplicated().sum()
    st.markdown(
        f"""
        <div class="card">
          <div class="muted" style="font-size:12px;">Duplicate rows</div>
          <div style="font-size:18px;font-weight:700;">{dup_count}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------
    # Unique values per column
    # -------------------------
    st.markdown("")
    st.markdown("### Unique values per column")
    unique_df = (
        pd.DataFrame({
            "column": df.columns,
            "unique_values": [df[col].nunique(dropna=True) for col in df.columns],
            "dtype": df.dtypes.astype(str).values
        })
        .sort_values("unique_values", ascending=False)
    )
    st.dataframe(unique_df, use_container_width=True)

    # -------------------------
    # Descriptive statistics
    # -------------------------
    st.markdown("")
    st.markdown("### Descriptive statistics (numeric)")
    if len(num_cols) == 0:
        st.info("No numeric columns found.")
    else:
        desc = df[num_cols].describe().T
        st.dataframe(desc, use_container_width=True)
