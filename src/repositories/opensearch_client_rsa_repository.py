from __future__ import annotations

import logging
from datetime import date

from src.connections.opensearch_factory import OpenSearchConnectionFactory
from src.models.vulnerability_index import VulnerabilityIndex


logger = logging.getLogger(__name__)


class OpenSearchClientRsaRepository:
    """Valida índices RSA no OpenSearch específico de cada cliente."""

    def __init__(self, connection_factory: OpenSearchConnectionFactory) -> None:
        self._connection_factory = connection_factory

    def get_indices_for_date(
        self,
        client_host: str,
        reference_date: date,
    ) -> list[VulnerabilityIndex]:
        index_name = f"rsa-{reference_date.strftime('%y.%m.%d')}"
        connection = self._connection_factory.create_for_host(client_host)

        try:
            indices = connection.client.cat.indices(
                index=index_name,
                format="json",
                h="index,docs.count",
                expand_wildcards="all",
                ignore_unavailable=True,
            )
        finally:
            connection.close()

        found_indices = [
            VulnerabilityIndex(
                name=item["index"],
                document_count=int(item.get("docs.count", 0)),
            )
            for item in indices
            if item.get("index")
        ]
        logger.info(
            "Índice RSA esperado no host %s: %s. Índices encontrados: %s",
            client_host,
            index_name,
            [index.name for index in found_indices],
        )
        return found_indices
