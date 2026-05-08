from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils import RetrievedDoc, list_corpus_files, preprocess_text, read_text_file


@dataclass(frozen=True)
class RetrievalResult:
    docs: List[RetrievedDoc]
    vectorizer_fitted: bool


class TfidfRetriever:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self._paths: List[str] = []
        self._texts: List[str] = []
        self._vectorizer: Optional[TfidfVectorizer] = None
        self._matrix = None

    def load_and_fit(self) -> None:
        self._paths = list_corpus_files(self.data_dir)
        self._texts = [read_text_file(p) for p in self._paths]
        if not self._paths:
            self._vectorizer = None
            self._matrix = None
            return

        # Deterministic TF-IDF. No randomness used.
        self._vectorizer = TfidfVectorizer(lowercase=True)
        self._matrix = self._vectorizer.fit_transform(self._texts)

    def retrieve(self, query: str, top_k: int = 3) -> RetrievalResult:
        if not self._paths or self._vectorizer is None or self._matrix is None:
            return RetrievalResult(docs=[], vectorizer_fitted=False)

        qv = self._vectorizer.transform([query])
        sims = cosine_similarity(qv, self._matrix)[0]

        # Deterministic tie-break: by similarity desc, then path asc.
        ranked = sorted(
            enumerate(sims.tolist()),
            key=lambda x: (-float(x[1]), self._paths[x[0]]),
        )[:top_k]

        docs = [
            RetrievedDoc(
                path=self._paths[i],
                text=self._texts[i],
                cosine_similarity=float(score),
            )
            for i, score in ranked
            if float(score) > 0.0
        ]
        return RetrievalResult(docs=docs, vectorizer_fitted=True)

