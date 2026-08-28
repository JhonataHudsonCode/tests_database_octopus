from datetime import date

import pytest

from src.repositories.cognito_client_repository import CognitoClientRepository
from src.repositories.opensearch_vulnerability_repository import (
    OpenSearchVulnerabilityRepository,
)


SPECIAL_CLIENT_ID = "comercial-clavis"


@pytest.mark.integration
@pytest.mark.client_data
@pytest.mark.postgres
@pytest.mark.opensearch
def test_should_validate_vulnerability_indices_for_all_rsa_enabled_clients(
    cognito_client_repository: CognitoClientRepository,
    opensearch_vulnerability_repository: OpenSearchVulnerabilityRepository,
) -> None:
    clients = cognito_client_repository.list_clients()

    assert clients, "Nenhum cliente foi retornado por public.clients."

    clients_to_validate = [
        client for client in clients if client.client_id != SPECIAL_CLIENT_ID
    ]
    assert clients_to_validate, "Nenhum cliente disponível para validação em lote."

    today = date.today()
    failures: list[str] = []

    for client in clients_to_validate:
        if not client.has_rsa:
            continue

        expected_index_name = (
            f"{client.client_id}_vulnerability-was-{today.strftime('%y.%m.%d')}"
        )
        index = opensearch_vulnerability_repository.get_index_for_date(
            client_name=client.client_id,
            reference_date=today,
        )

        if index is None:
            failures.append(f"Índice não encontrado: {expected_index_name}")
        elif index.document_count <= 0:
            failures.append(
                f"Índice sem documentos: {expected_index_name}"
            )

    assert not failures, "\n".join(failures)
