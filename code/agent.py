from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from classifier import classify
from decision import decide
from justification import build_justification
from ranker import rank_docs
from response_generator import generate_response
from retriever import TfidfRetriever
from risk_detector import detect_risk
from utils import preprocess_text


@dataclass(frozen=True)
class AgentConfig:
    data_dir: str
    similarity_threshold: float = 0.25
    top_k: int = 3


class SupportTriageAgent:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.retriever = TfidfRetriever(config.data_dir)
        self.retriever.load_and_fit()

    def process_ticket(self, subject: str | None, issue: str | None, company: str | None) -> Dict[str, str]:
        cleaned = preprocess_text(subject, issue)
        raw_input = f"{subject or ''} {issue or ''}".strip()

        cls = classify(cleaned, company)
        risk_res = detect_risk(cleaned)

        retrieval = self.retriever.retrieve(cleaned, top_k=self.config.top_k)
        ranked = rank_docs(cleaned, retrieval.docs) if retrieval.docs else []
        top_doc = ranked[0] if ranked else None
        top_similarity = top_doc.cosine_similarity if top_doc else None

        dec = decide(
            risk=risk_res.risk,
            has_docs=bool(ranked),
            top_similarity=top_similarity,
            product_area=cls.product_area,
            request_type=cls.request_type,
            similarity_threshold=self.config.similarity_threshold,
        )

        response = generate_response(dec.status, cleaned, top_doc)
        justification = build_justification(
            cleaned=cleaned,
            classification_keywords=cls.detected_keywords,
            risk=risk_res.risk,
            risk_keywords=risk_res.detected_keywords,
            top_doc=top_doc,
            decision=dec,
            similarity_threshold=self.config.similarity_threshold,
        ).text

        return {
            "status": dec.status,
            "product_area": cls.product_area,
            "response": response,
            "justification": justification,
            "request_type": cls.request_type,
            "_raw_input": raw_input,
            "_cleaned": cleaned,
            "_risk": risk_res.risk,
            "_top_doc_path": top_doc.path if top_doc else "",
            "_top_doc_score": f"{top_doc.cosine_similarity:.4f}" if top_doc else "",
            "_decision_reason": dec.reason,
        }

