import os
from logging import getLogger
from pathlib import Path

import pandas
from anytree import Node, RenderTree

from ._mapping_type import get_comment, skos_uri_dict

logger = getLogger("root")

ROOT_PATH = Path(os.path.dirname(__file__))

activitytype_path = "data/flow/activitytype/"
location_path = "data/location/"
dataquality_path = "data/dataquality/"
uncertainty_path = "data/uncertainty/"
time_path = "data/time/"
flowobject_path = "data/flow/flowobject/"
flow_path = "data/flow/"
currency_path = "data/currency/"

# Lookup function for pandas DataFrame
def lookup(self, keyword):
    """Filter the DataFrame based on the keyword in the "name" column"""
    filtered_df = self[self["name"].str.contains(keyword, case=False)]
    return filtered_df


def get_children(
    self,
    parent_codes,
    deep=True,
    return_parent=False,
    exclude_sut_children=False,
    only_sut_children=False,
):
    """
    Get descendants (direct and indirect) for a list of parent_codes.

    Parameters
    ----------
    parent_codes: str or list
        A single parent_code or a list of parent_codes for which descendants are to be fetched.
    deep: bool, optional
        If True, fetch all descendants recursively. If False, fetch only direct children. Default is True.
    return_parent: bool, optional
        If True, include the parent codes in the returned DataFrame. Default is False.
    exclude_sut_children: bool, optional
        If True, exclude children in the final Bonsai SUTs. Default is False.
    only_sut_children: bool, optional
        If True, only include children that are in the final Bonsai SUTs. Default is False.

    Returns
    -------
    pandas.DataFrame
        A DataFrame containing rows with descendants of the specified parent_codes.
    """
    if not isinstance(self, pandas.DataFrame):
        raise TypeError("The object must be a pandas DataFrame.")

    if not {"code", "parent_code"}.issubset(self.columns):
        raise KeyError("DataFrame must contain 'code' and 'parent_code' columns.")

    if isinstance(parent_codes, str):
        parent_codes = [parent_codes]
    elif not isinstance(parent_codes, (list, set, tuple)):
        raise TypeError("parent_codes must be a string or a list-like object.")

    parent_codes = set(parent_codes)

    # Handle exclusion of SUT children
    bonsai_codes = set()
    if "in_final_sut" in self.columns:
        if exclude_sut_children:
            bonsai_codes = set(self.loc[self["in_final_sut"] == "True", "code"])
        sut_codes = (
            set(self.loc[self["in_final_sut"] == "True", "code"])
            if only_sut_children
            else None
        )

    if deep:
        to_explore = set(parent_codes)
        all_descendants = set()

        while to_explore:
            current_children = self[self["parent_code"].isin(to_explore)]
            new_descendants = set(current_children["code"]) - all_descendants

            if exclude_sut_children:
                new_descendants -= bonsai_codes

            if not new_descendants:
                break  # Exit loop if no new children found

            all_descendants.update(new_descendants)
            to_explore = new_descendants  # Continue exploring new children

        if not all_descendants:
            logger.debug(f"No children found for {parent_codes}")

        df = self[self["code"].isin(all_descendants)]
    else:
        df = self[self["parent_code"].isin(parent_codes)]
        if df.empty:
            df = self[self["code"].isin(parent_codes)]

    # Apply SUT filter only at the end
    if only_sut_children:
        print(f"leng sut codes is‚  {len(sut_codes)}")
        df = df[df["code"].isin(sut_codes)]

    # Include parent codes if requested
    if return_parent:
        df = pandas.concat(
            [self[self["code"].isin(parent_codes)], df]
        ).drop_duplicates()

    return CustomDataFrame(df)


