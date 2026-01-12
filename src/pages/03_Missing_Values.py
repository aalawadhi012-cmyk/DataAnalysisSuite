import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from src.utils.io import get_dataframe_from_session, set_dataframe_in_session


def render():
    st.subheader("03) Missing Values")
    st.markdown(
        '<div class="muted">Analyze missing values and apply treatments (drop / impute).</div>',
        unsafe_allow_html=True
    )
    st.markdown("")

    df, meta = get_dataframe_from_session(st.session_state)

    if df is None:
        st.markdown('<div class="card">No dataset loaded. Please load a dataset first.</div>', unsafe_allow_html=True)
        return

    # =========================
    # Missing summary
    # =========================
    miss_count = df.isna().sum()
    miss_pct = (miss_count / len(df)) * 100

    summary = (
        pd.DataFrame({
            "column": df.columns,
            "missing_count": miss_count.values,
            "missing_pct": miss_pct.values,
            "dtype": df.dtypes.astype(str).values
        })
        .sort_values("missing_count", ascending=False)
    )

    total_missing = int(miss_count.sum())
    cols_with_missing = int((miss_count > 0).sum())

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"<div class='card'><b>Total missing cells</b><br>{total_missing}</div>",
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"<div class='card'><b>Columns with missing</b><br>{cols_with_missing}</div>",
            unsafe_allow_html=True
        )
    with c3:
        ratio = (total_missing / df.size) * 100 if df.size else 0
        st.markdown(
            f"<div class='card'><b>Missing ratio</b><br>{ratio:.2f}%</div>",
            unsafe_allow_html=True
        )

    st.markdown("")
    st.markdown("### Missing values per column (table)")
    st.dataframe(summary, use_container_width=True)

    # =========================
    # BAR CHART (ONLY)
    # =========================
    st.markdown("")
    st.markdown("### Missing values per column (Bar chart)")

    plot_df = summary.copy()

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.bar(
        plot_df["column"],
        plot_df["missing_count"],
        color="#1f2937",          # dark gray (clear & professional)
        edgecolor="black",
        linewidth=0.8
    )

    ax.set_title("Missing Values per Column", fontsize=14, fontweight="bold")
    ax.set_xlabel("Columns")
    ax.set_ylabel("Missing Count")

    ax.tick_params(axis="x", rotation=45, labelsize=9)
    ax.tick_params(axis="y", labelsize=9)

    ax.grid(axis="y", linestyle="--", alpha=0.4)

    # Important: show zeros clearly
    ax.set_ylim(bottom=0)

    st.pyplot(fig, clear_figure=True)
    plt.close(fig)

    if total_missing == 0:
        st.info("No missing values detected. All bars at zero indicate complete data.")

    # =========================
    # Treatment
    # =========================
    st.markdown("")
    st.markdown("### Treatment")

    tabs = st.tabs(["Drop columns", "Drop rows", "Impute"])

    # Drop columns
    with tabs[0]:
        threshold = st.slider("Drop columns if missing % >", 0, 100, 40, 5)
        cols_to_drop = summary.loc[summary["missing_pct"] > threshold, "column"].tolist()

        st.write(f"Columns to drop: {len(cols_to_drop)}")
        if cols_to_drop:
            st.code(", ".join(cols_to_drop))

        if st.button("Apply: Drop columns", type="primary"):
            new_df = df.drop(columns=cols_to_drop)
            set_dataframe_in_session(new_df, meta, st.session_state)
            st.success(f"Applied. New shape: {new_df.shape}")

    # Drop rows
    with tabs[1]:
        selected_cols = st.multiselect("Columns", df.columns.tolist())
        how = st.selectbox("Rule", ["any", "all"])
        if st.button("Apply: Drop rows", type="primary"):
            if not selected_cols:
                st.error("Select at least one column.")
            else:
                new_df = df.dropna(subset=selected_cols, how=how)
                set_dataframe_in_session(new_df, meta, st.session_state)
                st.success(f"Applied. New rows: {new_df.shape[0]}")

    # Impute
    with tabs[2]:
        num_cols = df.select_dtypes(include="number").columns.tolist()
        cat_cols = [c for c in df.columns if c not in num_cols]

        strategy = st.selectbox("Numeric strategy", ["mean", "median", "zero"])
        if st.button("Apply: Impute", type="primary"):
            new_df = df.copy()

            if num_cols:
                if strategy == "mean":
                    new_df[num_cols] = new_df[num_cols].fillna(new_df[num_cols].mean())
                elif strategy == "median":
                    new_df[num_cols] = new_df[num_cols].fillna(new_df[num_cols].median())
                else:
                    new_df[num_cols] = new_df[num_cols].fillna(0)

            if cat_cols:
                new_df[cat_cols] = new_df[cat_cols].fillna("Unknown")

            set_dataframe_in_session(new_df, meta, st.session_state)
            st.success("Imputation applied.")

    st.markdown("")
    st.markdown("### Post-action preview")
    st.dataframe(st.session_state["df"].head(20), use_container_width=True)
