import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from src.utils.io import get_dataframe_from_session


def render():
    st.subheader("05) Bivariate Analysis")
    st.markdown(
        '<div class="muted">Analyze relationships between two variables.</div>',
        unsafe_allow_html=True
    )
    st.markdown("")

    df, _ = get_dataframe_from_session(st.session_state)
    if df is None:
        st.markdown('<div class="card">No dataset loaded.</div>', unsafe_allow_html=True)
        return

    # -------------------------
    # Variable selection
    # -------------------------
    col1, col2 = st.columns(2)
    with col1:
        x_col = st.selectbox("Select X variable", df.columns.tolist(), index=0)
    with col2:
        y_col = st.selectbox("Select Y variable", df.columns.tolist(), index=1)

    if x_col == y_col:
        st.warning("Please select two different variables.")
        return

    x = df[x_col]
    y = df[y_col]

    x_num = pd.api.types.is_numeric_dtype(x)
    y_num = pd.api.types.is_numeric_dtype(y)

    plot_df = df[[x_col, y_col]].dropna()

    st.markdown("")

    # =========================
    # Numeric × Numeric
    # =========================
    if x_num and y_num:
        st.markdown("### Numeric × Numeric")

        # Correlation
        pearson = plot_df[x_col].corr(plot_df[y_col], method="pearson")
        spearman = plot_df[x_col].corr(plot_df[y_col], method="spearman")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"<div class='card'><b>Pearson</b><br>{pearson:.4f}</div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='card'><b>Spearman</b><br>{spearman:.4f}</div>", unsafe_allow_html=True)

        st.markdown("")

        # Scatter (Plotly)
        fig = px.scatter(
            plot_df,
            x=x_col,
            y=y_col,
            title=f"Scatter: {x_col} vs {y_col}",
            opacity=0.7
        )
        st.plotly_chart(fig, use_container_width=True)

        # Scatter + regression (Seaborn)
        fig2, ax = plt.subplots(figsize=(10, 4))
        sns.regplot(x=x_col, y=y_col, data=plot_df, ax=ax, scatter_kws={"alpha": 0.6})
        ax.set_title(f"{x_col} vs {y_col} (Trend)")
        ax.grid(True, linestyle="--", alpha=0.3)
        st.pyplot(fig2, clear_figure=True)
        plt.close(fig2)

    # =========================
    # Numeric × Categorical
    # =========================
    elif x_num and not y_num or (not x_num and y_num):
        st.markdown("### Numeric × Categorical")

        if x_num:
            num_col, cat_col = x_col, y_col
        else:
            num_col, cat_col = y_col, x_col

        st.markdown(f"**Numeric:** {num_col}  |  **Categorical:** {cat_col}")

        # Boxplot
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.boxplot(x=cat_col, y=num_col, data=plot_df, ax=ax)
        ax.set_title(f"{num_col} by {cat_col}")
        ax.tick_params(axis="x", rotation=45)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        st.pyplot(fig, clear_figure=True)
        plt.close(fig)

        # Aggregated statistics
        st.markdown("### Grouped statistics")
        stats = (
            plot_df
            .groupby(cat_col)[num_col]
            .agg(["count", "mean", "median", "std"])
            .reset_index()
        )
        st.dataframe(stats, use_container_width=True)

    # =========================
    # Categorical × Categorical
    # =========================
    else:
        st.markdown("### Categorical × Categorical")

        ctab = pd.crosstab(x, y)
        st.markdown("### Contingency table")
        st.dataframe(ctab, use_container_width=True)

        # Bar chart
        fig = ctab.plot(kind="bar", figsize=(10, 5))
        plt.title(f"{x_col} vs {y_col}")
        plt.ylabel("Count")
        plt.xlabel(x_col)
        plt.grid(axis="y", linestyle="--", alpha=0.3)
        st.pyplot(plt.gcf(), clear_figure=True)
        plt.close()
