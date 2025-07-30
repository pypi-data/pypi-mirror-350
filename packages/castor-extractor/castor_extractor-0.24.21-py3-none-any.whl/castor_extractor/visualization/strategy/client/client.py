import logging
from collections.abc import Iterator
from enum import Enum
from typing import Any, Callable, Optional
from urllib.parse import urlparse

from mstrio.connection import Connection  # type: ignore
from mstrio.helpers import IServerError  # type: ignore
from mstrio.modeling import (  # type: ignore
    list_attributes,
    list_facts,
    list_metrics,
)
from mstrio.project_objects import (  # type: ignore
    Report,
    list_dashboards,
    list_documents,
    list_olap_cubes,
    list_reports,
)
from mstrio.server import Environment  # type: ignore
from mstrio.types import ObjectSubTypes, ObjectTypes  # type: ignore
from mstrio.users_and_groups import User, list_users  # type: ignore
from mstrio.utils.entity import Entity  # type: ignore
from mstrio.utils.helper import is_dashboard  # type: ignore
from pydantic import BaseModel, ConfigDict

from ..assets import StrategyAsset
from .credentials import StrategyCredentials

logger = logging.getLogger(__name__)

_BATCH_SIZE: int = 100


class URLTemplates(Enum):
    DASHBOARD = "https://{hostname}/MicroStrategyLibrary/app/{project_id}/{id_}"
    DOCUMENT = "https://{hostname}/MicroStrategy/servlet/mstrWeb?documentID={id_}&projectID={project_id}"
    REPORT = "https://{hostname}/MicroStrategy/servlet/mstrWeb?reportID={id_}&projectID={project_id}"
    FOLDER = "https://{hostname}/MicroStrategy/servlet/mstrWeb?folderID={id_}&projectID={project_id}"


def _is_dashboard(entity: Entity) -> bool:
    """
    Returns True if the entity is a Dashboard. They can only be distinguished
    from Documents by checking the `view_media` property.
    """
    is_type_document = entity.type == ObjectTypes.DOCUMENT_DEFINITION
    return is_type_document and is_dashboard(entity.view_media)


def _is_report(entity: Entity) -> bool:
    """
    Returns True if the entity is a Report. Cubes share the same type as Reports,
    so the subtype must be checked.
    """
    is_type_report = entity.type == ObjectTypes.REPORT_DEFINITION
    is_subtype_cube = entity.subtype == ObjectSubTypes.OLAP_CUBE.value
    return is_type_report and not is_subtype_cube


def _safe_get_attribute(entity: Entity, attribute: str) -> Optional[str]:
    """
    Some properties may raise an error. Example: retrieving a Report's `sql` fails if the Report has not been published.
    This safely returns the attribute value, or None if the retrieval fails.
    """
    try:
        value = getattr(entity, attribute)
    except IServerError as e:
        logger.error(f"Could not get {attribute} for entity {entity.id}: {e}")
        value = None
    return value


class Dependency(BaseModel):
    id: str
    name: str
    subtype: int
    type: int

    model_config = ConfigDict(extra="ignore")


def _list_dependencies(entity: Entity) -> list[dict]:
    """Lists the entity's dependencies, keeping only relevant fields."""
    dependencies: list[dict] = []

    offset = 0
    while True:
        batch = entity.list_dependencies(offset=offset, limit=_BATCH_SIZE)
        dependencies.extend(batch)
        if len(batch) < _BATCH_SIZE:
            break
        offset += _BATCH_SIZE

    return [
        Dependency(**dependency).model_dump() for dependency in dependencies
    ]


def _level_1_folder_id(folders: list[dict]) -> str:
    """Searches for the first enclosing folder and returns its ID."""
    for folder in folders:
        if folder["level"] == 1:
            return folder["id"]

    raise ValueError("No level 1 folder found")


