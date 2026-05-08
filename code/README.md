# Code Package

This package implements a deterministic support ticket triage pipeline for classifying, risk-scoring, retrieving relevant documentation, ranking results, and generating either a response or escalation decision.

## Overview

The package is structured as a small inference pipeline:

- `main.py` - entry point for processing ticket CSV data and writing outputs.
- `agent.py` - orchestrates preprocessing, classification, risk detection, retrieval, ranking, decisioning, response generation, and justification.
- `classifier.py` - detects request type and product area from cleaned ticket text.
- `risk_detector.py` - assigns HIGH / MEDIUM / LOW risk labels based on keywords.
- `retriever.py` - loads support corpus documents and performs deterministic TF-IDF retrieval.
- `ranker.py` - sorts retrieved documents by cosine similarity plus keyword overlap bonus.
- `decision.py` - applies escalation rules and decides whether to reply, escalate, or mark invalid.
- `response_generator.py` - produces a concise reply sentence or escalation message.
- `justification.py` - builds a traceable justification string for each ticket result.
- `logger.py` - appends trace logs to a file.
- `utils.py` - shared text preprocessing, tokenization, corpus loading, and helper models.

## Dependencies

The package depends on:

- `pandas`
- `scikit-learn`

Install requirements for the project root, for example:

```bash
pip install -r ../requirements.txt
```

## Usage

From the `code/` folder, run:

```bash
python main.py
```

By default, this reads:

- `../support_tickets/support_tickets.csv`
- `../data/`

And writes:

- `../support_tickets/output.csv`
- `../log.txt`

## Custom execution

To run with custom input/output paths:

```bash
python main.py <input_csv> <output_csv> <data_dir> <log_path>
```

Example:

```bash
python main.py ../support_tickets/support_tickets.csv ../support_tickets/output.csv ../data ../log.txt
```

## Behavior

- Cleans and normalizes ticket text by lowercasing and removing punctuation.
- Classifies tickets into request types like `bug`, `feature_request`, `product_issue`, or `invalid`.
- Detects product areas such as `visa_fraud`, `visa_billing`, `hackerrank_assessment`, `authentication`, `claude`, or `unknown`.
- Uses TF-IDF retrieval over `data/` documents and sorts results deterministically.
- Escalates when input is invalid, risk is HIGH, no relevant documents are found, similarity is low, or the product area is unknown.
- Generates a response from the best matched document or a predefined escalation/invalid message.

## Notes

- The package is intentionally deterministic and rule-driven.
- The `data/` corpus should contain `.md` or `.txt` support documents.
- `support_tickets.csv` must include `subject` and `issue` columns. A `company` column is optional.