def create_conc(df_A, df_B, source="", target=""):
    """Create new concordance based on two other tables.

    Argument
    --------
    df_A : pandas.DataFrame
        concordance table A
        with mapping from "x" to "y"
    df_B : pandas.DataFrame
        concordance table B
        with mapping from "y" to "z"
    target : str
        classification name that specifies "x"
    source : str
        classification name that specifies "z"

    Returns
    -------
    pandas.DataFrame
        concordance table with mapping form "x" to "z"
    """
    if "activitytype_to" in df_B.columns and "flowobjet_to" in df_B.columns:
        raise NotImplementedError("Concpair tables not allowed")
    elif "activitytype_to" in df_A.columns and "activitytype_to" in df_B.columns:
        column_prefix = "activitytype"
    elif "flowobject_to" in df_A.columns and "flowobject_to" in df_B.columns:
        column_prefix = "flowobject"

    merged = pandas.merge(df_A, df_B, on=f"{column_prefix}_to", suffixes=("_A", "_B"))

    # Create the resulting DataFrame with required columns
    result = pandas.DataFrame(
        {
            f"{column_prefix}_from": merged[f"{column_prefix}_from_A"],
            f"{column_prefix}_to": merged[f"{column_prefix}_from_B"],
            "classification_from": source,  # Fixed value from A
            "classification_to": target,  # Fixed value for result
        }
    )

    # Drop duplicate pairs of source and target
    new_mapping = result.drop_duplicates(
        subset=[
            f"{column_prefix}_from",
            f"{column_prefix}_to",
            "classification_from",
            "classification_to",
        ]
    )

    # Calculate the counts of each source and target in the merged DataFrame
    source_counts = new_mapping[f"{column_prefix}_from"].value_counts().to_dict()
    target_counts = new_mapping[f"{column_prefix}_to"].value_counts().to_dict()
    # Apply the get_comment function to each row
    new_mapping["comment"] = new_mapping.apply(
        lambda row: get_comment(
            source_counts[row[f"{column_prefix}_from"]],
            target_counts[row[f"{column_prefix}_to"]],
            s=row[f"{column_prefix}_from"],
            t=row[f"{column_prefix}_to"],
        ),
        axis=1,
    )
    new_mapping["skos_uri"] = new_mapping["comment"].map(skos_uri_dict)

    new_mapping = new_mapping[
        [
            f"{column_prefix}_from",
            f"{column_prefix}_to",
            "classification_from",
            "classification_to",
            "comment",
            "skos_uri",
        ]
    ]
    new_mapping = new_mapping.reset_index(drop=True)
    return new_mapping


def _get_concordance_file(file_path):
    try:
        # Read the concordance CSV into a DataFrame
        return pandas.read_csv(file_path, dtype=str)
        # return multiple_dfs
    except FileNotFoundError:
        return None
    except Exception as e:
        logger.error(f"Error reading concordance file: {e}")
        return None


def get_concordance(from_classification, to_classification):
    """
    Get the concordance DataFrame based on the specified classifications.
    Parameters
    ----------
    from_classification: str
        The source classification name (e.g., "bonsai").
    to_classification: str
        The target classification name (e.g., "nace_rev2").
    Returns
    -------
    pd.DataFrame
        The concordance DataFrame if 1 file is found; otherwise, a dict of DataFrames.
    """
    # Construct the file name
    fitting_file_names = [
        f"conc_{from_classification}_{to_classification}.csv",
        f"concpair_{from_classification}_{to_classification}.csv",
    ]
    reversed_file_names = [
        f"conc_{to_classification}_{from_classification}.csv",
        f"concpair_{to_classification}_{from_classification}.csv",
    ]
    file_paths = [
        activitytype_path,
        location_path,
        dataquality_path,
        uncertainty_path,
        time_path,
        flowobject_path,
        flow_path,
    ]
    multiple_dfs = {}
    for f in file_paths:
        for n in fitting_file_names:
            file_path = ROOT_PATH.joinpath(f, n)
            df = _get_concordance_file(file_path)
            if not df is None:
                multiple_dfs[f"{f}"] = df
        for n in reversed_file_names:
            file_path = ROOT_PATH.joinpath(f, n)
            df = _get_concordance_file(file_path)
            if not df is None:
                # Renaming columns
                new_columns = {}
                for col in df.columns:
                    if "_from" in col:
                        new_columns[col] = col.replace("_from", "_to")
                    elif "_to" in col:
                        new_columns[col] = col.replace("_to", "_from")
                df.rename(columns=new_columns, inplace=True)

                # Changing the comment column
                df["comment"] = df["comment"].replace(
                    {
                        "one-to-many correspondence": "many-to-one correspondence",
                        "many-to-one correspondence": "one-to-many correspondence",
                    }
                )
                df["skos_uri"] = df["skos_uri"].replace(
                    {
                        "http://www.w3.org/2004/02/skos/core#narrowMatch": "http://www.w3.org/2004/02/skos/core#broadMatch",
                        "http://www.w3.org/2004/02/skos/core#broadMatch": "http://www.w3.org/2004/02/skos/core#narrowMatch",
                    }
                )
                multiple_dfs[f"{f}"] = df

    if len(multiple_dfs) == 1:
        return multiple_dfs[next(iter(multiple_dfs))]
    elif len(multiple_dfs) > 1:
        return multiple_dfs
    else:
        raise FileNotFoundError(
            f"No concordance for '{from_classification}' and '{to_classification}' found."
        )


def get_tree(for_classification, ctype):
    """
    Get the tree table as DataFrame for a classification
    Parameters
    ----------
    for_classification: str
        Name of the requested classification (e.g., "nace_rev2").
    Returns
    -------
    pd.DataFrame
        The tree as DataFrame
    """
    # Search all file_paths
    if ctype in ["activitytype", "flowobject"]:
        ctype = f"flow/{ctype}"
    file_path = ROOT_PATH.joinpath("data", ctype, f"tree_{for_classification}.csv")
    return _get_concordance_file(file_path)


