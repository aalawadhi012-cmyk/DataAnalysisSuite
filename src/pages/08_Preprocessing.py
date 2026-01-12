import streamlit as st
import pandas as pd
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, MinMaxScaler, RobustScaler
from sklearn.impute import SimpleImputer

from src.utils.io import get_dataframe_from_session, set_dataframe_in_session


def render():
    st.subheader("08) Preprocessing")
    st.markdown(
        '<div class="muted">Prepare data for modeling: imputation, encoding, and scaling using pipelines.</div>',
        unsafe_allow_html=True
    )
    st.markdown("")

    df, meta = get_dataframe_from_session(st.session_state)
    if df is None:
        st.markdown('<div class="card">No dataset loaded.</div>', unsafe_allow_html=True)
        return

    # -------------------------
    # Column selection
    # -------------------------
    num_cols = df.select_dtypes(include="number").columns.tolist()
    cat_cols = [c for c in df.columns if c not in num_cols]

    st.markdown("### Column selection")
    c1, c2 = st.columns(2)
    with c1:
        sel_num = st.multiselect("Numeric columns", num_cols, default=num_cols)
    with c2:
        sel_cat = st.multiselect("Categorical columns", cat_cols, default=cat_cols)

    if not sel_num and not sel_cat:
        st.warning("Select at least one column.")
        return

    # -------------------------
    # Options
    # -------------------------
    st.markdown("### Options")

    o1, o2, o3 = st.columns(3)
    with o1:
        num_impute = st.selectbox("Numeric imputation", ["mean", "median", "constant"], index=0)
        num_const = st.text_input("Numeric constant", value="0")
    with o2:
        cat_impute = st.selectbox("Categorical imputation", ["most_frequent", "constant"], index=0)
        cat_const = st.text_input("Categorical constant", value="Unknown")
    with o3:
        scaler_name = st.selectbox("Scaler", ["StandardScaler", "MinMaxScaler", "RobustScaler", "None"], index=0)

    # -------------------------
    # Build pipelines
    # -------------------------
    num_steps = []
    if sel_num:
        num_steps.append(("imputer", SimpleImputer(strategy=num_impute if num_impute != "constant" else "constant",
                                                    fill_value=float(num_const) if num_impute == "constant" else None)))
        if scaler_name != "None":
            scaler = {
                "StandardScaler": StandardScaler(),
                "MinMaxScaler": MinMaxScaler(),
                "RobustScaler": RobustScaler()
            }[scaler_name]
            num_steps.append(("scaler", scaler))
        num_pipe = Pipeline(steps=num_steps)
    else:
        num_pipe = None

    cat_steps = []
    if sel_cat:
        cat_steps.append(("imputer", SimpleImputer(strategy=cat_impute,
                                                    fill_value=cat_const if cat_impute == "constant" else None)))
        cat_steps.append(("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)))
        cat_pipe = Pipeline(steps=cat_steps)
    else:
        cat_pipe = None

    transformers = []
    if num_pipe and sel_num:
        transformers.append(("num", num_pipe, sel_num))
    if cat_pipe and sel_cat:
        transformers.append(("cat", cat_pipe, sel_cat))

    preprocessor = ColumnTransformer(transformers=transformers, remainder="drop")

    # -------------------------
    # Apply
    # -------------------------
    st.markdown("")
    apply = st.button("Apply preprocessing", type="primary")

    if apply:
        try:
            X = preprocessor.fit_transform(df)
            # Build feature names
            feature_names = []
            if sel_num:
                feature_names.extend(sel_num)
            if sel_cat:
                ohe = preprocessor.named_transformers_["cat"].named_steps["encoder"]
                cat_features = ohe.get_feature_names_out(sel_cat).tolist()
                feature_names.extend(cat_features)

            X_df = pd.DataFrame(X, columns=feature_names)
            new_meta = dict(meta or {})
            new_meta["preprocessing"] = {
                "numeric_cols": sel_num,
                "categorical_cols": sel_cat,
                "num_imputation": num_impute,
                "cat_imputation": cat_impute,
                "scaler": scaler_name,
            }

            set_dataframe_in_session(X_df, new_meta, st.session_state)

            st.success(f"Preprocessing applied. New shape: {X_df.shape}")
            st.markdown("### Preview of processed data")
            st.dataframe(X_df.head(20), use_container_width=True)

            # Download
            csv = X_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download processed CSV",
                data=csv,
                file_name="processed_data.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.exception(e)
