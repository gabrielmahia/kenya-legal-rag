# ⚖️ Kenya Legal RAG

Retrieval-Augmented Generation (RAG) system over Kenya's key legal documents. Query the Constitution of Kenya, Employment Act, Land Act, Companies Act, and more — in English or Swahili.

[![PyPI version](https://badge.fury.io/py/kenya-legal-rag.svg)](https://badge.fury.io/py/kenya-legal-rag)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Compatible](https://img.shields.io/badge/MCP-compatible-blue)](https://modelcontextprotocol.io)

## Research Basis

Built on the cross-lingual RAG framework methodology (arXiv:2601.02065) and validated against multilingual legal RAG approaches (IEEE Access, RAG in Legal Technology Survey, 2025). The Swahili benchmarking study (arXiv:2509.04516) confirms native-language retrieval produces substantially fewer errors.

## Legal Documents Covered

| Document | Coverage |
|----------|----------|
| Constitution of Kenya 2010 | Full text, all articles |
| Employment Act (Cap. 226) | Employee rights, contracts, termination |
| Land Act 2012 | Land tenure, registration, disputes |
| Companies Act 2015 | Business registration, compliance |
| Consumer Protection Act | Consumer rights, remedies |
| Data Protection Act 2019 | Privacy rights, obligations |

## Usage

```python
from kenya_legal_rag import KenyaLegalRAG

rag = KenyaLegalRAG()

# Query in English
result = rag.query("What are an employee's rights when dismissed without notice?")

# Query in Swahili
result = rag.query("Je, mfanyakazi ana haki gani anapofukuzwa kazi bila notisi?")

print(result.answer)
print(result.sources)
```

## MCP Server

```bash
uvx kenya-legal-rag
# or
pip install kenya-legal-rag
kenya-legal-rag
```

## Install

```bash
pip install kenya-legal-rag
```

## Part of the East Africa Civic Tech Portfolio

See also: [mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp) | [civic-agent-kit](https://github.com/gabrielmahia/civic-agent-kit)

## Disclaimer

Legal information only. Not legal advice. Consult a qualified advocate for legal matters.

## IP & Collaboration

MIT licensed. Feedback via GitHub Issues only — pull requests are not accepted. Full policy: [docs/architecture/IP_POLICY.md](docs/architecture/IP_POLICY.md). Security reports: see [SECURITY.md](SECURITY.md).
