from __future__ import annotations

import os
import re
import string
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Set, Tuple


PUNCT_TRANSLATION = str.maketrans({ch: " " for ch in string.punctuation})


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def preprocess_text(subject: str | None, issue: str | None) -> str:
    merged = f"{subject or ''} {issue or ''}".strip()
    lowered = merged.lower()
    no_punct = lowered.translate(PUNCT_TRANSLATION)
    return normalize_whitespace(no_punct)


def tokenize(text: str) -> List[str]:
    if not text:
        return []
    return [t for t in text.split(" ") if t]


def keyword_set(text: str) -> Set[str]:
    return set(tokenize(text))


def read_text_file(path: str) -> str:
    # Deterministic read: prefer utf-8, fall back to cp1252 without errors.
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, "r", encoding="cp1252", errors="ignore") as f:
            return f.read()


def list_corpus_files(data_dir: str) -> List[str]:
    paths: List[str] = []
    for root, _dirs, files in os.walk(data_dir):
        for name in files:
            lower = name.lower()
            if lower.endswith((".txt", ".md")):
                paths.append(os.path.join(root, name))
    paths.sort()
    return paths


def split_into_sentences(text: str) -> List[str]:
    cleaned = normalize_whitespace(text.replace("\n", " "))
    if not cleaned:
        return []
    # Simple, deterministic sentence split.
    parts = re.split(r"(?<=[.!?])\s+", cleaned)
    return [p.strip() for p in parts if p.strip()]


@dataclass(frozen=True)
class RetrievedDoc:
    path: str
    text: str
    cosine_similarity: float


@dataclass(frozen=True)
class RankedDoc:
    path: str
    text: str
    cosine_similarity: float
    keyword_overlap_bonus: float
    score: float

