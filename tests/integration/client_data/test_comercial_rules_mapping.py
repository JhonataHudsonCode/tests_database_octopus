from collections.abc import Mapping
from typing import Any

import pytest

from src.repositories.cognito_client_repository import CognitoClientRepository
from src.repositories.opensearch_rules_repository import OpenSearchRulesRepository


CLIENT_ID = "comercial"
CLIENT_SCHEMA = "public"
RULES_INDEX_NAME = "rules"

EXPECTED_RULES_MAPPING: dict[str, str | dict[str, Any]] = {
    "@timestamp": "date",
    "cardinality": "long",
    "file": "text",
    "frequency": "long",
    "interval": "long",
    "query": "text",
    "query_key": "text",
    "rule": {
        "channels": "text",
        "description": "text",
        "handling": "text",
        "id": "text",
        "index": "text",
        "name": "text",
        "properties": {
            "homolog": "boolean",
            "severity": "text",
            "source": "text",
            "type": "text",
        },
    },
    "term": "text",
}


@pytest.mark.integration
@pytest.mark.client_data
@pytest.mark.postgres
@pytest.mark.opensearch
def test_should_validate_comercial_rules_mapping(
    cognito_client_repository: CognitoClientRepository,
    opensearch_rules_repository: OpenSearchRulesRepository,
) -> None:
    client = cognito_client_repository.get_by_client_id(
        schema_name=CLIENT_SCHEMA,
        client_id=CLIENT_ID,
    )
    assert client is not None, f"Cliente não encontrado: {CLIENT_ID}"

    client_host = (
        client.octopus_endpoint.replace("https://", "").replace("http://", "")
    )
    metadata = opensearch_rules_repository.get_index_metadata(
        client_host=client_host,
        index_name=RULES_INDEX_NAME,
    )

    _assert_mapping_properties(
        actual_properties=metadata.mapping.get("properties", {}),
        expected_properties=EXPECTED_RULES_MAPPING,
    )


def _assert_mapping_properties(
    actual_properties: Mapping[str, Any],
    expected_properties: Mapping[str, str | dict[str, Any]],
    path: str = "",
) -> None:
    for field_name, expected_definition in expected_properties.items():
        field_path = f"{path}.{field_name}" if path else field_name
        actual_definition = actual_properties.get(field_name)

        assert actual_definition is not None, (
            f"Campo ausente no mapping do índice rules: {field_path}"
        )

        if isinstance(expected_definition, dict):
            nested_properties = actual_definition.get("properties", {})
            assert nested_properties, (
                f"Campo objeto sem propriedades no mapping: {field_path}"
            )
            _assert_mapping_properties(
                actual_properties=nested_properties,
                expected_properties=expected_definition,
                path=field_path,
            )
            continue

        assert actual_definition.get("type") == expected_definition, (
            f"Tipo incorreto para {field_path}. "
            f"Esperado: {expected_definition}; "
            f"encontrado: {actual_definition.get('type')}"
        )
