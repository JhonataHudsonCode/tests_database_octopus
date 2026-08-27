import pytest

from src.config.settings import PostgresSettings
from src.models.table_metadata import TableMetadata
from src.repositories.postgres_catalog_repository import PostgresCatalogRepository


@pytest.mark.integration
@pytest.mark.postgres
def test_should_return_expected_table_from_pg_tables(
    postgres_repository: PostgresCatalogRepository,
    postgres_settings: PostgresSettings,
) -> None:
    table = postgres_repository.get_pg_table(
        schema_name=postgres_settings.target_schema,
        table_name=postgres_settings.target_table,
    )

    assert table is not None
    assert isinstance(table, TableMetadata)
    assert table.schema_name == postgres_settings.target_schema
    assert table.table_name == postgres_settings.target_table
    assert table.owner
