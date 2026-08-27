import pytest

from src.repositories.opensearch_dashboards_repository import (
    OpenSearchDashboardsRepository,
)


@pytest.mark.integration
@pytest.mark.dashboards
def test_should_list_opensearch_dashboards(
    opensearch_dashboards_repository: OpenSearchDashboardsRepository,
) -> None:
    dashboards = opensearch_dashboards_repository.list_dashboards()

    assert isinstance(dashboards, list)
    assert all(isinstance(dashboard_name, str) for dashboard_name in dashboards)
