import allure
import pytest

from src.config.settings import PostgresSettings
from src.models.table_metadata import TableMetadata
from src.repositories.postgres_catalog_repository import PostgresCatalogRepository


@allure.epic("Integration Tests")
@allure.feature("PostgreSQL")
@allure.story("pg_catalog.pg_tables")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.integration
@pytest.mark.postgres

def test_should_return_expected_table_from_pg_tables(
    postgres_repository: PostgresCatalogRepository,
    postgres_settings: PostgresSettings,
) -> None:
    with allure.step(
        f"Consultar metadata de "
        f"{postgres_settings.target_schema}.{postgres_settings.target_table}"
    ):
        table = postgres_repository.get_pg_table(
            schema_name=postgres_settings.target_schema,
            table_name=postgres_settings.target_table,
        )

    with allure.step("Validar contrato retornado pelo repository"):
        assert table is not None
        assert isinstance(table, TableMetadata)
        assert table.schema_name == postgres_settings.target_schema
        assert table.table_name == postgres_settings.target_table
        assert table.owner
