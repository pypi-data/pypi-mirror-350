"""Module with utilities related to handling Jinja variables."""

import logging
import os
import re
import typing as t

import flywheel
import pandas as pd
from dotty_dict import Dotty
from ruamel.yaml import YAML

KEY_TYPES = ["PUBLIC_KEY", "PRIVATE_KEY", "SECRET_KEY"]
DEFAULT_REQUIRED_COLUMNS = ["subject.label"]
DEFAULT_SUBJECT_CODE_COL = "subject.label"
DEFAULT_NEW_SUBJECT_LOC = "export.subject.label"

log = logging.getLogger(__name__)


def get_jinja_variables(deid_template_path: os.PathLike) -> t.Tuple[list, list]:
    """Gets the jinja variables (`"{{ VARIABLE }}"`) and sorts by type.

    Args:
        deid_template_path: Path to deid template YAML profile

    Returns:
        list: variables to be set from Flywheel `subject` metadata
        list: variables to be set from CSV input file
    """

    with open(deid_template_path, "r") as fid:
        deid_template_str = fid.read()
    jinja_vars = re.findall(r"{{.*}}", deid_template_str)
    jinja_vars = [v.strip("{} ") for v in jinja_vars]
    jinja_vars = [v for v in jinja_vars if v not in KEY_TYPES]
    subj_vars, csv_vars = [], []
    for v in jinja_vars:
        (subj_vars if v.startswith("subject.") else csv_vars).append(v)
    subj_vars = [v for v in set(subj_vars)]
    csv_vars = [v for v in set(csv_vars)]

    return subj_vars, csv_vars


def get_subject_df(
    origin: flywheel.Project | flywheel.Subject | flywheel.Session,
    subj_vars: t.Optional[list] = [],
):
    """Given origin container and metadata variables from profile, returns DataFrame.

    Args:
        origin: Flywheel container (Project, Subject, Session)
        subj_vars: List of Jinja variables that begin with `subject.`

    Returns:
        pd.DataFrame: Metadata df with `subject.label` + `subj_vars` cols
    """
    if origin.container_type == "project":
        subjects = origin.subjects.find()
    elif origin.container_type == "subject":
        subjects = [origin]
    elif origin.container_type == "session":
        subjects = [origin.subject]

    subj_df = pd.DataFrame(
        columns=subj_vars, index=[subject.label for subject in subjects]
    )
    subj_df.index.name = "subject.label"

    for subject in subjects:
        subject = subject.reload()
        dotty_subj = Dotty(subject.to_dict())
        for var in subj_vars:
            if val := dotty_subj.get(var.removeprefix("subject.")):
                subj_df.loc[subject.label, var] = val
            else:
                log.warning(
                    f"No value for {subject.label} {var}. Value will be set as blank. "
                    "This may result in an invalid deid profile."
                )
                subj_df.loc[subject.label, var] = ""

    subj_df.columns = subj_df.columns.str.replace(".", "_")
    subj_df.reset_index(inplace=True)

    return subj_df


def get_csv_df(  # noqa: PLR0913
    deid_template_path: os.PathLike,
    csv_path: os.PathLike,
    subject_label_col: str = DEFAULT_SUBJECT_CODE_COL,
    new_subject_label_loc: str = DEFAULT_NEW_SUBJECT_LOC,
    required_cols: t.Optional[list] = None,
    csv_vars: t.Optional[list] = [],
) -> pd.DataFrame:
    """Creates dataframe from input CSV and validates with deid_template.

    Args:
        deid_template_path: Path to deid template YAML profile
        csv_path: Path to CSV file
        subject_label_col: Subject label column name
        new_subject_label_loc: New subject location in template (dotty dict notation)
        required_cols: List of required column names
        csv_vars: List of Jinja variables found in deid template YAML profile

    Returns:
        pd.DataFrame: DataFrame of template updates according to CSV input
    """
    with open(deid_template_path, "r") as fid:
        yaml = YAML(typ="rt")
        deid_template = yaml.load(fid)

    csv_df = pd.read_csv(csv_path, dtype=str)

    # Check that all expected variables exist
    if required_cols is None:
        required_cols = DEFAULT_REQUIRED_COLUMNS
    required_cols += csv_vars
    required_cols = set(required_cols)
    for c in required_cols:
        if c not in csv_df:
            raise ValueError(f"Column {c} is missing from dataframe")
    for c in csv_df:
        if c not in required_cols:
            log.debug(f"Column {c} not found in DeID template")

    # Check for uniqueness of subject columns
    if subject_label_col in csv_df:
        if not csv_df[subject_label_col].is_unique:
            raise ValueError(f"{subject_label_col} is not unique in csv")

    new_subject_col = Dotty(deid_template).get(new_subject_label_loc, "").strip("{} ")
    if new_subject_col in csv_df:
        if not csv_df[new_subject_col].is_unique:
            raise ValueError(f"{new_subject_col} is not unique in csv")

    return csv_df


def create_jinja_var_df(
    template_path: os.PathLike,
    origin: flywheel.Project | flywheel.Subject | flywheel.Session,
    csv_path: t.Optional[os.PathLike],
) -> t.Optional[pd.DataFrame]:
    """Creates a DataFrame of subject-specific deid template variables

    Args:
        template_path: Path to deid template
        origin: Flywheel container (Project, Subject, Session)
        csv_path: Path to subject_csv

    Returns:
        pd.DataFrame: Dataframe of subject-specific template updates, else None
    """
    subj_df, csv_df = None, None
    subj_vars, csv_vars = get_jinja_variables(template_path)
    if subj_vars:
        subj_df = get_subject_df(origin, subj_vars)
    if csv_vars and csv_path:
        csv_df = get_csv_df(template_path, csv_path, csv_vars=csv_vars)
    elif csv_vars and not csv_path:
        # deid profile has CSV Jinja variables but no CSV was provided
        log.warning(
            "The deid_profile includes Jinja variable notation but no subject_csv "
            "was provided to fill these variables. "
            f"Found variables: {', '.join(csv_vars)}."
        )
        # Just warn, or warn and exit?

    if isinstance(subj_df, pd.DataFrame) and isinstance(csv_df, pd.DataFrame):
        return pd.merge(subj_df, csv_df, on="subject.label", how="outer")
    elif isinstance(subj_df, pd.DataFrame):
        return subj_df
    return csv_df
