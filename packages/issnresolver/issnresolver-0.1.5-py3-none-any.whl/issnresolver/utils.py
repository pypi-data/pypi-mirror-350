"""
utils.py
~~~~~~~~
Utility helpers built on top of the async engine in `core.py`.

Public helpers
--------------

clean_issn(code)                → str | None
    Normalise raw ISSN/EISSN to canonical 0000-0000 format.

fill_missing_issnl_fast(df, *)  → pd.DataFrame
    Vectorised helper that:
      1. Collects every missing ISSN-L row in `df`
      2. Looks up ISSN-L for any ISSN/EISSN present
      3. Returns a **copy** of `df` with as many ISSN-L gaps filled as possible
"""

from __future__ import annotations

import re
from typing import Optional, List, Union

import pandas as pd

from .core import async_lookup           # forward lookup ISSN → ISSN-L

# --------------------------------------------------------------------------- #
_ISSN_RE = re.compile(r"^\d{4}-\d{3}[\dX]$")


def _clean_single_issn(code: str | None) -> Optional[str]:
    """
    Normalise a single ISSN/EISSN string to canonical '0000-0000' form.
    """
    if not code or not isinstance(code, str):
        return None

    # Remove spaces, thin-space U+200A, zero-width etc.
    code = (
        code.replace("\u200a", "")
            .replace("\u200b", "")
            .replace(" ", "")
            .upper()
            .strip()
    )

    if "-" not in code and len(code) == 8:          # 12345678 → 1234-5678
        code = f"{code[:4]}-{code[4:]}"
    if _ISSN_RE.match(code):
        return code
    return None


def clean_issn(code: Union[str, List[str], None]) -> Union[str, List[str], None]:
    """
    Normalise an ISSN/EISSN string or a list of such strings to canonical '0000-0000' form.

    Examples
    --------
    >>> clean_issn("12345678")
    '1234-5678'
    >>> clean_issn("1234-567x")
    '1234-567X'
    >>> clean_issn(["12345678", "1234-567x"])
    ['1234-5678', '1234-567X']
    >>> clean_issn(None)
    None
    """
    if code is None:
        return None

    if isinstance(code, list):
        return [_clean_single_issn(c) for c in code]
    else:
        return _clean_single_issn(code)


# --------------------------------------------------------------------------- #
def _collect_issns(rows: pd.DataFrame) -> List[str]:
    """Return all unique, cleaned ISSNs from a frame slice."""
    issns = (
        rows[["issn", "eissn"]]
        .stack()           # → Series
        .map(clean_issn)   # normalise
        .dropna()
        .unique()
    )
    return list(issns)


def fill_missing_issnl_fast(
    df: pd.DataFrame,
    *,
    workers: int = 10,
    rps_cap: int = 5,
    quiet: bool = False,
) -> pd.DataFrame:
    """
    Asynchronously fill missing `issn_l` values in **df**.

    Parameters
    ----------
    df : pd.DataFrame
        Must contain columns: 'issn', 'eissn', 'issn_l'
    workers : int, default 10
        Concurrent HTTP requests
    rps_cap : int, default 5
        Naïve requests-per-second cap (0 = unlimited)
    quiet : bool, default False
        Suppress progress / info prints

    Returns
    -------
    pd.DataFrame
        *Copy* of the input with new ISSN-L values populated.
    """
    if not {"issn", "eissn", "issn_l"} <= set(df.columns):
        raise ValueError("DataFrame must contain 'issn', 'eissn', and 'issn_l' columns.")

    out = df.copy()

    missing_mask = out["issn_l"].isna()
    if missing_mask.sum() == 0:
        if not quiet:
            print("fill_missing_issnl_fast: no gaps found – nothing to do.")
        return out

    to_lookup = _collect_issns(out.loc[missing_mask])
    if not quiet:
        print(f"fill_missing_issnl_fast: querying {len(to_lookup)} ISSNs …")

    lookup_map = async_lookup(to_lookup, workers=workers, rps_cap=rps_cap)
    if not quiet:
        print(f"fill_missing_issnl_fast: resolved {len(lookup_map)} ISSN-L values.")

    # Preserve pre-existing links, overwrite only NaNs
    def _resolve(row):
        if pd.notna(row["issn_l"]):
            return row["issn_l"]
        for code in (row.get("issn"), row.get("eissn")):
            if issnl := lookup_map.get(clean_issn(code)):
                return issnl
        return None

    before = out["issn_l"].notna().sum()
    out.loc[missing_mask, "issn_l"] = out.loc[missing_mask].apply(_resolve, axis=1)
    filled = out["issn_l"].notna().sum() - before

    if not quiet:
        print(f"fill_missing_issnl_fast: filled {filled}/{missing_mask.sum()} gaps.")

    return out


# --------------------------------------------------------------------------- #
__all__: list[str] = [
    "clean_issn",
    "fill_missing_issnl_fast",
]