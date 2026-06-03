"""
kenya_legal_rag — RAG over Kenya legal documents
Cross-lingual (English + Swahili) query support
"""
from __future__ import annotations
import os
import json
import urllib.request
from dataclasses import dataclass
from typing import Optional


@dataclass
class LegalQueryResult:
    answer: str
    sources: list[str]
    language: str
    confidence: str


LEGAL_CORPUS = {
    "constitution": {
        "title": "Constitution of Kenya 2010",
        "url": "https://www.kenyalaw.org/kl/fileadmin/pdfdownloads/Acts/ConstitutionofKenya2010.pdf",
        "key_articles": {
            "19": "Rights and fundamental freedoms — every person has inherent dignity and right to have rights respected",
            "25": "Fundamental rights that cannot be limited even in emergency",
            "27": "Equality and freedom from discrimination",
            "35": "Access to information — every citizen has right to access information held by State",
            "40": "Protection of right to property — every person has right to acquire and own property",
            "41": "Labour relations — every person has right to fair labour practices",
            "43": "Economic and social rights — housing, health, food, water, social security, education",
            "47": "Fair administrative action",
            "48": "Access to justice — every person has right to have dispute resolved by application of law",
        }
    },
    "employment_act": {
        "title": "Employment Act Chapter 226",
        "key_provisions": {
            "notice": "Section 35: Minimum notice periods — 1 day (under 1 month) to 28 days (5+ years)",
            "termination": "Section 41: Employer must explain reason for termination, employee may have representative",
            "unfair_dismissal": "Section 45: Dismissal unfair if not justifiable reason or procedure not followed",
            "leave": "Section 28: Annual leave — 21 days per year after 12 months continuous service",
            "maternity": "Section 29: Maternity leave — 3 months on full pay",
            "overtime": "Section 27: Overtime — 150% of normal rate (200% on public holidays)",
            "minimum_wage": "Minimum wages set by Wages Orders, vary by region and sector",
        }
    },
    "land_act": {
        "title": "Land Act 2012",
        "key_provisions": {
            "ownership": "Section 24: Land in Kenya is classified as public, community, or private",
            "registration": "Land Registration Act: all interests in land must be registered",
            "dispute": "Section 150: Land disputes — parties should attempt alternative dispute resolution first",
            "compulsory": "Section 107: Compulsory acquisition — government must pay fair compensation promptly",
        }
    },
    "data_protection": {
        "title": "Data Protection Act 2019",
        "key_provisions": {
            "rights": "Section 26: Right to access personal data, correct inaccuracies, object to processing",
            "consent": "Section 30: Personal data cannot be processed without consent except in limited circumstances",
            "breach": "Section 43: Data controller must notify Commissioner of breach within 72 hours",
        }
    }
}


class KenyaLegalRAG:
    """
    Retrieval-Augmented Generation over Kenya legal documents.
    Uses Gemini REST API for generation, internal corpus for retrieval.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
        self.corpus = LEGAL_CORPUS

    def _detect_language(self, text: str) -> str:
        swahili_words = {"je", "na", "ya", "wa", "kwa", "au", "ni", "haki", "sheria",
                         "mfanyakazi", "ardhi", "kampuni", "habari", "hati", "serikali"}
        words = set(text.lower().split())
        return "sw" if len(words & swahili_words) >= 2 else "en"

    def _retrieve(self, query: str) -> list[dict]:
        """Simple keyword-based retrieval over legal corpus."""
        query_lower = query.lower()
        relevant = []
        keyword_map = {
            "employment|work|job|salary|wage|dismiss|termination|mfanyakazi|kazi|mshahara|kufukuzwa": "employment_act",
            "land|property|title|deed|ardhi|mashamba|miliki": "land_act",
            "constitution|rights|fundamental|haki|katiba": "constitution",
            "data|privacy|personal|taarifa|faragha": "data_protection",
            "company|business|registration|kampuni|biashara": "constitution",
        }
        for pattern, doc_key in keyword_map.items():
            if any(kw in query_lower for kw in pattern.split("|")):
                if doc_key in self.corpus:
                    relevant.append(self.corpus[doc_key])
        return relevant or list(self.corpus.values())[:2]

    def query(self, question: str) -> LegalQueryResult:
        """Query the Kenya legal corpus."""
        lang = self._detect_language(question)
        docs = self._retrieve(question)

        context = "\n\n".join([
            f"=== {doc['title']} ===\n" + "\n".join(
                f"{k}: {v}" for k, v in (doc.get("key_provisions") or doc.get("key_articles", {})).items()
            )
            for doc in docs
        ])

        if lang == "sw":
            system = (
                "Wewe ni mshauri wa sheria ya Kenya. Jibu kwa Kiswahili wazi. "
                "Tumia habari zilizotolewa tu. Kama hujui jibu, sema hivyo. "
                "Hii si ushauri wa kisheria rasmi — mwambie mtumiaji awasiliane na wakili kwa mambo muhimu."
            )
        else:
            system = (
                "You are a Kenya legal information assistant. Answer clearly in English. "
                "Use only the provided legal information. If unsure, say so. "
                "This is information only, not legal advice — recommend consulting an advocate for important matters."
            )

        prompt = f"Legal context:\n{context}\n\nQuestion: {question}"

        if not self.api_key:
            return LegalQueryResult(
                answer="API key not configured. Set GOOGLE_API_KEY environment variable.",
                sources=[d["title"] for d in docs],
                language=lang,
                confidence="N/A"
            )

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
        body = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "systemInstruction": {"parts": [{"text": system}]},
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 600}
        }
        try:
            req = urllib.request.Request(
                url, data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=30) as r:
                d = json.loads(r.read())
                answer = d["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            answer = f"Error: {e}"

        return LegalQueryResult(
            answer=answer,
            sources=[d["title"] for d in docs],
            language=lang,
            confidence="medium"
        )


if __name__ == "__main__":
    rag = KenyaLegalRAG()
    result = rag.query("What notice period is an employee entitled to after 3 years of service?")
    print(f"Answer: {result.answer}")
    print(f"Sources: {result.sources}")
