from __future__ import annotations

import logging
from datetime import date
from typing import Any

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
            connection.client.info()
            logger.info(
                "Conexão com o OpenSearch do cliente realizada em %s.",
                client_host,
            )
            indices = connection.client.cat.indices(
                index="rsa-*",
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
                document_count=self._parse_document_count(item.get("docs.count")),
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

    def get_documents(
        self,
        client_host: str,
        index_name: str,
        size: int = 10,
    ) -> list[dict[str, Any]]:
        """Retorna documentos de um índice RSA do OpenSearch do cliente."""
        connection = self._connection_factory.create_for_host(client_host)

        try:
            response = connection.client.search(
                index=index_name,
                body={
                    "size": size,
                    "query": {"match_all": {}},
                },
            )
        finally:
            connection.close()

        return response["hits"]["hits"]

    @staticmethod
    def _parse_document_count(value: object) -> int:
        if value in {None, "", "-"}:
            return 0

        return int(value)
