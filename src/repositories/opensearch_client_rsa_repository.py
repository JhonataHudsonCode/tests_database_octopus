from __future__ import annotations

from datetime import date

from src.connections.opensearch_factory import OpenSearchConnectionFactory


class OpenSearchClientRsaRepository:
    """Valida índices RSA no OpenSearch específico de cada cliente."""

    def __init__(self, connection_factory: OpenSearchConnectionFactory) -> None:
        self._connection_factory = connection_factory

    def index_exists_for_date(
        self,
        client_host: str,
        reference_date: date,
    ) -> bool:
        index_name = f"rsa-{reference_date.strftime('%y.%m.%d')}"
        connection = self._connection_factory.create_for_host(client_host)

        try:
            return bool(connection.client.indices.exists(index=index_name))
        finally:
            connection.close()
