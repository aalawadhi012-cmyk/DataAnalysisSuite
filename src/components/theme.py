import streamlit as st


def apply_global_theme():
    st.markdown(
        """
        <style>
        /* ===============================
           FIX HEADER / CONTENT OVERLAP
           =============================== */

        /* Safe spacing from top (prevents overlap with header) */
        .block-container {
            max-width: 1200px;
            padding-top: 3rem;      /* ↑ increased */
            padding-bottom: 2rem;
        }

        /* Prevent margin collapsing for first element */
        .block-container > div:first-child {
            margin-top: 0.75rem;
        }

        /* ===============================
           SIDEBAR
           =============================== */
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(255,255,255,0.06);
        }

        [data-testid="stSidebar"] > div {
            padding-top: 1rem;
        }

        /* ===============================
           TYPOGRAPHY
           =============================== */
        h1, h2, h3 {
            letter-spacing: -0.02em;
        }

        .muted {
            color: rgba(229,231,235,0.7);
        }

        /* ===============================
           CARDS
           =============================== */
        .card {
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.03);
            border-radius: 16px;
            padding: 16px 18px;
        }

        .card:hover {
            border-color: rgba(124,58,237,0.45);
        }

        /* ===============================
           BADGES
           =============================== */
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 12px;
            border: 1px solid rgba(255,255,255,0.10);
            background: rgba(124,58,237,0.12);
        }

        /* ===============================
           DIVIDERS
           =============================== */
        hr {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.08);
            margin: 1rem 0;
        }

        /* ===============================
           BUTTONS
           =============================== */
        button,
        button[kind="primary"] {
            border-radius: 12px !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
