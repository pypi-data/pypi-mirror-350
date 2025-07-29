import re
import typing as t
from collections.abc import Mapping
from datetime import datetime
from functools import lru_cache
from pathlib import Path

import flywheel
from dateutil import parser
from dotty_dict import Dotty
from flywheel_migration import util
from flywheel_migration.deidentify.json_file_profile import JSONFileProfile, JSONRecord

META_ALLOW_LIST_DICT = {
    "file": {"classification", "info", "modality", "type"},
    "acquisition": ("timestamp", "timezone", "uid", "info", "label", "tags"),
    "session": (
        "age",
        "operator",
        "timestamp",
        "timezone",
        "uid",
        "weight",
        "info",
        "label",
        "tags",
    ),
    "subject": (
        "firstname",
        "lastname",
        "date_of_birth",
        "sex",
        "cohort",
        "mlset",
        "ethnicity",
        "race",
        "species",
        "strain",
        "info",
        "type",
        "label",
        "tags",
    ),
    "project": ("info", "description", "tags"),
}
# all non defined here are assumed to be str and no constrain
KEY_TYPE = {
    "file": {
        "classification": (dict, None),
        "info": (dict, None),
    },
    "acquisition": {
        "timestamp": (datetime, None),
        "info": (dict, None),
        "tags": (list, None),
    },
    "session": {
        "age": (int, None),
        "timestamp": (datetime, None),
        "weight": (float, None),
        "info": (dict, None),
        "tags": (list, None),
    },
    "subject": {
        "sex": (str, [None, "male", "female", "other", "unknown"]),
        "cohort": (str, [None, "Control", "Study"]),
        "mlset": (str, [None, "Training", "Test", "Validation"]),
        "type": (str, [None, "human", "animal", "phantom"]),
        "race": (
            str,
            [
                None,
                "American Indian or Alaska Native",
                "Asian",
                "Native Hawaiian or Other Pacific Islander",
                "Black or African American",
                "White",
                "More Than One Race",
                "Unknown or Not Reported",
            ],
        ),
        "ethnicity": (
            str,
            [
                None,
                "Hispanic or Latino",
                "Not Hispanic or Latino",
                "Unknown or Not Reported",
            ],
        ),
        "species": (str, None),
        "info": (dict, None),
        "tags": (list, None),
    },
    "project": {
        "info": (dict, None),
        "tags": (list, None),
    },
}
ASSETS_PATH = Path(__file__).parent / "assets"
DENY_LIST = {"info.header"}
DEFAULT_ALL = False

# To store container
PROJECT_SUBJECT_CACHE = {}


class ContainerToJSONFormatter:
    """Class to get container allowed metadata with its parent(s)"""

    expose_parents = {
        "project": [],
        "subject": ["project"],
        "session": ["project", "subject"],
        "acquisition": ["project", "subject", "session"],
    }

    def __init__(self, client: flywheel.Client, config: t.Optional[dict] = None):
        self.client = client
        self.config = config if config else {}

    @staticmethod
    def filter(
        container: flywheel.Subject | flywheel.Session | flywheel.Acquisition,
        config: t.Optional[dict] = None,
    ):
        """Return a filtered container dict representation with editable key/value

        Args:
            container (object): A flywheel container

        Returns:
            dict: filtered container representation with editable key/value
        """
        config = config if config else {}
        cont_dict = container.to_dict()
        cont_type = container.container_type
        if cont_type == "file" and not config.get("include-info-header", False):
            # drop info.header
            if "header" in cont_dict["info"]:
                cont_dict["info"].pop("header")
        return {k: cont_dict[k] for k in META_ALLOW_LIST_DICT[cont_type]}

    def apply_nested_dict(self, ob, func):
        for k, v in ob.items():
            if isinstance(v, Mapping):
                self.apply_nested_dict(v, func)
            else:
                ob[k] = func(v)

    def _get_and_cache(self, container_id: str, container_type: str):
        """Returns container filtered metadata, caching it appropriately."""
        if container_type in ["project", "subject"]:
            if container_id in PROJECT_SUBJECT_CACHE:
                return PROJECT_SUBJECT_CACHE[container_id]
            else:
                getter = getattr(self.client, f"get_{container_type}")
                parent_cont = getter(container_id)
                filter_container = self.filter(parent_cont)
                PROJECT_SUBJECT_CACHE[container_id] = filter_container
                return filter_container
        elif container_type in ["session", "acquisition"]:
            getter = getattr(self.client, f"get_{container_type}")
            return self._get_session_acquisition(getter, container_id)

    @lru_cache(maxsize=5000)
    def _get_session_acquisition(self, getter, container_id: str):
        """Returns session or acquisition filtered metadata."""
        parent_cont = getter(container_id)
        return self.filter(parent_cont)

    def format(
        self,
        container: flywheel.Project
        | flywheel.Subject
        | flywheel.Session
        | flywheel.Acquisition,
        add_parents: bool = True,
    ) -> dict:
        """Return a dictionary representation of the container and its parents

        Note:
            * project and subject are cached in PROJECT_SUBJECT_CACHE
            * session and acquisition are cached with lru with max size 10k.
        """
        f_cont_dict = self.filter(container, self.config)
        if add_parents:
            if container.container_type != "file":
                for parent_type in self.expose_parents[container.container_type]:
                    parent_id = container.parents[parent_type]
                    f_cont_dict[parent_type] = self._get_and_cache(
                        parent_id, parent_type
                    )
            elif container.container_type == "file":
                f_parent_dict = {}
                parent = container.parent
                f_parent_dict[parent.container_type] = self.filter(parent, self.config)
                for parent_type in self.expose_parents[parent.container_type]:
                    parent_id = parent.parents[parent_type]
                    filter_container = self._get_and_cache(parent_id, parent_type)
                    f_parent_dict[parent_type] = filter_container
                f_cont_dict.update(f_parent_dict)
            else:
                raise TypeError(
                    f"Unrecognized container type: {container.container_type}"
                )

        # datetime to str
        self.apply_nested_dict(
            f_cont_dict, lambda x: str(x) if isinstance(x, datetime) else x
        )

        return f_cont_dict


