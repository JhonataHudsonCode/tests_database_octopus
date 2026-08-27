import pytest

from src.repositories.opensearch_health_repository import OpenSearchHealthRepository


@pytest.mark.integration
@pytest.mark.opensearch
def test_should_list_opensearch_indices(
    opensearch_repository: OpenSearchHealthRepository,
) -> None:
    indices = opensearch_repository.list_indices()

    assert isinstance(indices, list)
    assert all(isinstance(index_name, str) for index_name in indices)
