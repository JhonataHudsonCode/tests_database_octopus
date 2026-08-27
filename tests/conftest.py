from __future__ import annotations

from collections.abc import Generator
import os

import pytest

from src.config.settings import (
    OpenSearchDashboardsSettings,
    OpenSearchSettings,
    PostgresSettings,
)
from src.connections.opensearch import OpenSearchConnection
from src.connections.opensearch_factory import OpenSearchConnectionFactory
from src.connections.opensearch_dashboards import OpenSearchDashboardsConnection
from src.connections.postgres import PostgresConnection
from src.repositories.opensearch_dashboards_repository import (
    OpenSearchDashboardsRepository,
)
from src.repositories.opensearch_health_repository import OpenSearchHealthRepository
from src.repositories.cognito_client_repository import CognitoClientRepository
from src.repositories.opensearch_vulnerability_repository import (
    OpenSearchVulnerabilityRepository,
)
from src.repositories.opensearch_client_rsa_repository import (
    OpenSearchClientRsaRepository,
)
from src.repositories.postgres_catalog_repository import PostgresCatalogRepository


@pytest.fixture(scope="session")
def postgres_settings() -> PostgresSettings:
    return PostgresSettings.from_env()


@pytest.fixture(scope="session")
def postgres_connection(
    postgres_settings: PostgresSettings,
) -> Generator[PostgresConnection, None, None]:
    connection = PostgresConnection(postgres_settings)
    connection.connect()

    yield connection

    connection.close()


@pytest.fixture(scope="session")
def postgres_repository(
    postgres_connection: PostgresConnection,
) -> PostgresCatalogRepository:
    return PostgresCatalogRepository(postgres_connection)


@pytest.fixture(scope="session")
def opensearch_settings() -> OpenSearchSettings:
    return OpenSearchSettings.from_env()


@pytest.fixture(scope="session")
def opensearch_connection(
    opensearch_settings: OpenSearchSettings,
) -> Generator[OpenSearchConnection, None, None]:
    connection = OpenSearchConnection(opensearch_settings)
    connection.connect()

    yield connection

    connection.close()


@pytest.fixture(scope="session")
def opensearch_repository(
    opensearch_connection: OpenSearchConnection,
) -> OpenSearchHealthRepository:
    return OpenSearchHealthRepository(opensearch_connection)


@pytest.fixture(scope="session")
def cognito_postgres_settings() -> PostgresSettings:
    if not os.getenv("COGNITO_PG_HOST"):
        pytest.skip("COGNITO_PG_HOST não foi configurado.")

    return PostgresSettings.from_env("COGNITO_PG")


@pytest.fixture(scope="session")
def cognito_postgres_connection(
    cognito_postgres_settings: PostgresSettings,
) -> Generator[PostgresConnection, None, None]:
    connection = PostgresConnection(cognito_postgres_settings)
    connection.connect()

    yield connection

    connection.close()


@pytest.fixture(scope="session")
def cognito_client_repository(
    cognito_postgres_connection: PostgresConnection,
) -> CognitoClientRepository:
    return CognitoClientRepository(cognito_postgres_connection)


@pytest.fixture(scope="session")
def new_opensearch_settings() -> OpenSearchSettings:
    if not os.getenv("NEW_OPENSEARCH_HOST"):
        pytest.skip("NEW_OPENSEARCH_HOST não foi configurado.")

    return OpenSearchSettings.from_env("NEW_OPENSEARCH")


@pytest.fixture(scope="session")
def new_opensearch_connection(
    new_opensearch_settings: OpenSearchSettings,
) -> Generator[OpenSearchConnection, None, None]:
    connection = OpenSearchConnection(new_opensearch_settings)
    connection.connect()

    yield connection

    connection.close()


@pytest.fixture(scope="session")
def new_opensearch_vulnerability_repository(
    new_opensearch_connection: OpenSearchConnection,
) -> OpenSearchVulnerabilityRepository:
    return OpenSearchVulnerabilityRepository(new_opensearch_connection)


@pytest.fixture(scope="session")
def client_rsa_repository(
    new_opensearch_settings: OpenSearchSettings,
) -> OpenSearchClientRsaRepository:
    connection_factory = OpenSearchConnectionFactory(new_opensearch_settings)
    return OpenSearchClientRsaRepository(connection_factory)


@pytest.fixture(scope="session")
def opensearch_dashboards_settings() -> OpenSearchDashboardsSettings:
    if not os.getenv("OPENSEARCH_DASHBOARDS_HOST"):
        pytest.skip("OPENSEARCH_DASHBOARDS_HOST não foi configurado.")

    return OpenSearchDashboardsSettings.from_env()


@pytest.fixture(scope="session")
def opensearch_dashboards_connection(
    opensearch_dashboards_settings: OpenSearchDashboardsSettings,
) -> Generator[OpenSearchDashboardsConnection, None, None]:
    connection = OpenSearchDashboardsConnection(opensearch_dashboards_settings)
    connection.connect()

    yield connection

    connection.close()


@pytest.fixture(scope="session")
def opensearch_dashboards_repository(
    opensearch_dashboards_connection: OpenSearchDashboardsConnection,
) -> OpenSearchDashboardsRepository:
    return OpenSearchDashboardsRepository(opensearch_dashboards_connection)
