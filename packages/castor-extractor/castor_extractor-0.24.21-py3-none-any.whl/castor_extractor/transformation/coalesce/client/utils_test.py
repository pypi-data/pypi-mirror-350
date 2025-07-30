from .utils import is_test


def test_is_test():
    test_names = {"some-uuid": {"check-mirrors", "check-seatbelt"}}
    column_names = {"some-uuid": {"carthago", "delenda", "est"}}

    happy_node_test = is_test(
        query_result={"name": "check-mirrors"},
        node_id="some-uuid",
        test_names=test_names,
        column_names=column_names,
    )
    assert happy_node_test is True

    unknown_node_test = is_test(
        query_result={"name": "check-engine"},
        node_id="some-uuid",
        test_names=test_names,
        column_names=column_names,
    )
    assert unknown_node_test is False

    happy_column_test_unique = is_test(
        query_result={"name": "carthago: Unique"},
        node_id="some-uuid",
        test_names=test_names,
        column_names=column_names,
    )
    assert happy_column_test_unique is True

    happy_column_test_null = is_test(
        query_result={"name": "carthago: Null"},
        node_id="some-uuid",
        test_names=test_names,
        column_names=column_names,
    )
    assert happy_column_test_null is True

    unknown_column_test = is_test(
        query_result={"name": "rome: Unique"},
        node_id="some-uuid",
        test_names=test_names,
        column_names=column_names,
    )
    assert unknown_column_test is False

    unknown_node_id_test = is_test(
        query_result={"name": "whatever: Unique"},
        node_id="unknown-uuid",
        test_names=test_names,
        column_names=column_names,
    )
    assert unknown_node_id_test is False
