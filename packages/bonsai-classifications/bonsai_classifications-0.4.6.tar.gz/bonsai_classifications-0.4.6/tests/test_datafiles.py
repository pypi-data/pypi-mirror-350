# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 11:45:14 2025
A test function that checks the correspondence files of external codes to Bonsai
and the associated tree files. It checks for missing columns and missing values.

For convenience, at the bottom there is a function to update the column names
to match the new format.

Author: Sander van Nielen (AAU)
"""
from logging import getLogger
from pathlib import Path

import pandas as pd
import pytest

logger = getLogger("root")

# directories to be checked
activitytype_path = Path("src/classifications/data/flow/activitytype")
flowobject_path = Path("src/classifications/data/flow/flowobject")
flow_path = Path("src/classifications/data/flow")

# Function to load CSV and check required columns
def assert_columns(file: Path, required_columns: list):
    df = pd.read_csv(file, dtype=str)
    for col in required_columns:
        assert col in df.columns, f"'{col}' column missing in {file.name}"
    return df


@pytest.mark.parametrize(
    "directory",
    [activitytype_path, flowobject_path],
    ids=["activitytype", "flowobject"],
)
def test_files(directory):
    test_pass = True

    # Check all tree_*.csv files
    tree_files = directory.glob("tree_*.csv")
    for tree_file in tree_files:
        df_tree = assert_columns(tree_file, ["level"])

        level_0 = len(df_tree[df_tree.level == "0"])
        if level_0 > 6:
            logger.warning(
                f"{level_0} items have level 0 in {directory.name}/{tree_file.name}"
            )

    # Check conc files
    conc_files = list(directory.glob("conc_*_bonsai.csv")) + list(
        directory.glob("conc_bonsai_*.csv")
    )
    for conc_file in conc_files:
        df_conc = assert_columns(
            conc_file,
            ["classification_from", "classification_to", "comment"],
        )
        # Check if the auto-filled columns are filled
        for col in ["comment"]:
            if df_conc[col].isna().any():
                logger.error(f"Empty '{col}' in {conc_file.name}")
                test_pass = False
        # Check for 'one-sided' links
        for col in [f"{directory.name}_from", f"{directory.name}_to"]:
            if df_conc[col].isna().any():
                logger.error(f"Empty values in '{col}' in {conc_file.name}")
                test_pass = False
                df_conc = df_conc[df_conc[col].notna()]

        # Search the associated tree file
        tree_filename = conc_file.name.replace("conc_", "tree_").replace("_bonsai", "")
        tree_file = directory / tree_filename
        if not tree_file.exists():
            logger.error(f"Missing file: {tree_file.name}")
            test_pass = False
            continue

        # Check the columns and levels of the tree file
        df_tree = assert_columns(tree_file, ["code", "name"])
        if "level" not in df_tree.columns:
            logger.error(f"'level' column missing in {tree_file.name}")
            test_pass = False
        else:
            level_0 = len(df_tree[df_tree.level == "0"])
            if level_0 > 3:
                logger.warning(f"{level_0} items have level 0 in {tree_file.name}")

        # Check if source classification codes are in the associated tree file
        suffix = "_from" if "_bonsai.csv" in conc_file.name else "_to"
        col = directory.name + suffix
        missing_codes = set(df_conc[col]) - set(df_tree["code"])
        if missing_codes:
            logger.warning(f"Codes missing in {tree_file.name}: {missing_codes}")

        # Check if there are any 'many-to-many' entries (doesn't make the test fail)
        many_to_many = df_conc[df_conc.comment == "many-to-many correspondence"]
        if not many_to_many.empty:
            logger.warning(
                f"Many-to-many correspondences found in {conc_file.name}:\n"
                f"{many_to_many.iloc[:10, :2]}"
            )

    assert test_pass, "One or more file checks failed. See the warning messages."


@pytest.mark.parametrize("directory", [flow_path], ids=["flow"])
def test_concpair(directory):
    # Check conc files
    conc_files = list(directory.glob("concpair_*_bonsai.csv")) + list(
        directory.glob("concpair_bonsai_*.csv")
    )
    for conc_file in conc_files:
        df_conc = assert_columns(
            conc_file,
            [
                "activitytype_from",
                "flowobject_from",
                "activitytype_to",
                "flowobject_to",
                "classification_from",
                "classification_to",
                "comment",
            ],
        )

        # Search the associated tree file
        tree_filename = conc_file.name.replace("concpair_", "tree_").replace(
            "_bonsai", ""
        )
        tree_file_act = directory / "activitytype" / tree_filename
        tree_file_act_bonsai = directory / "activitytype" / "tree_bonsai.csv"

        tree_file_flowobj = directory / "flowobject" / tree_filename
        tree_file_flobobj_bonsai = directory / "flowobject" / "tree_bonsai.csv"

        # Check the columns and levels of the tree file
        df_tree_act = assert_columns(tree_file_act, ["code", "name"])
        df_tree_flowobj = assert_columns(tree_file_flowobj, ["code", "name"])

        df_tree_flowobj_bonsai = assert_columns(
            tree_file_flobobj_bonsai, ["code", "name"]
        )
        df_tree_act_bonsai = assert_columns(tree_file_act_bonsai, ["code", "name"])

        # Check if source classification codes are in the associated tree file
        suffix = "_from" if "_bonsai.csv" in conc_file.name else "_to"
        col = "activitytype" + suffix
        missing_codes = set(df_conc[col]) - set(df_tree_act["code"])
        missing_codes = {code for code in missing_codes if pd.notna(code)}
        if missing_codes:
            logger.warning(
                f"Codes missing in activitytype/{tree_file_act.name}: {missing_codes}"
            )

        suffix = "_to" if "_bonsai.csv" in conc_file.name else "_from"
        col = "activitytype" + suffix
        missing_codes = set(df_conc[col]) - set(df_tree_act_bonsai["code"])
        missing_codes = {code for code in missing_codes if pd.notna(code)}
        if missing_codes:
            logger.warning(
                f"Codes missing in activitytype/{tree_file_act_bonsai.name}: {missing_codes}"
            )

        # Check if source classification codes are in the associated tree file
        suffix = "_from" if "_bonsai.csv" in conc_file.name else "_to"
        col = "flowobject" + suffix
        missing_codes = set(df_conc[col]) - set(df_tree_flowobj["code"])
        missing_codes = {code for code in missing_codes if pd.notna(code)}
        if missing_codes:
            logger.warning(
                f"Codes missing in flowobject/{tree_file_flowobj.name}: {missing_codes}"
            )

        # Check if source classification codes are in the associated tree file
        suffix = "_to" if "_bonsai.csv" in conc_file.name else "_from"
        col = "flowobject" + suffix
        missing_codes = set(df_conc[col]) - set(df_tree_flowobj_bonsai["code"])
        missing_codes = {code for code in missing_codes if pd.notna(code)}
        if missing_codes:
            logger.warning(
                f"Codes missing in flowobject/{tree_file_flobobj_bonsai.name}: {missing_codes}"
            )


def test_bonsai_products_to_markets_codes_exist():
    bonsai_products_to_markets_df = pd.read_csv(
        flow_path / "bonsai_sut_products_to_markets.csv"
    )

    activitytype_df = pd.read_csv(activitytype_path / "tree_bonsai.csv")
    flowobject_df = pd.read_csv(flowobject_path / "tree_bonsai.csv")
    # Extract unique values
    flowobject_values = set(bonsai_products_to_markets_df["flowobject"])
    activitytype_values = set(bonsai_products_to_markets_df["activitytype"])

    # Extract unique values from flowobject and activitytype CSVs (code + alias_code)
    flowobject_codes = set(flowobject_df["code"].dropna()) | set(
        flowobject_df["alias_code"].dropna()
    )
    activitytype_codes = set(activitytype_df["code"].dropna()) | set(
        activitytype_df["alias_code"].dropna()
    )

    # Assertions
    missing_flowobjects = flowobject_values - flowobject_codes
    missing_activitytypes = activitytype_values - activitytype_codes
    if missing_flowobjects:
        logger.warning(f"Missing flowobjects {missing_flowobjects}")
    if missing_activitytypes:
        logger.warning(f"Missing activitytypes {missing_activitytypes}")

    assert not missing_flowobjects, f"Missing flowobject codes: {missing_flowobjects}"
    assert (
        not missing_activitytypes
    ), f"Missing activitytype codes: {missing_activitytypes}"
