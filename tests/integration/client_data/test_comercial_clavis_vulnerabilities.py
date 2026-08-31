from datetime import date

import pytest

from src.repositories.cognito_client_repository import CognitoClientRepository
from src.repositories.opensearch_vulnerability_repository import (
    OpenSearchVulnerabilityRepository,
)
from src.repositories.opensearch_client_rsa_repository import (
    OpenSearchClientRsaRepository,
)

INDEX_CLIENT_NAME = "comercial"
CLIENT_SCHEMA = "public"

@pytest.mark.integration
@pytest.mark.client_data
@pytest.mark.postgres
@pytest.mark.opensearch
def test_should_validate_comercial_vulnerability_index_for_today(
    cognito_client_repository: CognitoClientRepository,
    opensearch_vulnerability_repository: OpenSearchVulnerabilityRepository,
    client_rsa_repository: OpenSearchClientRsaRepository,
) -> None:
    client = cognito_client_repository.get_by_client_id_has_rsa(
        schema_name=CLIENT_SCHEMA,
        client_id=INDEX_CLIENT_NAME,
    )

    assert client is not None, f"Cliente não encontrado: {INDEX_CLIENT_NAME}"

    if not client.has_rsa:
        pytest.fail(f"Cliente {INDEX_CLIENT_NAME} não possui RSA habilitado.")

    today = date.today()
    expected_index_name = (
        f"{INDEX_CLIENT_NAME}_vulnerability-was-{today.strftime('%y.%m.%d')}"
    )
    indices = opensearch_vulnerability_repository.get_indices_for_date(
        client_names=[INDEX_CLIENT_NAME],
        reference_date=today,
    )
    indices_by_name = {index.name: index for index in indices}
    index = indices_by_name.get(expected_index_name)

    assert index is not None, f"Índice não encontrado: {expected_index_name}"
    assert index.name == expected_index_name
    assert index.document_count > 0, (
        f"O índice {expected_index_name} não contém documentos."
    )
    vulnerability_documents = opensearch_vulnerability_repository.get_documents(
        expected_index_name,
    )
    assert vulnerability_documents, (
        f"O índice {expected_index_name} não retornou documentos."
    )

    expected_rsa_index_name = f"rsa-{today.strftime('%y.%m.%d')}"
    rsa_indices = client_rsa_repository.get_indices_for_date(
        client_host=(
            client.octopus_endpoint
            .replace("https://", "")
            .replace("http://", "")
        ),
        reference_date=today,
    )
    rsa_index_names = {index.name for index in rsa_indices}

    assert expected_rsa_index_name in rsa_index_names, (
        f"Índice não encontrado no OpenSearch do cliente "
        f"({client.octopus_endpoint}): {expected_rsa_index_name}"
    )
    rsa_documents = client_rsa_repository.get_documents(
        client_host=(
            client.octopus_endpoint
            .replace("https://", "")
            .replace("http://", "")
        ),
        index_name=expected_rsa_index_name,
    )
    assert rsa_documents, (
        f"O índice {expected_rsa_index_name} não retornou documentos."
    )
