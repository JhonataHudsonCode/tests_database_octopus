import pytest

from src.models.table_metadata import TableMetadata
from src.repositories.postgres_catalog_repository import PostgresCatalogRepository


@pytest.mark.integration
@pytest.mark.postgres
def test_should_return_expected_table_from_pg_tables(
    postgres_repository: PostgresCatalogRepository,
) -> None:
    table = postgres_repository.get_pg_table(
        schema_name=TARGET_SCHEMA,
        table_name=TARGET_TABLE,
    )

    assert table is not None
    assert isinstance(table, TableMetadata)
    assert table.schema_name == TARGET_SCHEMA
    assert table.table_name == TARGET_TABLE
    assert table.owner
TARGET_SCHEMA = "pg_catalog"
TARGET_TABLE = "pg_type"
