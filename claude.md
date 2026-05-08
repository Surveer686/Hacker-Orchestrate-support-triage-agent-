# 🧠 Multi-Domain Support Triage Agent (TOP 1% BUILD SPEC)

---

# 🚨 CRITICAL RULES (NON-NEGOTIABLE)

- Use ONLY local corpus (`data/`)
- NEVER hallucinate
- ALWAYS escalate high-risk cases
- Deterministic output ONLY (no randomness)
- Every decision MUST be explainable
- Justification must trace back to input + corpus

---

# 🎯 GOAL

Input:
support_tickets/support_tickets.csv

Output:
support_tickets/output.csv

Columns:
status,product_area,response,justification,request_type

---

# 🏗️ ARCHITECTURE (STRICT)


Input
→ Preprocessing
→ Classification
→ Risk Detection
→ Retrieval (TF-IDF)
→ Ranking
→ Decision Engine
→ Response Generation
→ Justification Engine
→ Logging


---

# 📁 PROJECT STRUCTURE


code/
├── main.py
├── agent.py
├── classifier.py
├── risk_detector.py
├── retriever.py
├── ranker.py
├── decision.py
├── response_generator.py
├── justification.py
├── logger.py
└── utils.py


---

# ⚙️ IMPLEMENTATION DETAILS

---

## 1. PREPROCESSING

- Merge `subject + issue`
- Lowercase
- Remove punctuation
- Normalize whitespace

---

## 2. CLASSIFIER (IMPORTANT)

### request_type:

Use weighted keyword logic:

- bug → error, failed, not working, crash
- feature_request → add, feature, improve
- invalid → nonsense / too short / irrelevant
- else → product_issue

---

### product_area:

Priority-based detection:

1. Use `company` if valid
2. Else detect:

| Keywords | Output |
|--------|--------|
| fraud, unauthorized | visa_fraud |
| card, charged, refund | visa_billing |
| test, assessment | hackerrank_assessment |
| login, password | authentication |
| claude, ai | claude |
| else | unknown |

---

## 3. RISK DETECTOR (SCORING CRITICAL)

Return: HIGH / MEDIUM / LOW

- HIGH → fraud, unauthorized, hacked, stolen
- MEDIUM → charged, billing, refund
- LOW → rest

---

## 4. RETRIEVER (TF-IDF BASED)

### MUST IMPLEMENT:

- Load corpus from `data/`
- Convert all documents into TF-IDF vectors
- Convert query into vector
- Compute cosine similarity

---

### OUTPUT:

Return top-k documents (k=3 recommended)

---

## 5. RANKER (NEW 🔥)

Sort retrieved documents by:

score = cosine_similarity + keyword_overlap_bonus

Where:

keyword_overlap_bonus =
+0.2 if query keywords appear in doc

---

## 6. DECISION ENGINE


IF risk == HIGH → escalated
ELSE IF no documents → escalated
ELSE → replied


---

## 7. RESPONSE GENERATOR

### If escalated:

"This issue involves a sensitive or high-risk scenario and has been escalated to a human support agent."

---

### If replied:

- Use top-ranked document
- Extract most relevant sentence
- Keep concise

---

## 8. JUSTIFICATION ENGINE (VERY IMPORTANT 🔥)

Must include:

- detected keywords
- risk level
- similarity score
- why escalated or replied

---

### Example:

"Detected keyword 'unauthorized' → classified as fraud (HIGH risk). Retrieval confidence low → escalated."

OR

"Matched 'test not starting' with support document (similarity=0.82). Safe to respond."

---

## 9. LOGGER

Write to `log.txt`

Include FULL TRACE:

Input: ...
Cleaned: ...
Type: ...
Product: ...

Risk: ...
Top Doc Score: ...
Decision: ...
Justification: ...
Response: ...

---

# 🚨 ESCALATION RULES (STRICT)

MUST ESCALATE IF:

- Fraud / unauthorized
- Billing dispute ambiguity
- Account compromise
- No relevant documents
- Low similarity (< threshold)

---

# ⚠️ EDGE CASES

Handle:

- Multiple intents → choose highest risk
- Garbage input → invalid
- Empty → invalid
- Unknown → escalate

---

# 🧪 TF-IDF IMPLEMENTATION (MANDATORY)

Use:

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
Steps:
Fit vectorizer on corpus
Transform query
Compute similarity
Sort results