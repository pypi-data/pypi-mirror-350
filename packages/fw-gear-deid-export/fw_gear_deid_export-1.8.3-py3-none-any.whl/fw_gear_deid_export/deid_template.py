#!/usr/bin/env python3

import argparse
import logging
import os
import re
import tempfile
import typing as t
from pathlib import Path

import pandas as pd
from flywheel_migration import deidentify
from jinja2 import Environment
from ruamel.yaml import YAML

DEFAULT_SUBJECT_CODE_COL = "subject.label"
DEFAULT_NEW_SUBJECT_LOC = "export.subject.label"
ACTIONS_LIST = ["replace-with", "remove", "increment-date", "hash", "hashuid"]

logger = logging.getLogger(__name__)


def find_profile_element(d: dict, target: str) -> tuple[str | list, str, bool]:
    """Traverse dictionary following target and return matching element

    Args:
        d (dict): Dictionary from a deid profile template

        target (str): Period separated path in dictionary tree (e.g. dicom.filename.destination). If field action
            is targeted, format must match <filetype>.fields.<fieldname>.<actionname>
            (e.g. dicom.fields.PatientID.replace-with)

    Returns:
        element: Final element in the dictionary tree matching target (not the value) or list if is_fields=True
        target: Final key
        is_fields (bool): True is element is the list founds as value for key='fields'
    """
    tps = target.split(".")
    if len(tps) == 1:
        return d, target, False
    else:
        if tps[0] == "fields":
            return d["fields"], ".".join(tps[1:]), True
        if tps[0] == "groups":
            return d["groups"], ".".join(tps[1:]), True
        elif isinstance(d, list):
            return find_profile_element(d[int(tps[0])], ".".join(tps[1:]))
        else:
            return find_profile_element(d[tps[0]], ".".join(tps[1:]))


def _add_zip_member_validation(deid_template: dict):
    if "zip" in deid_template.keys():
        if "validate-zip-members" not in deid_template["zip"].keys():
            deid_template["zip"]["validate-zip-members"] = True
    return deid_template


def update_deid_profile(
    deid_template_path: os.PathLike,
    updates: t.Optional[dict] = None,
    dest_path: t.Optional[os.PathLike] = None,
) -> os.PathLike:
    """Return the updated deid profile

    Args:
        deid_template_path (Path-like): Path to deid profile template
        updates (dict): A dictionary of key/value to be updated (e.g. a row from a csv file)
        dest_path (Path-like): Path where update template is saved
    """

    load_path = deid_template_path

    # update jinja2 variable
    if updates:
        with open(load_path, "r") as fp:
            deid_template_str = fp.read()
            # remove quote around jinja var to allow for casting inferred from dataframe
            deid_template_str = re.sub(
                r"(?:\"|\'){{([^{}]+)}}(?:\"|\')", r"{{ \g<1> }}", deid_template_str
            )
            # substitute "." in variables for "_"
            deid_template_str = re.sub(r"{{([^{}]+)}}", clean_jinja, deid_template_str)
        env = Environment()
        jinja_template = env.from_string(deid_template_str)
        with open(dest_path, "w") as fp:
            fp.write(jinja_template.render(**updates))
        load_path = dest_path

    # ensure zip members are present
    yaml = YAML(typ="rt")
    with open(load_path, "r") as fid:
        deid_template = yaml.load(fid)
    if "only-config-profiles" not in deid_template.keys():
        deid_template["only-config-profiles"] = True
    # ensure deid-log not present
    if "deid-log" in deid_template.keys():
        logger.warning(
            "This gear does not support deid-log in deid-profile. Skipping deid-log.."
        )
        deid_template.pop("deid-log")
    deid_template = _add_zip_member_validation(deid_template)

    with open(dest_path, "w") as fid:
        yaml.dump(deid_template, fid)

    return dest_path


def clean_jinja(matchobj: re.Match):
    return matchobj.group(0).replace(".", "_")


def load_deid_profile(template_dict: dict) -> tuple[deidentify.DeIdProfile, dict]:
    """
    Load the flywheel.migration DeIdProfile at the profile_path

    Args:
        template_dict(dict): a dictionary loaded from the de-identification template file that will be provided as
            config to DeIdProfile

    Returns:
        flywheel_migration.deidentify.DeIdProfile, fw_metadata_profile
    """
    deid_profile = deidentify.DeIdProfile()
    deid_profile.load_config(template_dict)
    fw_metadata_profile = template_dict.get("flywheel", dict())
    return deid_profile, fw_metadata_profile


def get_updated_template(
    df: pd.DataFrame,
    deid_template_path: os.PathLike,
    subject_label: t.Optional[str] = None,
    subject_label_col: str = DEFAULT_SUBJECT_CODE_COL,
    dest_template_path: t.Optional[str] = None,
) -> str:
    """Return path to updated DeID profile

    Args:
        df (pandas.DataFrame): Dataframe representation of some mapping info
        subject_label (str): value matching subject_label_col in row used to update the template
        deid_template_path (path-like): Path to a deid template
        subject_label_col (str): Subject label column name
        dest_template_path (Path-like): Path to output DeID profile

    Returns:
        (str): Path to output DeID profile
    """

    series = df[df[subject_label_col] == subject_label]
    if series.empty:
        raise ValueError(f"{subject_label} not found in csv")
    else:
        series.pop(subject_label_col)
        if dest_template_path is None:
            dest_template_path = tempfile.NamedTemporaryFile().name
        update_deid_profile(
            deid_template_path,
            updates=series.to_dict("records")[0],
            dest_path=dest_template_path,
        )

    return dest_template_path


def process_csv(
    csv_path: os.PathLike,
    deid_template_path: os.PathLike,
    subject_label_col: str = DEFAULT_SUBJECT_CODE_COL,
    output_dir: str = "/tmp",
) -> dict:
    """Generate patient specific deid profile

    Args:
        csv_path (Path-like): Path to CSV file
        deid_template_path (Path-like): Path to the deid profile template
        output_dir (Path-like): Path to ouptut dir where yml are saved
        subject_label_col (str): Subject label column name

    Returns:
        dict: Dictionary with key/value = subject.label/path to updated deid profile
    """

    # validate(deid_template_path, csv_path)
    # TODO this function has changed a lot, need to check this workflow

    df = pd.read_csv(csv_path, dtype=str)

    deids_paths = {}
    for subject_label in df[subject_label_col]:
        dest_template_path = Path(output_dir) / f"{subject_label}.yml"
        deids_paths[subject_label] = get_updated_template(
            df,
            deid_template_path,
            subject_label=subject_label,
            subject_label_col=subject_label_col,
            dest_template_path=dest_template_path,
        )
    return deids_paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path", help="path to the CSV file")
    parser.add_argument(
        "deid_template_path", help="Path to source de-identification profile to modify"
    )
    parser.add_argument(
        "--output_directory", help="path to which to save de-identified template"
    )
    parser.add_argument(
        "--subject_label_col", help="Name of the column containing subject label"
    )

    args = parser.parse_args()

    res = process_csv(
        args.csv_path,
        args.deid_template_path,
        subject_label_col=args.subject_label_col,
        output_dir=args.output_directory,
    )

    print(res)
