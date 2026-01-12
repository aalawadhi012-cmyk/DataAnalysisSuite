import streamlit as st
from src.utils.io import load_dataset, set_dataframe_in_session, get_dataframe_from_session


def render():
    st.subheader("01) Data Ingestion")
    st.markdown('<div class="muted">Upload CSV/Excel/Parquet. Detect encoding (CSV) and store dataset in session.</div>', unsafe_allow_html=True)
    st.markdown("")

    # Uploader
    uploaded = st.file_uploader(
        "Upload dataset",
        type=["csv", "txt", "xlsx", "xls", "parquet"],
        accept_multiple_files=False
    )

    col_a, col_b, col_c = st.columns([0.33, 0.33, 0.34], vertical_alignment="center")

    with col_a:
        load_btn = st.button("Load dataset", type="primary", use_container_width=True)

    with col_b:
        clear_btn = st.button("Clear session dataset", use_container_width=True)

    with col_c:
        st.markdown('<div class="card"><div class="muted" style="font-size:12px;">Tip</div><div style="font-size:13px;">Use Parquet for large datasets.</div></div>', unsafe_allow_html=True)

    # Clear
    if clear_btn:
        st.session_state.pop("df", None)
        st.session_state.pop("df_meta", None)
        st.success("Session dataset cleared.")

    # Load
    if load_btn:
        if uploaded is None:
            st.error("Please upload a file first.")
        else:
            try:
                with st.spinner("Loading dataset..."):
                    df, meta = load_dataset(uploaded)
                    set_dataframe_in_session(df, meta, st.session_state)
                st.success(f"Loaded: {meta['file_name']}  |  Shape: {meta['rows']} x {meta['cols']}")
            except Exception as e:
                st.exception(e)

    st.markdown("")

    # Show current session dataset summary
    df, meta = get_dataframe_from_session(st.session_state)

    if df is None:
        st.markdown('<div class="card">No dataset loaded yet. Upload a file and click <b>Load dataset</b>.</div>', unsafe_allow_html=True)
        return

    # Summary cards
    left, mid, right = st.columns(3)
    with left:
        st.markdown(
            f"""
            <div class="card">
              <div class="muted" style="font-size:12px;">File</div>
              <div style="font-weight:800;">{meta.get("file_name","-")}</div>
              <div class="muted" style="font-size:12px;">Type: .{meta.get("file_type","-")}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with mid:
        st.markdown(
            f"""
            <div class="card">
              <div class="muted" style="font-size:12px;">Shape</div>
              <div style="font-weight:800;">{df.shape[0]} rows</div>
              <div class="muted" style="font-size:12px;">{df.shape[1]} columns</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with right:
        enc = meta.get("encoding")
        extra = f"Encoding: {enc}" if enc else "Encoding: -"
        st.markdown(
            f"""
            <div class="card">
              <div class="muted" style="font-size:12px;">Read Info</div>
              <div style="font-weight:800;">Ready</div>
              <div class="muted" style="font-size:12px;">{extra}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")
    st.markdown("### Preview")
    st.dataframe(df.head(30), use_container_width=True)

    st.markdown("")
    st.markdown("### Data types")
    st.dataframe(df.dtypes.astype(str).reset_index().rename(columns={"index": "column", 0: "dtype"}), use_container_width=True)
