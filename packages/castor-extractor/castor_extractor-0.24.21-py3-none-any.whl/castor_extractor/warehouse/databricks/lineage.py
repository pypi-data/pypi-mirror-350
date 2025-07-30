from typing import Iterable, Optional

from .enums import LineageEntity


class LineageProcessor:
    """
    helper class that handles lineage deduplication and filtering
    """

    def __init__(self, lineage_entity: LineageEntity):
        self.lineage_entity = lineage_entity

        self.lineage: dict[tuple[str, str], dict] = dict()

    def _parent_path(self, link) -> Optional[str]:
        if self.lineage_entity == LineageEntity.TABLE:
            return link["source_table_full_name"]

        source_table = link["source_table_full_name"]
        source_column = link["source_column_name"]
        if not (source_table and source_column):
            return None

        return f"{source_table}.{source_column}"

    def _child_path(self, link) -> Optional[str]:
        if self.lineage_entity == LineageEntity.TABLE:
            return link["target_table_full_name"]

        target_table = link["target_table_full_name"]
        target_column = link["target_column_name"]
        if not (target_table and target_column):
            return None

        return f"{target_table}.{target_column}"

    def add(self, link: dict) -> None:
        """
        If the parent and child paths are valid, keeps the most recent lineage
        link in the `self.lineage` map.
        """
        parent = self._parent_path(link)
        child = self._child_path(link)
        timestamp = link["event_time"]

        if not (parent and child and parent != child):
            return

        key = (parent, child)
        if key in self.lineage and self.lineage[key]["event_time"] > timestamp:
            return

        self.lineage[key] = link


def valid_lineage(
    lineage: Iterable[dict], lineage_entity: LineageEntity
) -> list[dict]:
    """
    Filters out self-lineage or lineage with a missing source or target path,
    then deduplicates by picking the link with the most recent event timestmap.
    """
    deduplicated_lineage = LineageProcessor(lineage_entity)

    for link in lineage:
        deduplicated_lineage.add(link)

    return list(deduplicated_lineage.lineage.values())