class StrategyClient:
    """Connect to Strategy through mstrio-py and fetch main assets."""

    def __init__(self, credentials: StrategyCredentials):
        self.base_url = credentials.base_url
        self.connection = Connection(
            base_url=self.base_url,
            username=credentials.username,
            password=credentials.password,
        )

        self.hostname = urlparse(self.base_url).hostname

        if credentials.project_ids:
            self.project_ids = credentials.project_ids
        else:
            env = Environment(connection=self.connection)
            self.project_ids = [project.id for project in env.list_projects()]

    def close(self):
        self.connection.close()

    def _url(self, entity: Entity) -> str:
        """
        Formats the right URL.
        * Dashboards : viewed in MicroStrategy
        * Reports and Documents : viewed in MicroStrategy Web
        * other (i.e. Cubes): the URL leads to the folder in MicroStrategy Web
        """
        if _is_dashboard(entity):
            id_ = entity.id
            template = URLTemplates.DASHBOARD

        elif entity.type == ObjectTypes.DOCUMENT_DEFINITION:
            id_ = entity.id
            template = URLTemplates.DOCUMENT

        elif _is_report(entity):
            id_ = entity.id
            template = URLTemplates.REPORT

        else:
            # default to folder URL
            id_ = _level_1_folder_id(entity.ancestors)
            template = URLTemplates.FOLDER

        return template.value.format(
            hostname=self.hostname,
            id_=id_,
            project_id=entity.project_id,
        )

    def _common_entity_properties(
        self,
        entity: Entity,
        with_url: bool = True,
        with_description: bool = True,
    ) -> dict:
        """
        Returns the entity's properties, including its dependencies
        and optional URL and/or description.
        """
        dependencies = _list_dependencies(entity)
        owner_id = entity.owner.id if isinstance(entity.owner, User) else None
        properties = {
            "dependencies": dependencies,
            "id": entity.id,
            "location": entity.location,
            "name": entity.name,
            "owner_id": owner_id,
            "subtype": entity.subtype,
            "type": entity.type.value,
        }

        if with_url:
            properties["url"] = self._url(entity)

        if with_description:
            properties["description"] = _safe_get_attribute(
                entity, "description"
            )

        return properties

    def _report_properties(self, report: Report) -> dict[str, Any]:
        """
        Report properties contain an optional SQL source query. Due to a typing
        bug in the mstrio package, the typing must be ignored.
        """
        properties = self._common_entity_properties(report)  # type: ignore
        properties["url"] = self._url(report)  # type: ignore
        properties["sql"] = _safe_get_attribute(report, "sql")  # type: ignore
        return properties

    @staticmethod
    def _user_properties(user: User) -> dict[str, Any]:
        return {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.default_email_address,
        }

    def _fetch_entities(
        self,
        extract_callback: Callable,
        with_url: bool = True,
        with_description: bool = True,
        custom_property_extractor: Optional[Callable] = None,
    ) -> Iterator[dict[str, Any]]:
        """
        Yields all entities across all projects using the given retrieval function from the mstrio package.
        """
        for project_id in self.project_ids:
            self.connection.select_project(project_id=project_id)

            entities = extract_callback(connection=self.connection)

            for entity in entities:
                try:
                    if custom_property_extractor:
                        yield custom_property_extractor(entity)
                    else:
                        yield self._common_entity_properties(
                            entity,
                            with_url=with_url,
                            with_description=with_description,
                        )
                except IServerError as e:
                    logger.error(
                        f"Could not fetch attributes for entity {entity.id}: {e}"
                    )

    def _fetch_attributes(self) -> Iterator[dict[str, Any]]:
        return self._fetch_entities(
            list_attributes,
            with_url=False,
        )

    def _fetch_cubes(self) -> Iterator[dict[str, Any]]:
        return self._fetch_entities(list_olap_cubes)

    def _fetch_dashboards(self) -> Iterator[dict[str, Any]]:
        return self._fetch_entities(list_dashboards)

    def _fetch_documents(self) -> Iterator[dict[str, Any]]:
        return self._fetch_entities(list_documents)

    def _fetch_facts(self) -> Iterator[dict[str, Any]]:
        """Yields all facts. Descriptions are not needed for this entity type."""
        return self._fetch_entities(
            list_facts,
            with_url=False,
            with_description=False,
        )

    def _fetch_metrics(self) -> Iterator[dict[str, Any]]:
        return self._fetch_entities(
            list_metrics,
            with_url=False,
        )

    def _fetch_reports(self) -> Iterator[dict[str, Any]]:
        return self._fetch_entities(
            list_reports,
            custom_property_extractor=self._report_properties,
        )

    def _fetch_users(self) -> Iterator[dict[str, Any]]:
        return self._fetch_entities(
            list_users,
            custom_property_extractor=self._user_properties,
        )

    def fetch(self, asset: StrategyAsset):
        """Fetch the given asset type from Strategy"""
        if asset == StrategyAsset.ATTRIBUTE:
            yield from self._fetch_attributes()

        elif asset == StrategyAsset.CUBE:
            yield from self._fetch_cubes()

        elif asset == StrategyAsset.DASHBOARD:
            yield from self._fetch_dashboards()

        elif asset == StrategyAsset.DOCUMENT:
            yield from self._fetch_documents()

        elif asset == StrategyAsset.FACT:
            yield from self._fetch_facts()

        elif asset == StrategyAsset.METRIC:
            yield from self._fetch_metrics()

        elif asset == StrategyAsset.REPORT:
            yield from self._fetch_reports()

        elif asset == StrategyAsset.USER:
            yield from self._fetch_users()

        else:
            raise NotImplementedError(f"Asset type {asset} not implemented yet")
