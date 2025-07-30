"""
core.py
~~~~~~~
Asynchronous helpers for resolving ISSN <--> ISSN-L via the ISSN Portal API.

Forward  lookup: async_lookup(...)
Reverse  lookup: async_lookup_reverse(...)

Both helpers share the same semaphore-based rate-limiter and progress bar.
"""

from __future__ import annotations

import asyncio
import time
import re
from typing import Iterable, Dict, List, Tuple, Optional

import aiohttp

try:
    # fancy progress bar (falls back to quiet mode if not installed)
    from tqdm import tqdm
except ImportError:  # pragma: no cover
    tqdm = None

# --------------------------------------------------------------------------- #
API_ISSN   = "https://portal.issn.org/resource/ISSN/{code}?format=json"
API_ISSNL  = "https://portal.issn.org/resource/ISSN-L/{code}?format=json"
ISSN_RE    = re.compile(r"\d{4}-\d{3}[\dX]")         # matches 0000-0000 or 0000-000X
USER_AGENT = "issnresolver/0.1 (async aiohttp client)"
# --------------------------------------------------------------------------- #


# ==========  low-level fetchers  ========================================== #
async def _fetch_issnl_from_issn(code: str,
                                 sem: asyncio.Semaphore,
                                 session: aiohttp.ClientSession) -> Tuple[str, Optional[str]]:
    """
    Given an ISSN/EISSN, return (code, ISSN-L or None)
    """
    async with sem:
        async with session.get(API_ISSN.format(code=code), timeout=10) as resp:
            if resp.status == 200 and (text := await resp.text()):
                if m := ISSN_RE.search(text):
                    return code, m.group(0)
    return code, None


async def _fetch_issns_from_issnl(issnl: str,
                                  sem: asyncio.Semaphore,
                                  session: aiohttp.ClientSession) -> Tuple[str, List[str]]:
    """
    Given an ISSN-L, return (issnl, [all related ISSN/EISSN codes])
    """
    async with sem:
        async with session.get(API_ISSNL.format(code=issnl), timeout=10) as resp:
            if resp.status == 200:
                try:
                    data = await resp.json(content_type=None)
                except Exception:  # pragma: no cover
                    return issnl, []

                # Extract all "@id": ".../ISSN/0000-0000" occurrences
                issn_codes: set[str] = set()
                def _recurse(obj):
                    if isinstance(obj, dict):
                        if "@id" in obj and "/ISSN/" in obj["@id"]:
                            code = obj["@id"].split("/ISSN/")[-1]
                            if ISSN_RE.fullmatch(code):
                                issn_codes.add(code)
                        for v in obj.values():
                            _recurse(v)
                    elif isinstance(obj, list):
                        for v in obj:
                            _recurse(v)

                _recurse(data)
                return issnl, sorted(issn_codes)
    return issnl, []


# ==========  generic bulk runner  ========================================= #
async def _bulk_runner(
    items: Iterable[str],
    worker_func,
    workers: int = 10,
    rps_cap: int = 5
) -> Dict[str, object]:
    """
    Generic async executor with naïve requests-per-second cap.
    Returns dict keyed by original code.
    """
    sem   = asyncio.Semaphore(workers)
    found: dict[str, object] = {}
    start = time.perf_counter()

    connector = aiohttp.TCPConnector(limit=workers * 2, limit_per_host=workers)
    async with aiohttp.ClientSession(connector=connector,
                                     headers={"User-Agent": USER_AGENT}) as session:

        coros = [worker_func(code, sem, session) for code in items]
        bar   = tqdm(total=len(items), desc=f"Async×{workers}") if tqdm else None

        for coro in asyncio.as_completed(coros):
            code, result = await coro
            if result:
                found[code] = result
            if bar:
                bar.update(1)

            # crude rate-limit
            if rps_cap:
                done     = bar.n if bar else len(found)
                elapsed  = time.perf_counter() - start
                curr_rps = done / max(elapsed, 0.01)
                if curr_rps > rps_cap:
                    await asyncio.sleep(max(0, (done / rps_cap) - elapsed))

        if bar:
            bar.close()

    return found


# ==========  public helpers  ============================================== #
def async_lookup(
    codes: Iterable[str],
    workers: int = 10,
    rps_cap: int = 5
) -> Dict[str, str]:
    """
    Resolve *unique* ISSN/EISSN codes → ISSN-L.
    Automatically handles both normal scripts and Jupyter notebooks.
    """
    unique = sorted(set(codes))
    try:
        return asyncio.run(_bulk_runner(unique, _fetch_issnl_from_issn, workers, rps_cap))
    except RuntimeError as e:
        if "asyncio.run() cannot be called" in str(e):
            # Likely running inside a Jupyter notebook
            try:
                import nest_asyncio
                nest_asyncio.apply()
                loop = asyncio.get_running_loop()
                return loop.run_until_complete(
                    _bulk_runner(unique, _fetch_issnl_from_issn, workers, rps_cap)
                )
            except ImportError:
                raise RuntimeError(
                    "You're running in a notebook and need `nest_asyncio`. "
                    "Install it with `pip install nest_asyncio`"
                )
        else:
            raise


def async_lookup_reverse(
    issnls: Iterable[str],
    workers: int = 10,
    rps_cap: int = 5
) -> Dict[str, List[str]]:
    """
    Resolve ISSN-L codes → list of all related ISSN/EISSN.
    Automatically handles both normal scripts and Jupyter notebooks.
    """
    unique = sorted(set(issnls))
    try:
        return asyncio.run(_bulk_runner(unique, _fetch_issns_from_issnl, workers, rps_cap))
    except RuntimeError as e:
        if "asyncio.run() cannot be called" in str(e):
            try:
                import nest_asyncio
                nest_asyncio.apply()
                loop = asyncio.get_running_loop()
                return loop.run_until_complete(
                    _bulk_runner(unique, _fetch_issns_from_issnl, workers, rps_cap)
                )
            except ImportError:
                raise RuntimeError(
                    "You're running in a notebook and need `nest_asyncio`. "
                    "Install it with `pip install nest_asyncio`"
                )
        else:
            raise


# --------------------------------------------------------------------------- #
__all__: list[str] = [
    "async_lookup",
    "async_lookup_reverse",
]
