# Evidence grounding for inquiry claims

The AI Ecosystem Model is descriptive. A valid graph path is not evidence
that an obligation is enforceable, that a control is effective, or that a
real-world outcome occurred. The inquiry protocol's Type 1/2/3 classification
remains authoritative; the **optional** claim ledger below is a separate
statement-level provenance aid, not an additional ontology or a truth score.

For a small number of consequential conclusions, authors may add front
matter:

```yaml
claim_evidence:
  - id: C-01
    classification: derived
    model_refs: [E_AGENT_TO_GATEWAY_A2T]
    assumptions:
      - Relevant target operations are mediated by the gateway.
```

Place `<!-- claim: C-01 -->` immediately after the paragraph or list item
containing that conclusion. Use stable IDs within an inquiry.

Classification:
- `represented`: canonical references directly encode the stated relationship.
- `derived`: a reasoning step beyond the graph; requires `assumptions`.
- `externally-evidenced`: a legal/empirical assertion; requires `sources`
  containing source URLs. Their reliability, currency and relevance require review.
- `unverified`: the proposition remains unresolved; requires `limitations`.

`model_refs` may list N_/E_/L_/F_/V_ identifiers. References are checked for
existence only. A represented claim can still misuse a valid ID, and a
derived claim can rest on a false assumption. The linter does not inspect
the prose, authenticate sources, evaluate jurisdictions, check freshness,
or establish the completeness of the set of annotated claims. Human
review remains responsible for those judgments.

Validate locally:

```sh
python scripts/validate_inquiry_claims.py model/ai_ecosystem.yaml docs/inquiries/*.md
python -m unittest discover -s tests -p 'test_*.py'
```

The master pipeline invokes claim-ledger validation after the existing
canonical reference checks. Legacy inquiries without `claim_evidence`
are accepted unchanged. New entries are deliberately opt-in; expansion
should follow demonstrated reviewer value rather than mandatory backfill.

A useful adversarial review asks whether a syntactically valid set of
nodes and edges is being presented as proof of execution, independence,
legal authority, or an empirical effect. For instance,
`E_OBSERVE_TO_AUDITOR` shows an evidence flow, not whether evidence is
complete, independently generated, or sufficient for certification.
