from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Decision:
    status: str  # escalated / replied / invalid
    reason: str


def decide(
    risk: str,
    has_docs: bool,
    top_similarity: Optional[float],
    product_area: str,
    request_type: str,
    similarity_threshold: float,
) -> Decision:
    if request_type == "invalid":
        return Decision(status="invalid", reason="invalid_input")

    # Strict escalation rules
    if risk == "HIGH":
        return Decision(status="escalated", reason="high_risk")

    if product_area == "unknown":
        return Decision(status="escalated", reason="unknown_product_area")

    if not has_docs:
        return Decision(status="escalated", reason="no_relevant_documents")

    if top_similarity is None or top_similarity < similarity_threshold:
        return Decision(status="escalated", reason="low_similarity")

    return Decision(status="replied", reason="safe_to_reply")

