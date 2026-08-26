import allure
import pytest

from src.repositories.postgres_catalog_repository import PostgresCatalogRepository


@allure.epic("Integration Tests")
@allure.feature("PostgreSQL")
@allure.story("Database connectivity")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.integration
@pytest.mark.postgres


def test_should_connect_to_postgres(
    postgres_repository: PostgresCatalogRepository,
) -> None:
    with allure.step("Verificar conectividade pelo repository"):
        is_connected = postgres_repository.check_connection()

    with allure.step("Validar retorno da camada de acesso"):
        assert is_connected is True
