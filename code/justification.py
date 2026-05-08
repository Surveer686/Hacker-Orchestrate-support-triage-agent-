from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from decision import Decision
from utils import RankedDoc


@dataclass(frozen=True)
class Justification:
    text: str


def build_justification(
    cleaned: str,
    classification_keywords: List[str],
    risk: str,
    risk_keywords: List[str],
    top_doc: Optional[RankedDoc],
    decision: Decision,
    similarity_threshold: float,
) -> Justification:
    detected = sorted(set((classification_keywords or []) + (risk_keywords or [])))
    detected_part = ", ".join([f"'{k}'" for k in detected]) if detected else "none"

    sim = top_doc.cosine_similarity if top_doc else 0.0
    sim_part = f"{sim:.4f}"

    if decision.status == "invalid":
        txt = (
            f"Detected keywords: {detected_part}. "
            f"Risk level: {risk}. Similarity: {sim_part}. "
            "Input did not meet minimum quality/length requirements → marked invalid."
        )
        return Justification(text=txt)

    if decision.status == "escalated":
        txt = (
            f"Detected keywords: {detected_part}. "
            f"Risk level: {risk}. Similarity: {sim_part} (threshold={similarity_threshold:.2f}). "
            f"Escalated because {decision.reason}."
        )
        return Justification(text=txt)

    txt = (
        f"Detected keywords: {detected_part}. "
        f"Risk level: {risk}. Matched support document with similarity={sim_part} "
        f"(threshold={similarity_threshold:.2f}) → safe to respond."
    )
    return Justification(text=txt)

