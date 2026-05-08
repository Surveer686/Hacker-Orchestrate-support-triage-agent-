from __future__ import annotations

import os
import sys

import pandas as pd

from agent import AgentConfig, SupportTriageAgent
from logger import TraceLogger, format_trace


def _require_file(path: str) -> None:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Required file not found: {path}")


def run(input_csv: str, output_csv: str, data_dir: str, log_path: str) -> None:
    _require_file(input_csv)
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Required corpus directory not found: {data_dir}")

    df = pd.read_csv(input_csv)
    for col in ["subject", "issue"]:
        if col not in df.columns:
            raise ValueError(f"Input CSV must contain column '{col}'")
    if "company" not in df.columns:
        df["company"] = ""

    agent = SupportTriageAgent(AgentConfig(data_dir=data_dir))
    logger = TraceLogger(log_path)

    outputs = []
    # Deterministic order: process in CSV row order.
    for _idx, row in df.iterrows():
        subject = "" if pd.isna(row.get("subject")) else str(row.get("subject"))
        issue = "" if pd.isna(row.get("issue")) else str(row.get("issue"))
        company = "" if pd.isna(row.get("company")) else str(row.get("company"))

        result = agent.process_ticket(subject=subject, issue=issue, company=company)

        outputs.append(
            {
                "status": result["status"],
                "product_area": result["product_area"],
                "response": result["response"],
                "justification": result["justification"],
                "request_type": result["request_type"],
            }
        )

        logger.log_block(
            format_trace(
                raw_input=result["_raw_input"],
                cleaned=result["_cleaned"],
                request_type=result["request_type"],
                product_area=result["product_area"],
                risk=result["_risk"],
                top_doc_path=result["_top_doc_path"] or None,
                top_doc_score=float(result["_top_doc_score"]) if result["_top_doc_score"] else None,
                decision=result["status"],
                justification=result["justification"],
                response=result["response"],
            )
        )

    out_df = pd.DataFrame(outputs, columns=["status", "product_area", "response", "justification", "request_type"])
    out_dir = os.path.dirname(output_csv)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    out_df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_csv = os.path.join(repo_root, "support_tickets", "support_tickets.csv")
    output_csv = os.path.join(repo_root, "support_tickets", "output.csv")
    data_dir = os.path.join(repo_root, "data")
    log_path = os.path.join(repo_root, "log.txt")

    run(input_csv=input_csv, output_csv=output_csv, data_dir=data_dir, log_path=log_path)
