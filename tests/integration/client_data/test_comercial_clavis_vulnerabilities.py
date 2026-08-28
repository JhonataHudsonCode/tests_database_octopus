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

@pytest.mark.integration
@pytest.mark.client_data
@pytest.mark.postgres
@pytest.mark.opensearch
def test_should_validate_comercial_vulnerability_index_for_today(
    cognito_client_repository: CognitoClientRepository,
    opensearch_vulnerability_repository: OpenSearchVulnerabilityRepository,
    client_rsa_repository: OpenSearchClientRsaRepository,
) -> None:
    client = cognito_client_repository.get_by_client_id_has_rsa(INDEX_CLIENT_NAME)

    assert client is not None, f"Cliente não encontrado: {INDEX_CLIENT_NAME}"

    if not client.has_rsa:
        pytest.fail(f"Cliente {INDEX_CLIENT_NAME} não possui RSA habilitado.")

    today = date.today()
    expected_index_name = (
        f"{INDEX_CLIENT_NAME}_vulnerability-was-{today.strftime('%y.%m.%d')}"
    )
    index = opensearch_vulnerability_repository.get_index_for_date(
        client_name=INDEX_CLIENT_NAME,
        reference_date=today,
    )

    assert index is not None, f"Índice não encontrado: {expected_index_name}"
    assert index.name == expected_index_name
    assert index.document_count > 0, (
        f"O índice {expected_index_name} não contém documentos."
    )

    expected_rsa_index_name = f"rsa-{today.strftime('%y.%m.%d')}"
    rsa_index_exists = client_rsa_repository.index_exists_for_date(
        client_host=client.octopus_endpoint,
        reference_date=today,
    )

    assert rsa_index_exists, (
        f"Índice não encontrado no OpenSearch do cliente "
        f"({client.octopus_endpoint}): {expected_rsa_index_name}"
    )
