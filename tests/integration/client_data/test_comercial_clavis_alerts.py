from datetime import date

import pytest

from src.repositories.cognito_client_repository import CognitoClientRepository
from src.repositories.opensearch_client_rsa_repository import (
    OpenSearchClientRsaRepository,
)
from src.repositories.opensearch_vulnerability_repository import (
    OpenSearchVulnerabilityRepository,
)


INDEX_CLIENT_NAME = "comercial"
CLIENT_SCHEMA = "public"


@pytest.mark.integration
@pytest.mark.client_data
@pytest.mark.postgres
@pytest.mark.opensearch
def test_should_validate_comercial_alerts_indices_for_today(
    cognito_client_repository: CognitoClientRepository,
    opensearch_vulnerability_repository: OpenSearchVulnerabilityRepository,
    client_rsa_repository: OpenSearchClientRsaRepository,
) -> None:
    client = cognito_client_repository.get_by_client_id(
        schema_name=CLIENT_SCHEMA,
        client_id=INDEX_CLIENT_NAME,
    )

    assert client is not None, f"Cliente não encontrado: {INDEX_CLIENT_NAME}"
    assert client.has_alerts, f"Cliente {INDEX_CLIENT_NAME} não possui alertas habilitados."

    today = date.today()
    expected_vulnerability_index = (
        f"{INDEX_CLIENT_NAME}_vulnerability-was-{today:%y.%m.%d}"
    )
    vulnerability_indices = opensearch_vulnerability_repository.get_indices_for_date(
        client_names=[INDEX_CLIENT_NAME],
        reference_date=today,
    )
    indices_by_name = {index.name: index for index in vulnerability_indices}
    vulnerability_index = indices_by_name.get(expected_vulnerability_index)

    assert vulnerability_index is not None, (
        f"Índice não encontrado: {expected_vulnerability_index}"
    )
    assert vulnerability_index.document_count > 0, (
        f"O índice {expected_vulnerability_index} não contém documentos."
    )
    vulnerability_documents = opensearch_vulnerability_repository.get_documents(
        expected_vulnerability_index,
    )
    assert vulnerability_documents, (
        f"O índice {expected_vulnerability_index} não retornou documentos."
    )

    expected_rsa_index = f"rsa-{today:%y.%m.%d}"
    client_host = (
        client.octopus_endpoint.replace("https://", "").replace("http://", "")
    )
    rsa_indices = client_rsa_repository.get_indices_for_date(
        client_host=client_host,
        reference_date=today,
    )
    rsa_index_names = {index.name for index in rsa_indices}

    assert expected_rsa_index in rsa_index_names, (
        f"Índice não encontrado no OpenSearch do cliente "
        f"({client.octopus_endpoint}): {expected_rsa_index}"
    )
    rsa_documents = client_rsa_repository.get_documents(
        client_host=client_host,
        index_name=expected_rsa_index,
    )
    assert rsa_documents, f"O índice {expected_rsa_index} não retornou documentos."
