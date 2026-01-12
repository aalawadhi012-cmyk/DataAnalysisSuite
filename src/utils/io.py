from __future__ import annotations

import pandas as pd
import chardet
from io import BytesIO
from typing import Tuple, Optional, Dict, Any


def _detect_encoding(file_bytes: bytes) -> str:
    """
    Best-effort encoding detection for CSV bytes.
    Defaults to utf-8 if detection is uncertain.
    """
    try:
        result = chardet.detect(file_bytes[:200_000])  # sample first 200KB
        enc = (result.get("encoding") or "utf-8").lower()
        return enc
    except Exception:
        return "utf-8"


def load_dataset(uploaded_file) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Load dataset from Streamlit uploaded_file (CSV / Excel / Parquet).
    Returns (df, meta)
    """
    name = uploaded_file.name
    suffix = name.split(".")[-1].lower()

    meta: Dict[str, Any] = {
        "file_name": name,
        "file_type": suffix,
        "encoding": None,
        "rows": None,
        "cols": None,
    }

    if suffix in ("csv", "txt"):
        raw = uploaded_file.getvalue()
        enc = _detect_encoding(raw)
        meta["encoding"] = enc

        try:
            df = pd.read_csv(BytesIO(raw), encoding=enc, low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(BytesIO(raw), encoding="utf-8", low_memory=False)
        except Exception:
            df = pd.read_csv(BytesIO(raw), encoding="latin-1", low_memory=False)

    elif suffix in ("xlsx", "xls"):
        xls = pd.ExcelFile(uploaded_file)
        sheet = xls.sheet_names[0]
        meta["sheet"] = sheet
        df = pd.read_excel(xls, sheet_name=sheet)

    elif suffix == "parquet":
        df = pd.read_parquet(uploaded_file)

    else:
        raise ValueError(f"Unsupported file type: .{suffix}")

    meta["rows"], meta["cols"] = df.shape
    return df, meta


def set_dataframe_in_session(df: pd.DataFrame, meta: Dict[str, Any], session_state) -> None:
    session_state["df"] = df
    session_state["df_meta"] = meta


def get_dataframe_from_session(session_state) -> Tuple[Optional[pd.DataFrame], Optional[Dict[str, Any]]]:
    return session_state.get("df"), session_state.get("df_meta")
