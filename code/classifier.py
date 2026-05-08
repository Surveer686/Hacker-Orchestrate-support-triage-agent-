from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Set, Tuple

from utils import keyword_set, tokenize


VALID_COMPANIES = {
    "visa_fraud",
    "visa_billing",
    "hackerrank_assessment",
    "authentication",
    "claude",
}


REQUEST_TYPE_KEYWORDS = {
    "bug": {"error", "failed", "not", "working", "crash"},
    "feature_request": {"add", "feature", "improve"},
}


PRODUCT_AREA_RULES: List[Tuple[Set[str], str]] = [
    ({"fraud", "unauthorized"}, "visa_fraud"),
    ({"card", "charged", "refund", "billing"}, "visa_billing"),
    ({"test", "assessment"}, "hackerrank_assessment"),
    ({"login", "password"}, "authentication"),
    ({"claude", "ai"}, "claude"),
]


@dataclass(frozen=True)
class Classification:
    request_type: str
    product_area: str
    detected_keywords: List[str]


def _is_invalid(cleaned: str) -> bool:
    toks = tokenize(cleaned)
    if not cleaned:
        return True
    if len(cleaned) < 8:
        return True
    if len(toks) < 2:
        return True
    # "nonsense / irrelevant" heuristic: high proportion of non-alpha tokens after preprocessing
    alpha_tokens = [t for t in toks if any(ch.isalpha() for ch in t)]
    if len(alpha_tokens) == 0:
        return True
    if len(alpha_tokens) / max(1, len(toks)) < 0.5:
        return True
    return False


def classify_request_type(cleaned: str) -> Tuple[str, List[str]]:
    if _is_invalid(cleaned):
        return "invalid", []

    kws = keyword_set(cleaned)
    bug_hits = sorted(kws.intersection(REQUEST_TYPE_KEYWORDS["bug"]))
    feat_hits = sorted(kws.intersection(REQUEST_TYPE_KEYWORDS["feature_request"]))

    # Weighted keyword logic (deterministic): bug outranks feature_request when both present.
    if bug_hits:
        return "bug", bug_hits
    if feat_hits:
        return "feature_request", feat_hits
    return "product_issue", []


def classify_product_area(cleaned: str, company: Optional[str]) -> Tuple[str, List[str]]:
    if company:
        c = company.strip().lower()
        if c in VALID_COMPANIES:
            return c, [c]

    kws = keyword_set(cleaned)
    for rule_keywords, area in PRODUCT_AREA_RULES:
        hits = sorted(kws.intersection(rule_keywords))
        if hits:
            return area, hits
    return "unknown", []


def classify(cleaned: str, company: Optional[str]) -> Classification:
    request_type, rt_hits = classify_request_type(cleaned)
    product_area, pa_hits = classify_product_area(cleaned, company)
    detected = sorted(set(rt_hits + pa_hits))
    return Classification(request_type=request_type, product_area=product_area, detected_keywords=detected)

