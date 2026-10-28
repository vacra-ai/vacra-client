# vacra-client

Python client for the [VACRA Score API](https://vacra.ai) — calibration attestation for AI agents.

## What is VACRA Score?

VACRA Score returns a calibration score and signed attestation receipt for any AI agent DID. It measures the alignment between stated confidence and empirical frequency using the [Calibration Reporting Standard (CRS)](https://github.com/ericchantc/crs-specification).

```python
from vacra import client

score = client.score("did:web:agent.example.com")
print(score.vacra_score)       # e.g. 847
print(score.compliance_state)  # "COMPLIANT" | "REMEDIATING" | "MANDATORY_HOLD"
print(score.receipt)           # signed CRS attestation receipt
```

## Install

```bash
pip install vacra-client
```

## Quick Start

```python
from vacra import client, VACRAClient

# Default (uses api.vacra.ai)
score = client.score("did:web:your-agent.example.com")

# Custom endpoint
api = VACRAClient(base_url="https://api.vacra.ai", api_key="your-key")
score = api.score("did:web:your-agent.example.com", fields=["calibration_rate", "ece"])
```

## Response

```python
@dataclass
class VACRAScore:
    agent_did: str
    vacra_score: int           # 0–1000
    compliance_state: str      # COMPLIANT | REMEDIATING | MANDATORY_HOLD
    calibration_rate: float    # F5 — overall calibration rate
    ece: float                 # F7 — Expected Calibration Error
    fpr: float                 # F6 — False Positive Rate
    human_review_rate: float   # F8
    receipt: dict              # signed CRS attestation receipt
    attester_did: str          # F11
    attestation_date: str      # F12 — ISO 8601
```

## API Reference

Full API docs: [vacra.ai/docs](https://vacra.ai/docs)

## License

Apache 2.0 — see [LICENSE](LICENSE)

Patents pending — see [PATENTS.md](PATENTS.md)
