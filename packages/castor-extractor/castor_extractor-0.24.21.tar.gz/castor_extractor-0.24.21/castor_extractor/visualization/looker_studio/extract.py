import json
import logging
from collections.abc import Iterable
from typing import Optional, Union, cast

from ...utils import (
    OUTPUT_DIR,
    current_timestamp,
    deep_serialize,
    from_env,
    get_output_filename,
    write_json,
    write_summary,
)
from .assets import LookerStudioAsset
from .client import LookerStudioClient, LookerStudioCredentials

logger = logging.getLogger(__name__)

APPLICATION_CREDENTIALS = "GOOGLE_APPLICATION_CREDENTIALS"
LOOKER_STUDIO_ADMIN_EMAIL = "CASTOR_LOOKER_STUDIO_ADMIN_EMAIL"


def iterate_all_data(
    client: LookerStudioClient,
    has_view_activity_logs: bool = True,
) -> Iterable[tuple[LookerStudioAsset, Union[list, dict]]]:
    assets_to_extract = LookerStudioAsset.mandatory

    if has_view_activity_logs:
        assets_to_extract.add(LookerStudioAsset.VIEW_ACTIVITY)

    for asset in assets_to_extract:
        logger.info(f"Extracting {asset.name} from API")
        data = list(deep_serialize(client.fetch(asset)))
        yield asset, data
        logger.info(f"Extracted {len(data)} {asset.name} from API")


def _credentials(params: dict) -> LookerStudioCredentials:
    """
    Builds the Looker Studio credentials by combining the Service Account
    credentials with the admin email.
    """
    path = params.get("credentials") or from_env(APPLICATION_CREDENTIALS)
    logger.info(f"Looker Studio credentials loaded from {path}")
    with open(path) as file:
        credentials = cast(dict, json.load(file))

    admin_email = params.get("admin_email") or from_env(
        LOOKER_STUDIO_ADMIN_EMAIL
    )
    credentials["admin_email"] = admin_email
    has_view_activity_logs = not params["skip_view_activity_logs"]
    credentials["has_view_activity_logs"] = has_view_activity_logs
    return LookerStudioCredentials(**credentials)


def _bigquery_credentials_or_none(params: dict) -> Optional[dict]:
    """Extracts optional GCP credentials to access BigQuery"""
    path = params.get("bigquery_credentials") or from_env(
        APPLICATION_CREDENTIALS,
        allow_missing=True,
    )
    if not path:
        return None

    logger.info(f"BigQuery credentials loaded from {path}")
    with open(path) as file:
        return cast(dict, json.load(file))


def extract_all(**kwargs) -> None:
    """
    Extracts data from Looker Studio and stores the output files locally under
    the given output_directory.
    """
    output_directory = kwargs.get("output") or from_env(OUTPUT_DIR)

    credentials = _credentials(kwargs)
    has_view_activity_logs = bool(credentials.has_view_activity_logs)

    bigquery_credentials = _bigquery_credentials_or_none(kwargs)

    client = LookerStudioClient(
        credentials=credentials,
        bigquery_credentials=bigquery_credentials,
    )
    ts = current_timestamp()

    for key, data in iterate_all_data(client, has_view_activity_logs):
        filename = get_output_filename(key.name.lower(), output_directory, ts)
        write_json(filename, data)

    write_summary(output_directory, ts)
