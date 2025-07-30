from ....utils import SerializedAsset
from .type import NodeIDToNamesMapping

_NULL_SUFFIX = ": Null"
_UNIQUE_SUFFIX = ": Unique"


def is_test(
    query_result: dict,
    node_id: str,
    test_names: NodeIDToNamesMapping,
    column_names: NodeIDToNamesMapping,
) -> bool:
    """
    checks whether a query result is a test result or not.

    all this implementation can soon be replaced by checking whether
    query_result['type'] == 'sqlTest', which should be GA Apr 28th 2025
    """
    # test scoped on the node (table)
    result_name = query_result["name"]
    if result_name in test_names.get(node_id, {}):
        return True

    # test scoped on the column
    if result_name.endswith(_NULL_SUFFIX) or result_name.endswith(
        _UNIQUE_SUFFIX
    ):
        column_name = result_name.split(":")[0]
        if column_name in column_names.get(node_id, {}):
            return True
    return False


def test_names_per_node(nodes: SerializedAsset) -> NodeIDToNamesMapping:
    """mapping nodeID: set(testName)"""
    mapping: dict[str, set[str]] = {}
    for node in nodes:
        node_id = node["id"]
        tests = node.get("metadata", {}).get("appliedNodeTests", [])
        mapping[node_id] = {test["name"] for test in tests}
    return mapping


def column_names_per_node(nodes: SerializedAsset) -> NodeIDToNamesMapping:
    """mapping nodeID: set(columnNames)"""
    mapping: dict[str, set[str]] = {}
    for node in nodes:
        node_id = node["id"]
        columns = node.get("metadata", {}).get("columns", [])
        mapping[node_id] = {column["name"] for column in columns}
    return mapping
