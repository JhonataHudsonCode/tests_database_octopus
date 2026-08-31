from __future__ import annotations

from datetime import datetime

from src.connections.opensearch_factory import OpenSearchConnectionFactory
from src.models.opensearch_index_metadata import OpenSearchIndexMetadata


class OpenSearchRulesRepository:
    """Consulta o mapping do índice rules no OpenSearch de um cliente."""

    def __init__(self, connection_factory: OpenSearchConnectionFactory) -> None:
        self._connection_factory = connection_factory

    def get_index_metadata(
        self,
        client_host: str,
        index_name: str = "rules",
    ) -> OpenSearchIndexMetadata:
        connection = self._connection_factory.create_for_host(client_host)

        try:
            mapping_response = connection.client.indices.get_mapping(index=index_name)
            settings_response = connection.client.indices.get_settings(index=index_name)
        finally:
            connection.close()

        mapping = mapping_response[index_name]["mappings"]
        creation_date = settings_response[index_name]["settings"]["index"][
            "creation_date"
        ]
        return OpenSearchIndexMetadata(
            name=index_name,
            created_at=datetime.fromtimestamp(int(creation_date) / 1000),
            mapping=mapping,
        )
