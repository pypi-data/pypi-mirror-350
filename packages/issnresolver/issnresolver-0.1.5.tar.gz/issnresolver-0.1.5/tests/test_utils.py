# tests/test_utils.py
"""
Unit tests for issnresolver.utils

These tests are 100 % offline:
• `clean_issn` is deterministic.
• `fill_missing_issnl_fast` is tested with `async_lookup` monkey-patched
  so no HTTP requests are made.
"""

import pandas as pd
import pytest

from issnresolver.utils import clean_issn, fill_missing_issnl_fast


# --------------------------------------------------------------------------- #
# clean_issn ---------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "raw, expected",
    [
        ("12345678",  "1234-5678"),      # plain 8-digits
        ("1234 567x", "1234-567X"),      # lowercase x + space
        ("1234-5678", "1234-5678"),      # NBSP/thin space etc.
        (" 1234-5678 ", "1234-5678"),    # leading / trailing spaces
        ("invalid",    None),            # bad code → None
        (None,         None),            # None → None
    ],
)
def test_clean_issn_normalises(raw, expected):
    assert clean_issn(raw) == expected


# --------------------------------------------------------------------------- #
# fill_missing_issnl_fast ---------------------------------------------------- #
# --------------------------------------------------------------------------- #
def test_fill_missing_issnl_fast(monkeypatch):
    """
    Ensure ISSN-L gaps are filled using the mocked async_lookup map.
    """
    df = pd.DataFrame(
        {
            "title":  ["Journal A", "Journal B"],
            "issn":   ["1234-5678", "8765-4321"],
            "eissn":  ["1557-7317", None],
            "issn_l": [None, None],
        }
    )

    # Fake network resolution table
    fake_map = {
        "1234-5678": "1234-5678",
        "1557-7317": "1234-5678",
        "8765-4321": "8765-4321",
    }

    # Monkey-patch utils.async_lookup so no HTTP happens
    import issnresolver.utils as utils_mod
    monkeypatch.setattr(utils_mod, "async_lookup", lambda *a, **kw: fake_map)

    filled = fill_missing_issnl_fast(df, quiet=True)

    # All gaps should now be filled
    assert filled["issn_l"].notna().all()
    assert filled.loc[0, "issn_l"] == "1234-5678"
    assert filled.loc[1, "issn_l"] == "8765-4321"