class JSONToContainerFormatter:
    """Class to format a JSONRecord into key/value update for a container"""

    def __init__(self, container_type: t.Optional[str] = None):
        self.container_type = container_type

    def filter(
        self,
        record: JSONRecord,
        config: t.Optional[dict] = None,
        all_: bool = DEFAULT_ALL,
    ) -> JSONRecord:
        """Returns a cleaned JSONRecord, filtering out none editable keys and handling
        the self.all_ config option.

        Args:
            record (JSONRecord): A JSONRecord
        """
        if not self.container_type:
            raise AttributeError("self.container_type must be defined to clean record")
        if not all_ and not config:
            raise ValueError("config must be defined when all_=False")

        if not all_:
            # If all_=False, only keep fields defined in name or regex
            record_filtered = Dotty({})
            all_paths = record.get_all_dotty_paths()
            for field in config.get("fields", []):
                if "name" in field:
                    record_filtered[field["name"]] = record[field["name"]]
                if "regex" in field:
                    reg = re.compile(field["regex"])
                    for p in all_paths:
                        if reg.match(p):
                            record_filtered[p] = record[p]
            record = record_filtered

        # record parent container metadata and need to be cleaned
        for k in list(record.keys()):
            if k not in META_ALLOW_LIST_DICT[self.container_type]:
                record.pop(k)

        return record

    def format(self, record: JSONRecord) -> dict:  # noqa: PLR0912
        """Format record to container key/value

        Args:
            record (JSONRecord): A JSONRecord.

        Returns:
            dict: A valid Flywheel container key/value dictionary to update properties
                of container
        """
        if not self.container_type:
            raise AttributeError("self.container_type must be defined to format record")

        record_dict = record.to_dict()

        # Flywheel SDK expects values with a specific format
        for k, v in record_dict.items():
            expected_type, constraint = KEY_TYPE[self.container_type].get(
                k, (str, None)
            )
            if constraint:
                if isinstance(constraint, list):
                    # to check value is in allowed value
                    if v not in constraint:
                        raise ValueError(
                            f"{k} value must be in {constraint}. Currently {v}."
                        )
                    continue
            if v is not None and not isinstance(v, expected_type):
                if k == "timestamp":
                    record_dict[k] = parser.parse(v)
                else:
                    # e.g. to cast int, float
                    record_dict[k] = expected_type(v)
            elif v is None or v == "":
                if expected_type is str and k != "date_of_birth":
                    # date_of_birth cannot be empty string
                    record_dict[k] = ""
                elif expected_type is list:
                    record_dict[k] = []
                elif expected_type is dict:
                    record_dict[k] = {}
                else:
                    record_dict[k] = None
        record_dict = {k: v for k, v in record_dict.items() if v is not None}
        return record_dict


def get_deid_fw_container_metadata(
    client: flywheel.Client,
    config: dict,
    container: flywheel.Subject | flywheel.Session | flywheel.Acquisition,
) -> dict:
    """Returns a de-id dictionary representation of the flywheel container metadata

    Args:
        client (flywheel.Client): A Flywheel client
        config (dict): Dictionary to use to instantiate a JSONFileProfile
        container (object): A flywheel container

    Returns:
        dict: Dictionary representation of a de-id container metadata
    """
    profile = JSONFileProfile()
    profile.load_config(config)
    formatter = ContainerToJSONFormatter(client, config=config)
    record = JSONRecord.from_dict(formatter.format(container))
    for field in profile.fields:
        field.deidentify(profile, {}, record)

    formatter = JSONToContainerFormatter(container_type=container.container_type)
    record = formatter.filter(
        record, config=config, all_=config.get("all", DEFAULT_ALL)
    )

    record["info.export.origin_id"] = util.hash_value(
        container.id, salt=container.parents.get("project")
    )

    container_dict = formatter.format(record)

    return container_dict
