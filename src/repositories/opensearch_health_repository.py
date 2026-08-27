from __future__ import annotations

from src.connections.opensearch import OpenSearchConnection


class OpenSearchHealthRepository:
    """Expõe verificações de saúde do OpenSearch para os testes."""

    def __init__(self, connection: OpenSearchConnection) -> None:
        self._connection = connection

    def check_connection(self) -> bool:
        """Retorna se o cluster OpenSearch responde ao ping."""
        return bool(self._connection.client.ping())
