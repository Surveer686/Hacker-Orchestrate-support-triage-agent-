from __future__ import annotations

from typing import Optional

from utils import RankedDoc, split_into_sentences


ESCALATION_MESSAGE = (
    "This issue involves a sensitive or high-risk scenario and has been escalated to a human support agent."
)

INVALID_MESSAGE = "Your request could not be processed because it did not contain enough information."


def _best_sentence_from_doc(cleaned_query: str, doc: RankedDoc) -> str:
    sentences = split_into_sentences(doc.text)
    if not sentences:
        return "Please refer to the relevant support documentation for the next steps."

    q_tokens = set(cleaned_query.split(" "))
    best = sentences[0]
    best_score = -1
    for s in sentences:
        s_lower = s.lower()
        overlap = sum(1 for t in q_tokens if t and t in s_lower)
        if overlap > best_score:
            best = s.strip()
            best_score = overlap

    # Keep concise.
    if len(best) > 350:
        return best[:347].rstrip() + "..."
    return best


def generate_response(status: str, cleaned_query: str, top_doc: Optional[RankedDoc]) -> str:
    if status == "invalid":
        return INVALID_MESSAGE
    if status == "escalated":
        return ESCALATION_MESSAGE
    if not top_doc:
        return ESCALATION_MESSAGE
    return _best_sentence_from_doc(cleaned_query, top_doc)

