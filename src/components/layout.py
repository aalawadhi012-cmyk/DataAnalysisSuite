import streamlit as st


def header():
    left, right = st.columns([0.75, 0.25], vertical_alignment="center")

    with left:
        st.markdown(
            """
            <div class="card">
              <div style="display:flex; gap:12px; align-items:center;">
                <div style="
                    width:44px;
                    height:44px;
                    border-radius:14px;
                    background: linear-gradient(135deg,
                        rgba(124,58,237,0.9),
                        rgba(59,130,246,0.6));
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    border:1px solid rgba(255,255,255,0.12);
                ">
                  <span style="font-weight:800;">DA</span>
                </div>
                <div>
                  <div style="font-size:20px;font-weight:800;line-height:1.1;">
                    Data Analysis Suite
                  </div>
                  <div class="muted" style="font-size:13px;">
                    EDA • Visualization • Preprocessing • Export
                  </div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # Session status (dynamic)
    # =========================
    df = st.session_state.get("df", None)
    meta = st.session_state.get("meta", {}) or {}

    if df is None:
        status_line = "No file loaded"
        detail_line = "Upload a dataset to start"
    else:
        rows, cols = df.shape
        # Optional: show filename if you store it in meta during upload (recommended)
        fname = meta.get("source_name") or meta.get("filename") or "Dataset"
        status_line = f"Loaded"
        detail_line = f"{fname} • {rows:,} rows × {cols:,} cols"

    with right:
        st.markdown(
            f"""
            <div class="card">
              <div class="muted" style="font-size:12px;">Session</div>
              <div style="font-weight:700;font-size:14px;">Ready</div>
              <div class="muted" style="font-size:12px;">{status_line}</div>
              <div class="muted" style="font-size:12px; margin-top:4px;">{detail_line}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height:14px;'></div>", unsafe_allow_html=True)


def footer():
    st.markdown(
        """
        <hr/>
        <div class="muted" style="font-size:12px; text-align:center;">
          Data Analysis Suite • Streamlit UI • Modular Architecture
        </div>
        """,
        unsafe_allow_html=True
    )
