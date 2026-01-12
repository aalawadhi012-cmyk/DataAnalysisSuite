import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from src.utils.io import get_dataframe_from_session


def render():
    st.subheader("04) Univariate Analysis")
    st.markdown(
        '<div class="muted">Analyze a single variable: distribution, central tendency, spread, and category frequency.</div>',
        unsafe_allow_html=True
    )
    st.markdown("")

    df, _ = get_dataframe_from_session(st.session_state)
    if df is None:
        st.markdown('<div class="card">No dataset loaded. Please load a dataset first.</div>', unsafe_allow_html=True)
        return

    # -------------------------
    # Column selection
    # -------------------------
    cols = df.columns.tolist()
    col = st.selectbox("Select a column", cols, index=0)

    s = df[col]
    is_num = pd.api.types.is_numeric_dtype(s)

    # Optional sampling for plots (keeps charts readable/performance stable)
    max_plot_n = st.slider("Max rows for plots (sampling if needed)", 500, 20000, 5000, 500)
    plot_s = s.dropna()
    if len(plot_s) > max_plot_n:
        plot_s = plot_s.sample(max_plot_n, random_state=42)

    # -------------------------
    # Summary cards
    # -------------------------
    missing = int(s.isna().sum())
    unique = int(s.nunique(dropna=True))
    total = int(len(s))

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card'><b>Type</b><br>{'Numeric' if is_num else 'Categorical/Text'}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card'><b>Total</b><br>{total}</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card'><b>Missing</b><br>{missing}</div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='card'><b>Unique</b><br>{unique}</div>", unsafe_allow_html=True)

    st.markdown("")

    # -------------------------
    # Numeric analysis
    # -------------------------
    if is_num:
        st.markdown("### Numeric summary")
        desc = s.describe()
        q1 = float(s.quantile(0.25)) if s.dropna().size else np.nan
        q3 = float(s.quantile(0.75)) if s.dropna().size else np.nan
        iqr = q3 - q1 if pd.notna(q3) and pd.notna(q1) else np.nan

        t1, t2, t3, t4 = st.columns(4)
        with t1:
            st.markdown(f"<div class='card'><b>Mean</b><br>{desc.get('mean', np.nan):.4g}</div>", unsafe_allow_html=True)
        with t2:
            st.markdown(f"<div class='card'><b>Std</b><br>{desc.get('std', np.nan):.4g}</div>", unsafe_allow_html=True)
        with t3:
            st.markdown(f"<div class='card'><b>Median</b><br>{desc.get('50%', np.nan):.4g}</div>", unsafe_allow_html=True)
        with t4:
            st.markdown(f"<div class='card'><b>IQR</b><br>{iqr:.4g}</div>", unsafe_allow_html=True)

        st.markdown("")
        st.markdown("### Distribution (Plotly)")
        fig = px.histogram(
            plot_s.to_frame(name=col),
            x=col,
            nbins=40,
            title=f"Histogram: {col}"
        )
        fig.update_layout(bargap=0.02)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Distribution + KDE (Seaborn)")
        fig2, ax = plt.subplots(figsize=(12, 4))
        sns.histplot(plot_s, bins=40, kde=True, ax=ax)
        ax.set_title(f"Histogram + KDE: {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Count")
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        st.pyplot(fig2, clear_figure=True)
        plt.close(fig2)

        st.markdown("### Boxplot (Outlier view)")
        fig3, ax3 = plt.subplots(figsize=(12, 2.5))
        sns.boxplot(x=plot_s, ax=ax3)
        ax3.set_title(f"Boxplot: {col}")
        ax3.set_xlabel(col)
        ax3.grid(axis="x", linestyle="--", alpha=0.3)
        st.pyplot(fig3, clear_figure=True)
        plt.close(fig3)

    # -------------------------
    # Categorical / text analysis
    # -------------------------
    else:
        st.markdown("### Frequency analysis")

        top_k = st.slider("Top K categories", 5, 50, 15, 1)
        vc = s.fillna("NaN").astype(str).value_counts().head(top_k)
        freq_df = vc.reset_index()
        freq_df.columns = ["category", "count"]

        st.dataframe(freq_df, use_container_width=True)

        st.markdown("### Bar chart (Plotly)")
        fig = px.bar(freq_df, x="category", y="count", title=f"Top {top_k} categories: {col}")
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Bar chart (Matplotlib)")
        fig2, ax = plt.subplots(figsize=(12, 5))
        ax.bar(freq_df["category"], freq_df["count"], color="#1f2937", edgecolor="black", linewidth=0.6)
        ax.set_title(f"Top {top_k} categories: {col}", fontsize=14, fontweight="bold")
        ax.set_xlabel("Category")
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        st.pyplot(fig2, clear_figure=True)
        plt.close(fig2)

    st.markdown("")
    st.markdown("### Raw preview (first 50 non-null values)")
    st.write(s.dropna().head(50).tolist())
