HackerRank Orchestra
Deterministic Multi-Domain Support Ticket Triage Agent
Language	Python 3
Stack	scikit-learn · pandas
Interface	Terminal / CLI
LLMs Used	None
Hallucinations	Zero
Deterministic	Yes

Overview
A terminal-based, rule-driven pipeline that classifies, risk-scores, retrieves, ranks, decides, and responds to support tickets across multiple product domains — with full auditability and zero hallucinations. Every decision is explainable and logged.

Domains Covered
–Visa Fraud — Visa Fraud
–Visa Billing — Visa Billing
–HackerRank Assessments — HackerRank Assessments
–Authentication — Authentication
–Claude AI — Claude AI

Pipeline Architecture
The pipeline runs 8 stages in strict sequential order. Same input always produces the same output.

Stage	Description
1. Preprocessing	Lowercase, strip punctuation, normalize whitespace
2. Classification	Detect request type (bug / feature_request / product_issue / invalid) and product area
3. Risk Scoring	Assign HIGH / MEDIUM / LOW label via keyword signals
4. TF-IDF Retrieval	Cosine similarity over local corpus, top-k = 3 documents returned
5. Re-ranking	Sort by cosine similarity + keyword overlap bonus (+0.2)
6. Decision Engine	Apply escalation rules: replied / escalated / invalid
7. Response Generation	Extract best sentence from top-matched corpus document
8. Justification + Logging	Build traceable justification string and append to log.txt

Escalation Rules
The agent escalates — rather than guessing — under the following conditions, evaluated in priority order:
–Request type is invalid
–Risk level is HIGH (e.g. keywords: stolen, fraud, unauthorized)
–Product area is unknown
–No relevant corpus documents retrieved
–Top document similarity is below threshold (default: 0.25)

Project Structure

File	Responsibility
main.py	Entry point — reads input CSV, writes output.csv and log.txt
agent.py	Orchestrates all pipeline stages in order
classifier.py	Detects request type and product area
risk_detector.py	Assigns HIGH / MEDIUM / LOW risk via keyword matching
retriever.py	TF-IDF corpus loading and cosine similarity retrieval
ranker.py	Re-ranks retrieved docs with keyword overlap bonus
decision.py	Applies escalation rule tree, returns decision and reason
response_generator.py	Picks best sentence from top-matched document
justification.py	Builds traceable justification string per ticket
logger.py	Appends full trace blocks to log.txt
utils.py	Shared preprocessing, tokenization, dataclasses

Installation
Requirements
–Python 3.8+
–pip

Install dependencies
pip install -r requirements.txt

requirements.txt contains:
scikit-learn
pandas

Usage
Default execution
From the code/ directory, run:
python main.py

This reads:
–../support_tickets/support_tickets.csv
–../data/  (corpus of .md and .txt support documents)

And writes:
–../support_tickets/output.csv
–../log.txt

Custom paths
python main.py <input_csv> <output_csv> <data_dir> <log_path>

Example:
python main.py ../support_tickets/support_tickets.csv ../support_tickets/output.csv ../data ../log.txt

Input Format
The input CSV must contain the following columns:
–subject  — ticket subject line (required)
–issue  — full ticket description (required)
–company  — company identifier for product area override (optional)

Output Format
The output CSV adds the following columns to each input row:
–status  — replied / escalated / invalid
–response  — generated reply or escalation message
–justification  — traceable reason for the decision

Key Engineering Decisions
–Zero hallucinations — every response is extracted directly from the local corpus. Nothing is generated from thin air.
–Fully deterministic — explicit tie-breaking at every stage (by score, cosine, then file path). Same input always produces the same output.
–Terminal-based — runs with a single command. No UI, no cloud, no external APIs.
–Knows when not to answer — escalates rather than guessing when confidence is low, risk is high, or the domain is unknown.
–Full audit trail — keywords matched, similarity scores, and decision reasons are logged per ticket to log.txt.
–No LLMs required — built entirely on TF-IDF, cosine similarity, and rule-based logic.

Corpus Documents
Place .md or .txt support documents in the data/ directory. The retriever fits a TF-IDF vectorizer over all documents at startup and reuses it for all tickets in the run.

Included corpus files:
–visa_fraud.md
–visa_billing.md
–hackerrank_assessment.md
–authentication.md
–claude_ai.md
–general_routing.txt

Reliable AI does not always need the biggest model. It needs the right architecture, clear rules, and full traceability.