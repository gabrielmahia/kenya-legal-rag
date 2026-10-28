# AGENTS.md — gabrielmahia/kenya-legal-rag

<!-- coverage-adaptive-reasoning:v2 -->

## What this is
⚖️ RAG system over Kenya legal documents — query the Constitution, Employment Act, Land Act, and Companies Act in Swahili

- Primary language: Python. Last push: 2026-07-04. Homepage: https://gabrielmahia.github.io.
- Detected from the files: Python packaging, tests under a tests directory or test_*.py files.
- CI workflows: ci.yml.
- Generated on 2026-10-28 from the repository's own files and GitHub metadata, not reviewed line by line. Anything marked UNKNOWN could not be determined: confirm it before relying on it, and correct this file when you learn better.

## Read first
- README.md
- agent-context.json
- Portfolio reasoning standard: https://github.com/gabrielmahia/nairobi-stack/blob/main/docs/COVERAGE_ADAPTIVE_REASONING.md

## Critical rules
- Read README.md first and treat its claims as unverified until a test or the source confirms them.
- Make the smallest change that solves the task, keep the repository runnable, and run the test command below if one exists; say plainly if you could not run it.
- Do not claim that anything works, passes, is live or deployed unless you ran it or read the proof; write UNKNOWN instead.
- If any data shown or shipped is simulated, sample or demo data, label it as such in the interface and in the README; never present it as real.
- Never commit secrets, tokens, credentials or personal data.
- Report vulnerabilities as SECURITY.md says: privately, never in a public issue.
- Licence: MIT. Do not change it.
- The subject of this repository appears to be legal (judged from the words 'legal' in its description and topics). Anything it outputs is information, not legal advice: keep that stated in the interface and README, and never use real personal data in tests, examples or screenshots.

## Coverage-Adaptive Reasoning v2

For consequential research, recommendations, investigations, analogy searches, forecasting, opportunity discovery, and canon building:

- A correct ranking inside an incomplete universe is still a failed answer.
- Separate candidate generation from candidate ranking.
- Materiality-gate the search: use the minimum useful set of orthogonal retrieval routes that could change the answer.
- Before closure ask what correct answer the current search method would be structurally incapable of finding.
- Treat aliases, language/geography, era, source class, format, genealogy, taxonomy, legal identity vs operational control/economic benefit, intermediaries, schema categories, null/failure cases, and negative space as potential blind spots when material.
- Maintain leading + competing + null explanations.
- Distinguish answer confidence from coverage confidence.
- “Nothing found” is not evidence of absence when coverage is low.
- Stop when additional independent search routes no longer materially change the candidate universe, hypotheses, decision, or next test.
- When an important miss occurs, repair the retrieval architecture via MISS → SENSOR REDESIGN; do not merely append the missed example.

## Multi-agent protocol
- Git is the memory bus.
- Read Issues and open/draft PRs before starting.
- Work from an Issue.
- Branch: `agent/<agent>/<issue>-<slug>`
- Open a draft PR immediately to claim scope.
- If another PR overlaps, review/subdivide rather than duplicate.
- Leave tests + handoff in Git.

## Commands
```bash
# install
pip install -r requirements.txt
# test
python -m pytest
# lint
see .github/workflows/ci.yml
```

## Never autonomously
- change licensing
- expose credentials
- perform irreversible external actions
