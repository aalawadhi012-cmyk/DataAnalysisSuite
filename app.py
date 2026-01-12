import streamlit as st
import importlib.util
from pathlib import Path

from src.components.theme import apply_global_theme
from src.components.layout import header, footer
from src.components.sidebar import render_sidebar


PAGES_DIR = Path(__file__).parent / "src" / "pages"

PAGE_MAP = {
    "01) Data Ingestion": "01_Data_Ingestion.py",
    "02) Overview": "02_Overview.py",
    "03) Missing Values": "03_Missing_Values.py",
    "04) Univariate": "04_Univariate.py",
    "05) Bivariate": "05_Bivariate.py",
    "06) Correlation": "06_Correlation.py",
    "07) Outliers": "07_Outliers.py",
    "08) Preprocessing": "08_Preprocessing.py",
    "09) Export": "09_Export.py",
}


def load_page_module(file_name: str):
    file_path = PAGES_DIR / file_name
    spec = importlib.util.spec_from_file_location(file_name.replace(".py", ""), file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def main():
    st.set_page_config(
        page_title="Data Analysis Suite",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    apply_global_theme()
    header()

    selected = render_sidebar()

    st.markdown("")
    module = load_page_module(PAGE_MAP[selected])

    # كل صفحة يجب أن تحتوي دالة render()
    if hasattr(module, "render"):
        module.render()
    else:
        st.error("Page module missing render() function.")

    footer()


if __name__ == "__main__":
    main()
