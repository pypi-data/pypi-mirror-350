"""
issnresolver
~~~~~~~~~~~~
Fast, asynchronous ISSN ↔ ISSN-L resolution via the ISSN Portal API.

Public API
----------
- async_lookup(codes, workers=10, rps_cap=5)
      Resolve a list of ISSN/EISSN codes → ISSN-L.

- async_lookup_reverse(codes, workers=10, rps_cap=5)          # optional
      Resolve a list of ISSN-L codes → all related ISSNs/EISSNs
      (exported only if you implemented the reverse lookup).

- clean_issn(code)
      Normalise an ISSN string to 0000-0000 format.

- fill_missing_issnl_fast(df, workers=10, rps_cap=5)
      Vectorised helper to fill missing ISSN-L values in a Pandas DataFrame.

"""

from .version import __version__        # semantic version string
from .core import async_lookup          # main async ISSN → ISSN-L resolver
from .utils import clean_issn, fill_missing_issnl_fast

# Export reverse lookup only if you added it
try:
    from .core import async_lookup_reverse   # noqa: F401
except ImportError:  # pragma: no cover
    async_lookup_reverse = None              # makes hasattr checks easier

# ---------------------------------------------------------------------- #
__all__: list[str] = [
    "__version__",
    "async_lookup",
    "clean_issn",
    "fill_missing_issnl_fast",
]

if async_lookup_reverse is not None:
    __all__.append("async_lookup_reverse")
# ---------------------------------------------------------------------- #
