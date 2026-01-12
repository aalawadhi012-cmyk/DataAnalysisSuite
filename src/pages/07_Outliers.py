import streamlit as st
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from src.utils.io import get_dataframe_from_session, set_dataframe_in_session


def detect_outliers_iqr(series):
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return lower, upper


def render():
    st.subheader("07) Outlier Analysis")
    st.markdown(
        '<div class="muted">Detect and handle outliers using the IQR method.</div>',
        unsafe_allow_html=True
    )
    st.markdown("")

    df, meta = get_dataframe_from_session(st.session_state)
    if df is None:
        st.markdown('<div class="card">No dataset loaded.</div>', unsafe_allow_html=True)
        return

    # =========================
    # Column selection
    # =========================
    num_cols = df.select_dtypes(include="number").columns.tolist()
    if not num_cols:
        st.info("No numeric columns available for outlier analysis.")
        return

    col = st.selectbox("Select numeric column", num_cols)

    s = df[col].dropna()

    if s.empty:
        st.warning("Selected column contains only missing values.")
        return

    # =========================
    # IQR computation
    # =========================
    lower, upper = detect_outliers_iqr(s)

    outliers = s[(s < lower) | (s > upper)]
    outlier_ratio = len(outliers) / len(s) * 100

    # =========================
    # Summary cards
    # =========================
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='card'><b>Total values</b><br>{len(s)}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='card'><b>Outliers</b><br>{len(outliers)}</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='card'><b>Outlier %</b><br>{outlier_ratio:.2f}%</div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='card'><b>IQR range</b><br>[{lower:.3g}, {upper:.3g}]</div>", unsafe_allow_html=True)

    # =========================
    # Visualization
    # =========================
    st.markdown("")
    st.markdown("### Boxplot (outlier visualization)")

    fig, ax = plt.subplots(figsize=(10, 3))
    sns.boxplot(x=s, ax=ax)
    ax.set_title(f"Boxplot: {col}")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    st.pyplot(fig, clear_figure=True)
    plt.close(fig)

    # =========================
    # Show outliers
    # =========================
    st.markdown("### Detected outliers (sample)")
    st.write(outliers.sort_values().head(20).tolist())

    # =========================
    # Treatment
    # =========================
    st.markdown("")
    st.markdown("### Treatment")

    action = st.radio(
        "Choose action",
        ["None", "Remove outliers", "Cap (Winsorize)"],
        index=0
    )

    if action != "None":
        apply = st.button("Apply outlier treatment", type="primary")

        if apply:
            new_df = df.copy()

            if action == "Remove outliers":
                mask = (new_df[col] >= lower) & (new_df[col] <= upper)
                new_df = new_df[mask]

            elif action == "Cap (Winsorize)":
                new_df[col] = new_df[col].clip(lower=lower, upper=upper)

            new_meta = dict(meta or {})
            new_meta["outlier_treatment"] = {
                "column": col,
                "method": "IQR",
                "action": action,
                "lower": float(lower),
                "upper": float(upper),
            }

            set_dataframe_in_session(new_df, new_meta, st.session_state)
            st.success(f"Outlier treatment applied. New shape: {new_df.shape}")

    st.markdown("")
    st.markdown("### Preview after action")
    st.dataframe(st.session_state["df"].head(20), use_container_width=True)
