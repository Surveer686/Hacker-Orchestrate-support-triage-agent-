from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


class TraceLogger:
    def __init__(self, path: str):
        self.path = path

    def log_block(self, block: str) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(block.rstrip() + "\n\n")


def format_trace(
    raw_input: str,
    cleaned: str,
    request_type: str,
    product_area: str,
    risk: str,
    top_doc_path: Optional[str],
    top_doc_score: Optional[float],
    decision: str,
    justification: str,
    response: str,
) -> str:
    score_str = f"{top_doc_score:.4f}" if top_doc_score is not None else "N/A"
    doc_str = top_doc_path or "N/A"
    return (
        f"Input: {raw_input}\n"
        f"Cleaned: {cleaned}\n"
        f"Type: {request_type}\n"
        f"Product: {product_area}\n\n"
        f"Risk: {risk}\n"
        f"Top Doc: {doc_str}\n"
        f"Top Doc Score: {score_str}\n"
        f"Decision: {decision}\n"
        f"Justification: {justification}\n"
        f"Response: {response}\n"
    )

