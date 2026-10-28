"""VACRA Score API client."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional
import urllib.request
import urllib.parse
import json


VACRA_API_BASE = "https://api.vacra.ai"


@dataclass
class VACRAScore:
    agent_did: str
    vacra_score: int
    compliance_state: str
    calibration_rate: Optional[float] = None
    ece: Optional[float] = None
    fpr: Optional[float] = None
    human_review_rate: Optional[float] = None
    receipt: dict = field(default_factory=dict)
    attester_did: Optional[str] = None
    attestation_date: Optional[str] = None
    raw: dict = field(default_factory=dict)


class VACRAClient:
    """Client for the VACRA Score API."""

    def __init__(
        self,
        base_url: str = VACRA_API_BASE,
        api_key: Optional[str] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or os.environ.get("VACRA_API_KEY")

    def score(
        self,
        agent_did: str,
        fields: Optional[list[str]] = None,
    ) -> VACRAScore:
        """
        Retrieve the VACRA Score for an agent DID.

        Args:
            agent_did: The agent's W3C DID (e.g. "did:web:agent.example.com")
            fields: Optional list of CRS fields to include in the response.

        Returns:
            VACRAScore dataclass with calibration attestation data.
        """
        encoded_did = urllib.parse.quote(agent_did, safe="")
        url = f"{self.base_url}/v1/agents/{encoded_did}/score"
        if fields:
            url += "?" + urllib.parse.urlencode({"fields": ",".join(fields)})

        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())

        return VACRAScore(
            agent_did=agent_did,
            vacra_score=data.get("vacra_score", 0),
            compliance_state=data.get("compliance_state", "UNKNOWN"),
            calibration_rate=data.get("calibration_rate"),
            ece=data.get("ece"),
            fpr=data.get("fpr"),
            human_review_rate=data.get("human_review_rate"),
            receipt=data.get("receipt", {}),
            attester_did=data.get("attester_did"),
            attestation_date=data.get("attestation_date"),
            raw=data,
        )


# Module-level default client (uses VACRA_API_KEY env var)
_default = VACRAClient()


def score(agent_did: str, **kwargs) -> VACRAScore:
    """Convenience wrapper — score an agent DID using the default client."""
    return _default.score(agent_did, **kwargs)
