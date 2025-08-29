"""Register Avro schemas with Confluent Schema Registry."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Tuple

import requests


def register_schema(
    subject: str,
    schema_path: str,
    registry_url: str,
    auth: Optional[Tuple[str, str]] = None,
) -> dict:
    """Register a schema file under the given subject.

    Parameters
    ----------
    subject:
        Schema Registry subject name.
    schema_path:
        Path to the Avro schema file (.avsc).
    registry_url:
        Base URL for the Schema Registry service.
    auth:
        Optional tuple with (username, password) for basic auth.
    """
    schema_str = Path(schema_path).read_text()
    payload = {"schema": schema_str}
    response = requests.post(
        f"{registry_url.rstrip('/')}/subjects/{subject}/versions",
        headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
        data=json.dumps(payload),
        auth=auth,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def main() -> None:
    """Example usage registering curated and features schemas."""
    registry_url = "https://schema-registry.example.com"
    register_schema("curated-value", "schemas/curated.avsc", registry_url)
    register_schema("features-value", "schemas/features.avsc", registry_url)


if __name__ == "__main__":
    main()
