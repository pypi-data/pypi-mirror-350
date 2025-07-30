from .enums import LineageEntity
from .lineage import LineageProcessor, valid_lineage

_OLDER_DATE = "2025-01-01 00:00:01.0"
_CLOSER_DATE = "2025-01-01 02:02:02.0"

_TABLE_LINEAGES = [
    {
        "source_table_full_name": "a.b.source",
        "target_table_full_name": "a.b.target",
        "event_time": _CLOSER_DATE,
        "other": "more recent stuff",
    },
    {
        "source_table_full_name": "a.b.source",
        "target_table_full_name": "a.b.target",
        "event_time": _OLDER_DATE,
        "other": "stuff that's too old",
    },
    {
        "source_table_full_name": "no target",
        "target_table_full_name": None,
        "event_time": _CLOSER_DATE,
    },
    {
        "source_table_full_name": None,
        "target_table_full_name": "no source",
        "event_time": _CLOSER_DATE,
    },
]


_COLUMN_LINEAGES = [
    {
        "source_table_full_name": "a.b.source",
        "source_column_name": "src_col",
        "target_table_full_name": "a.b.target",
        "target_column_name": "trgt_col",
        "event_time": _OLDER_DATE,
        "other": "old stuff",
    },
    {
        "source_table_full_name": "a.b.source",
        "source_column_name": "src_col",
        "target_table_full_name": "a.b.target",
        "target_column_name": "trgt_col",
        "event_time": _CLOSER_DATE,
        "other": "newer stuff",
    },
    {
        "source_table_full_name": "a.b.toto",
        "source_column_name": "toto_col",
        "target_table_full_name": "a.b.tata",
        "target_column_name": "tata_col",
        "event_time": _OLDER_DATE,
    },
    {
        "source_table_full_name": "a.b.source",
        "source_column_name": "a.b.source",
        "target_table_full_name": None,
        "target_column_name": None,
        "event_time": _CLOSER_DATE,
    },
]


def test_valid_lineage():
    table_links = valid_lineage(_TABLE_LINEAGES, LineageEntity.TABLE)

    assert len(table_links) == 1
    assert table_links[0]["source_table_full_name"] == "a.b.source"
    assert table_links[0]["target_table_full_name"] == "a.b.target"
    assert table_links[0]["event_time"] == _CLOSER_DATE
    assert table_links[0]["other"] == "more recent stuff"


def test_LineageLinks_add():
    deduplicated_lineage = LineageProcessor(LineageEntity.COLUMN)
    for link in _COLUMN_LINEAGES:
        deduplicated_lineage.add(link)

    lineage = deduplicated_lineage.lineage
    assert len(lineage) == 2
    assert ("a.b.source.src_col", "a.b.target.trgt_col") in lineage
    assert ("a.b.toto.toto_col", "a.b.tata.tata_col") in lineage
    assert (
        lineage[("a.b.source.src_col", "a.b.target.trgt_col")]["other"]
        == "newer stuff"
    )
