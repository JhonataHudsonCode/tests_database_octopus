from __future__ import annotations

from collections.abc import Generator

import pytest

from src.config.settings import (
    OpenSearchSettings,
    PostgresSettings,
)
from src.connections.opensearch import OpenSearchConnection
from src.connections.opensearch_factory import OpenSearchConnectionFactory
from src.connections.opensearch_dashboards import OpenSearchDashboardsConnection
from src.connections.postgres import PostgresConnection
from src.connections.postgres_factory import PostgresConnectionFactory
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
from src.repositories.opensearch_rules_repository import OpenSearchRulesRepository
from src.repositories.postgres_catalog_repository import PostgresCatalogRepository


COGNITO_DATABASE = "cognito"


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
def postgres_connection_factory(
    postgres_settings: PostgresSettings,
) -> PostgresConnectionFactory:
    return PostgresConnectionFactory(postgres_settings)


@pytest.fixture(scope="session")
def cognito_postgres_connection(
    postgres_connection_factory: PostgresConnectionFactory,
) -> Generator[PostgresConnection, None, None]:
    connection = postgres_connection_factory.create_for_database(COGNITO_DATABASE)
    connection.connect()

    yield connection

    connection.close()


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
def cognito_client_repository(
    cognito_postgres_connection: PostgresConnection,
) -> CognitoClientRepository:
    return CognitoClientRepository(cognito_postgres_connection)


@pytest.fixture(scope="session")
def opensearch_vulnerability_repository(
    opensearch_connection: OpenSearchConnection,
) -> OpenSearchVulnerabilityRepository:
    return OpenSearchVulnerabilityRepository(opensearch_connection)


@pytest.fixture(scope="session")
def client_rsa_repository(
    opensearch_settings: OpenSearchSettings,
) -> OpenSearchClientRsaRepository:
    connection_factory = OpenSearchConnectionFactory(opensearch_settings)
    return OpenSearchClientRsaRepository(connection_factory)


@pytest.fixture(scope="session")
def opensearch_rules_repository(
    opensearch_settings: OpenSearchSettings,
) -> OpenSearchRulesRepository:
    connection_factory = OpenSearchConnectionFactory(opensearch_settings)
    return OpenSearchRulesRepository(connection_factory)


@pytest.fixture(scope="session")
def opensearch_dashboards_connection(
    opensearch_settings: OpenSearchSettings,
) -> Generator[OpenSearchDashboardsConnection, None, None]:
    connection = OpenSearchDashboardsConnection(opensearch_settings)
    connection.connect()

    yield connection

    connection.close()


@pytest.fixture(scope="session")
def opensearch_dashboards_repository(
    opensearch_dashboards_connection: OpenSearchDashboardsConnection,
) -> OpenSearchDashboardsRepository:
    return OpenSearchDashboardsRepository(opensearch_dashboards_connection)
