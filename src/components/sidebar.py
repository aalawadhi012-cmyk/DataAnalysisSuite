import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="card">
              <div style="font-weight:800;font-size:16px;">Navigation</div>
              <div class="muted" style="font-size:12px;">Select a module</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("")

        module = st.radio(
            label="",
            options=[
                "01) Data Ingestion",
                "02) Overview",
                "03) Missing Values",
                "04) Univariate",
                "05) Bivariate",
                "06) Correlation",
                "07) Outliers",
                "08) Preprocessing",
                "09) Export",
            ],
            index=0
        )

        st.markdown("")
        st.markdown(
            """
            <div class="card">
              <div class="badge">Design</div>
              <div style="margin-top:8px;font-size:13px;" class="muted">
                Dark theme • Cards • Modular pages • Ready for Plotly/Seaborn/Matplotlib
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    return module
