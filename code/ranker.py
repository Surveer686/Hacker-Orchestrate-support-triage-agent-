from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set

from utils import RankedDoc, RetrievedDoc, keyword_set


def rank_docs(cleaned_query: str, docs: List[RetrievedDoc]) -> List[RankedDoc]:
    qk = keyword_set(cleaned_query)

    ranked: List[RankedDoc] = []
    for d in docs:
        doc_lower = d.text.lower()
        overlap = any(kw in doc_lower for kw in qk if kw)
        bonus = 0.2 if overlap else 0.0
        score = float(d.cosine_similarity) + bonus
        ranked.append(
            RankedDoc(
                path=d.path,
                text=d.text,
                cosine_similarity=float(d.cosine_similarity),
                keyword_overlap_bonus=float(bonus),
                score=float(score),
            )
        )

    # Deterministic tie-break: score desc, cosine desc, path asc
    ranked.sort(key=lambda r: (-r.score, -r.cosine_similarity, r.path))
    return ranked

