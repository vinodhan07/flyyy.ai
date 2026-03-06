# ─── Fuzzy Matching Utilities ───
from rapidfuzz import fuzz, process
from typing import List, Optional


def get_best_match(
    target: str, candidates: List[str], threshold: int = 70
) -> Optional[str]:
    """Find the best fuzzy match for *target* among *candidates*."""
    if not target or not candidates:
        return None

    lowered = [c.lower() for c in candidates]
    match = process.extractOne(target.lower(), lowered, scorer=fuzz.WRatio)

    if match and match[1] >= threshold:
        idx = lowered.index(match[0])
        return candidates[idx]

    return None
