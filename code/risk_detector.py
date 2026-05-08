from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set, Tuple

from utils import keyword_set


HIGH_RISK = {"fraud", "unauthorized", "hacked", "stolen"}
MEDIUM_RISK = {"charged", "billing", "refund"}


@dataclass(frozen=True)
class RiskResult:
    risk: str  # HIGH / MEDIUM / LOW
    detected_keywords: List[str]


def detect_risk(cleaned: str) -> RiskResult:
    kws = keyword_set(cleaned)
    high_hits = sorted(kws.intersection(HIGH_RISK))
    if high_hits:
        return RiskResult(risk="HIGH", detected_keywords=high_hits)

    med_hits = sorted(kws.intersection(MEDIUM_RISK))
    if med_hits:
        return RiskResult(risk="MEDIUM", detected_keywords=med_hits)

    return RiskResult(risk="LOW", detected_keywords=[])

