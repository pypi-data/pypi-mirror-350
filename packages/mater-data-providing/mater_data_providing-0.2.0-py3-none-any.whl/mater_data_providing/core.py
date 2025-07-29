"""
This module defines the functions to help ang check the providing of data for the mater data framework.

Copyright (C) 2025 @verzierf <francois.verzier@univ-grenoble-alpes.fr>

SPDX-License-Identifier: LGPL-3.0-or-later
"""

import json
import logging
import os
from typing import Dict, Literal

import numpy as np
import pandas as pd


def metadata_definition(link: str, source: str, project: str) -> Dict[str, str]:
    """Returns a dictionary with all the keys necessary for the mater database metadata table schema.

    :param link: Link to find the raw dataset
    :type link: str
    :param source: Source name
    :type source: str
    :param project: Name of the project you are working on
    :type project: str
    :return: One metadata table entry
    :rtype: Dict[str, str]
    """
    return {"link": link, "source": source, "project": project}


def provider_definition(
    first_name: str, last_name: str, email_address: str
) -> Dict[str, str]:
    """Returns a dictionary with all the keys necessary for the mater database provider table schema.

    :param first_name: Your first name
    :type first_name: str
    :param last_name: Your last name
    :type last_name: str
    :param email_address: Your email address
    :type email_address: str
    :return: One provider table entry
    :rtype: Dict[str, str]
    """
    return {
        "first_name": first_name,
        "last_name": last_name,
        "email_address": email_address,
    }


def dump_json(
    input_data: pd.DataFrame, provider: Dict[str, str], metadata: Dict[str, str]
) -> json.dumps:
    """_summary_

    :param input_data: A dataframe with the right columns
    :type input_data: pd.DataFrame
    :param provider: The provider dictionnary from provider_definition()
    :type provider: Dict[str, str]
    :param metadata: The metadata dictionnary from metadata_definition()
    :type metadata: Dict[str, str]
    :return: A serialized json
    :rtype: json.dumps
    """
    data = {
        "input_data": input_data.to_dict(orient="records"),
        "provider": provider,
        "metadata": metadata,
    }
    return json.dumps(data, indent=2)


def to_json(
    j: json,
    name: str,
    mode: Literal["w", "a"] = "w",
):
    """Maps the dimension elements from the input json from a dimension.json file and writes the resulting json into a specific directory structure.

    This structure is the one used by the mater library to run a simulation from local json data.

    :param j: Dumped json to map with the right dimension names and write as a .json file
    :type j: json
    :param name: The name of the json file
    :type name: str
    :param mode: pd.DataFrame.to_json mode argument, defaults to "w"
    :type mode: Literal[&quot;w&quot;, &quot;a&quot;], optional
    """
    # Define the directory path
    data_path = os.path.join("data")

    # Check if the directory exists, if not, create it
    if not os.path.exists(data_path):
        os.makedirs(data_path)
        logging.info(f"Directory {data_path} created.")

    # Define the directory path
    dir_path = os.path.join("data", "input_data")

    # Check if the directory exists, if not, create it
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        logging.info(f"Directory {dir_path} created.")

    # get input_data json as dataframe
    df = pd.DataFrame(json.loads(j)["input_data"])
    # replace equivalents from dimension.json
    df_replaced = replace_equivalence(df)
    # set dimension columns as one dictionnary column
    df_transformed = _dimension_as_json(df_replaced)
    # write the json file
    #### ToDo: find a way to automatically set name to the python script name importing this function
    df_transformed.to_json(
        os.path.join(dir_path, name + ".json"), orient="records", indent=2, mode=mode
    )


def replace_equivalence(df: pd.DataFrame) -> pd.DataFrame:
    """Replaces the dimension elements of a dataframe according to the data\dimension\dimension.json file.

    :param df: Initial dataframe
    :type df: pd.DataFrame
    :return: Uniformed dataframe
    :rtype: pd.DataFrame
    """
    dimension = pd.read_json(
        os.path.join("data", "dimension", "dimension.json"), orient="records"
    )
    try:
        # Ensure multiple keys in 'equivalence' dictionaries are handled correctly
        df_filtered = dimension.dropna(
            subset=["equivalence"]
        )  # Keep rows with non-null equivalence

        # Expand 'equivalence' dictionary into separate columns
        df_exploded = (
            df_filtered["equivalence"]
            .apply(pd.Series)
            .stack()
            .reset_index(level=1, drop=True)
        )

        # Map each source equivalence key to its corresponding vehicle name
        equivalence_dict = (
            df_exploded.to_frame()
            .join(df_filtered["value"])
            .set_index(0)["value"]
            .to_dict()
        )
        df.replace(equivalence_dict, inplace=True)
    except KeyError:
        pass
    return df


# internal functions


def _dimension_as_json(df: pd.DataFrame):
    df2 = df.copy()
    dimensions = np.setdiff1d(
        list(df2.columns), ["variable", "date", "value", "time", "unit", "scenario"]
    )
    df2["dimensions_values"] = df.apply(
        lambda row: {dim: row[dim] for dim in dimensions}, axis=1
    )
    return df2.drop(dimensions, axis=1)
