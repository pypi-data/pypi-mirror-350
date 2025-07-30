from http import HTTPStatus
from typing import Iterator, Optional

import requests

from ....utils import (
    APIClient,
    BearerAuth,
    RequestSafeMode,
    SerializedAsset,
    retry,
)
from ..assets import CoalesceAsset, CoalesceQualityAsset
from .credentials import CoalesceCredentials
from .endpoint import (
    CoalesceEndpointFactory,
)
from .type import NodeIDToNamesMapping
from .utils import column_names_per_node, is_test, test_names_per_node

_LIMIT_MAX = 1_000
_MAX_ERRORS = 50
_RETRY_BASE_MS = 10 * 60 * 1000  # 10 minutes
_RETRY_COUNT = 2
_RETRY_EXCEPTIONS = [requests.exceptions.ConnectTimeout]


def _run_result_payload(result: dict, query_result: dict) -> dict:
    return {
        "node_id": result["nodeID"],
        "node_name": result["name"],
        "test_name": query_result["name"],
        "start_time": query_result["startTime"],
        "end_time": query_result["endTime"],
        "status": query_result["status"],
        "success": query_result["success"],
        "isRunning": query_result["isRunning"],
    }


COALESCE_SAFE_MODE = RequestSafeMode(
    status_codes=(HTTPStatus.INTERNAL_SERVER_ERROR,),
    max_errors=_MAX_ERRORS,
)
COALESCE_TIMEOUT_SECONDS = 90


class CoalesceBearerAuth(BearerAuth):
    """Bearer Authentication for Coalesce"""

    def fetch_token(self) -> Optional[str]:
        pass

    def __init__(self, token: str):
        self._token = token


class CoalesceClient(APIClient):
    """REST API client to extract data from Coalesce"""

    def __init__(
        self,
        credentials: CoalesceCredentials,
    ):
        auth = CoalesceBearerAuth(token=credentials.token)
        super().__init__(
            host=credentials.host,
            auth=auth,
            safe_mode=COALESCE_SAFE_MODE,
            timeout=COALESCE_TIMEOUT_SECONDS,
        )

    def _fetch_environments(self) -> Iterator[dict]:
        endpoint = CoalesceEndpointFactory.environments()
        result = self._get(endpoint=endpoint)
        return result["data"]

    @retry(
        exceptions=_RETRY_EXCEPTIONS,
        max_retries=_RETRY_COUNT,
        base_ms=_RETRY_BASE_MS,
    )
    def _node_details(self, environment_id: int, node_id: str) -> dict:
        endpoint = CoalesceEndpointFactory.nodes(
            environment_id=environment_id, node_id=node_id
        )
        return self._get(endpoint=endpoint)

    def _fetch_env_nodes(self, environment_id: int) -> SerializedAsset:
        endpoint = CoalesceEndpointFactory.nodes(environment_id=environment_id)
        result = self._get(endpoint=endpoint)
        nodes: list[dict] = []
        for node in result["data"]:
            details = self._node_details(environment_id, node["id"])
            nodes.append({**node, **details})
        return nodes

    def _fetch_all_nodes(self) -> SerializedAsset:
        nodes: list[dict] = []
        for environment in self._fetch_environments():
            environment_id = environment["id"]
            nodes.extend(self._fetch_env_nodes(environment_id))
        return nodes

    def _fetch_runs(self, starting_from: str) -> SerializedAsset:
        """
        fetch runs, per environment;
        we break per environment to lower the chance of exceeding the 1k limit
        """
        runs: list[dict] = []
        for environment in self._fetch_environments():
            environment_id = environment["id"]
            runs.extend(
                self._fetch_recent_runs_per_env(environment_id, starting_from)
            )
        return runs

    def _fetch_recent_runs_per_env(
        self, environment_id: int, starting_from: str
    ) -> SerializedAsset:
        endpoint = CoalesceEndpointFactory.runs()
        params = {
            "environmentID": environment_id,
            "limit": _LIMIT_MAX,
            "orderBy": "runEndTime",
            "orderByDirection": "asc",
            "startingFrom": starting_from,
        }
        result = self._get(endpoint=endpoint, params=params)
        return result["data"]

    def _fetch_run_results(self, run_id: str) -> SerializedAsset:
        endpoint = CoalesceEndpointFactory.run_results(run_id)
        result = self._get(endpoint=endpoint)
        return result["data"]

    def _run_results_by_run(
        self,
        run_id: str,
        test_names: NodeIDToNamesMapping,
        column_names: NodeIDToNamesMapping,
    ) -> SerializedAsset:
        run_results: list[dict] = []
        for result in self._fetch_run_results(run_id):
            node_id = result["nodeID"]
            for query_result in result["queryResults"]:
                _is_test = is_test(
                    query_result,
                    node_id,
                    test_names,
                    column_names,
                )
                if not _is_test:
                    continue
                run_result = _run_result_payload(result, query_result)
                run_results.append(run_result)
        return run_results

    def _run_results_by_env(
        self, environment_id: int, starting_from: str
    ) -> SerializedAsset:
        run_results: list[dict] = []
        nodes = self._fetch_env_nodes(environment_id)
        test_names = test_names_per_node(nodes)
        column_names = column_names_per_node(nodes)
        runs = self._fetch_recent_runs_per_env(environment_id, starting_from)

        for run in runs:
            run_id = run["id"]
            _results = self._run_results_by_run(
                run_id, test_names, column_names
            )
            run_results.extend(_results)
        return run_results

    def _fetch_all_run_results(self, starting_from: str) -> SerializedAsset:
        run_results: list[dict] = []

        for environment in self._fetch_environments():
            environment_id = environment["id"]
            _results = self._run_results_by_env(environment_id, starting_from)
            run_results.extend(_results)

        return run_results

    def fetch(
        self, asset: CoalesceAsset, starting_from=None
    ) -> SerializedAsset:
        """Extract the given Coalesce Asset"""
        if asset in (CoalesceAsset.NODES, CoalesceQualityAsset.NODES):
            return self._fetch_all_nodes()
        elif asset == CoalesceQualityAsset.RUN_RESULTS:
            return self._fetch_all_run_results(starting_from=starting_from)
        raise AssertionError(
            f"Asset {asset} is not supported by CoalesceClient"
        )