def print_tree(self, toplevelcode):
    """Print the tree structure for a given code.

    Bold text represent sub-categories which are included when applying it in the Bonsai SUT.
    Italic text represent sub-categories which are not included, since these are separate codes in the Bonsai SUT.

    """
    all_codes = self.get_children(
        toplevelcode, deep=True, return_parent=True, exclude_sut_children=False
    )
    sut_codes = self.get_children(
        toplevelcode, deep=True, return_parent=True, exclude_sut_children=True
    )
    # Create nodes from the data
    nodes = {}
    for _, row in all_codes.iterrows():
        nodes[row["code"]] = Node(
            row["code"], parent=nodes.get(row["parent_code"]), descript=row["name"]
        )

    italic_codes = set(sut_codes["code"])  # Set of codes to make italic
    for pre, fill, node in RenderTree(nodes[toplevelcode]):
        if node.name in italic_codes:
            print(f"{pre}\033[1m{node.name} - {node.descript}\033[0m")  # Italicize text
        else:
            print(f"{pre}\033[3m{node.name} - {node.descript}\033[0m")


# def nearest_sut_code(self, code):
#    """Return the nearest code that is in the SUTs.
#
#    Only ancestors and exact matches are considerred.
#
#    :param self: Pandas DataFrame containing the data
#    :param code: The code to check
#    :return tuple: code, alias code
#    """
#    visited_codes = set()
#
#    while True:
#        if code in visited_codes:
#            return None  # Return empty DataFrame if cycle is detected
#
#        visited_codes.add(code)
#        row = self[self["code"] == code]
#
#        if row.empty:
#            return None  # Return empty DataFrame if code is not found
#
#        name = row["name"].values[0]
#
#        # Recursive function to check all descendants (children, grandchildren, etc.)
#        def has_valid_descendant(current_code):
#            descendants = self[self["parent_code"] == current_code]
#            for _, descendant in descendants.iterrows():
#                if descendant["name"] == name and descendant["in_final_sut"]:
#                    return True  # Found a valid descendant
#                if has_valid_descendant(descendant["code"]):  # Recursively check deeper
#                    return True
#            return False
#
#        # Check for any descendant with the same name and in_final_sut == True
#        if has_valid_descendant(code):
#            return code  # Found a match, keep the original code
#
#        if row["in_final_sut"].values[0] == "True":
#            return (
#                row["code"].values[0],
#                row["alias_code"].values[0],
#            )  # Return row if in_final_sut is True
#
#        parent_code = row["parent_code"].values[0]
#        if pandas.isna(parent_code) or parent_code == "":
#            return None
#
#        code = parent_code


def nearest_sut_code(self, code):
    """Return the nearest code that is in the SUTs.

    Searches for any descendant (child, grandchild, etc.) with the same name
    and in_final_sut == True. If not found, moves up to ancestors.

    :param self: Pandas DataFrame containing the data
    :param code: The code to check
    :return tuple: (code, alias_code) or None if no match is found
    """
    visited_codes = set()

    def find_valid_descendant(current_code, name):
        """Recursively searches for a descendant with the same name and in_final_sut == True."""
        descendants = self[self["parent_code"] == current_code]
        for _, descendant in descendants.iterrows():
            if descendant["name"] == name and bool(descendant["in_final_sut"]):
                return descendant["code"], descendant["alias_code"]
            result = find_valid_descendant(
                descendant["code"], name
            )  # Recursively check deeper
            if result:
                return result
        return None

    while True:
        if code in visited_codes:
            return None  # Avoid infinite loops in case of cycles

        visited_codes.add(code)
        row = self[self["code"] == code]

        if row.empty:
            return None  # Return None if code is not found

        name = row["name"].values[0]

        # 🔍 **Check for any descendant at any depth**
        descendant_result = find_valid_descendant(code, name)
        if descendant_result:
            return descendant_result  # ✅ Found a valid descendant

        # ✅ **If current row is in SUT, return it**
        if bool(row["in_final_sut"].values[0]):
            return row["code"].values[0], row["alias_code"].values[0]

        # 🔼 **Move to the parent**
        parent_code = row["parent_code"].values[0]
        if pandas.isna(parent_code) or parent_code == "":
            return None  # Stop if no valid parent exists

        code = parent_code  # Continue searching in the parent


# Subclass pandas DataFrame
class CustomDataFrame(pandas.DataFrame):
    lookup = lookup
    get_children = get_children
    print_tree = print_tree
    nearest_sut_code = nearest_sut_code
