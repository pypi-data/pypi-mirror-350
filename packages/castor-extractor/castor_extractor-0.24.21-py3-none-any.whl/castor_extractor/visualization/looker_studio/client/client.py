from typing import Iterator, Optional

from ....utils import empty_iterator
from ....warehouse.abstract import WarehouseAsset
from ....warehouse.bigquery import BigQueryClient, BigQueryQueryBuilder
from .. import LookerStudioAsset
from .admin_sdk_client import USER_EMAIL_FIELD, AdminSDKClient
from .credentials import LookerStudioCredentials
from .looker_studio_api_client import LookerStudioAPIClient


class LookerStudioQueryBuilder(BigQueryQueryBuilder):
    def job_history_queries(self) -> list:
        """
        This class and method are a convenient workaround to build the
        ExtractionQueries which retrieve BigQuery's job history, but filtered on
        Looker Studio only.

        Compared to the generic BigQuery query history, only the SQL "template"
        changes. By defining this class here, this will pick the SQL file
        `queries/query.sql` located in the same directory as this file.
        """
        return super().build(WarehouseAsset.QUERY)  # type: ignore


class LookerStudioClient:
    """
    Acts as a wrapper class to fetch Looker Studio assets, which requires
    coordinating calls between the Admin SDK API and the Looker Studio API.

    If the BigQuery credentials are provided, it can also fetch the source queries
    of BigQuery data sources.
    """

    def __init__(
        self,
        credentials: LookerStudioCredentials,
        bigquery_credentials: Optional[dict] = None,
    ):
        self.admin_sdk_client = AdminSDKClient(credentials)
        self.looker_studio_client = LookerStudioAPIClient(credentials)

        self.bigquery_client: Optional[BigQueryClient] = None
        if bigquery_credentials:
            self.bigquery_client = BigQueryClient(bigquery_credentials)

    def _get_assets(self) -> Iterator[dict]:
        """
        Extracts reports and data sources user by user.
        """
        users = self.admin_sdk_client.list_users()

        for user in users:
            email = user[USER_EMAIL_FIELD]
            yield from self.looker_studio_client.fetch_user_assets(email)

    def _get_source_queries(self) -> Iterator[dict]:
        """
        Extracts the BigQuery jobs triggered by Looker Studio. The last job
        per data source is returned.
        """
        if not self.bigquery_client:
            return empty_iterator()

        query_builder = LookerStudioQueryBuilder(
            regions=self.bigquery_client.get_regions(),
            datasets=self.bigquery_client.get_datasets(),
            extended_regions=self.bigquery_client.get_extended_regions(),
        )

        queries = query_builder.job_history_queries()

        for query in queries:
            yield from self.bigquery_client.execute(query)

    def fetch(self, asset: LookerStudioAsset) -> Iterator[dict]:
        if asset == LookerStudioAsset.ASSETS:
            yield from self._get_assets()

        elif asset == LookerStudioAsset.SOURCE_QUERIES:
            yield from self._get_source_queries()

        elif asset == LookerStudioAsset.VIEW_ACTIVITY:
            yield from self.admin_sdk_client.list_view_events()

        else:
            raise ValueError(f"The asset {asset}, is not supported")
