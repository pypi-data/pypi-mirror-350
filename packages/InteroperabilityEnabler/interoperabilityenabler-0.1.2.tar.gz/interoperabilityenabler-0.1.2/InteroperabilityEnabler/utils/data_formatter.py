"""
Data Formatter:
To convert the data expressed in various format (CSV, XLS, XLSX and NGSI-LD)
into the SEDIMARK internal format, i.e., pandas DataFrame.
NGSI-LD was selected as the primary format.

Author: Shahin ABDOUL SOUKOUR - Inria
Maintainer: Shahin ABDOUL SOUKOUR - Inria
"""

import json
import pandas as pd


def data_to_dataframe(data):
    """
    Convert data from file path or raw JSON/JSON-LD into a flattened pandas DataFrame.

    Args:
        data (str | dict | list): Path to a data file or a JSON/JSON-LD object.

    Returns:
        pd.DataFrame: Flattened data as a DataFrame.
    """
    df = None
    try:
        if isinstance(data, str):
            # Handle file path
            if data.endswith(".xls") or data.endswith(".xlsx"):
                df = pd.read_excel(data)
            elif data.endswith(".csv"):
                df = pd.read_csv(data)
            elif data.endswith(".json") or data.endswith(".jsonld"):
                with open(data, "r", encoding="utf-8") as file:
                    json_data = json.load(file)
                    entities = json_data if isinstance(json_data, list) else json_data.get("@graph", [json_data])
                    df = pd.DataFrame([flatten_dict(e) for e in entities])
                    df.reset_index(drop=True, inplace=True)
            else:
                raise ValueError("Unsupported file format. Must be .xls, .xlsx, .csv, .json, or .jsonld")
        elif isinstance(data, (dict, list)):
            # Handle raw JSON or JSON-LD object directly
            entities = data if isinstance(data, list) else data.get("@graph", [data])
            df = pd.DataFrame([flatten_dict(e) for e in entities])
            df.reset_index(drop=True, inplace=True)
        else:
            raise ValueError("Unsupported input type. Must be file path or JSON object.")
    except Exception as e:
        print(f"Error processing data: {e}")
    return df


def flatten_dict(d, parent_key="", sep=".", preserve_keys=None):
    """
    Recursively flattens a nested dictionary into a flat dictionary.

    Args:
        d (dict): The dictionary to flatten.
        parent_key (str): Prefix for keys during recursion.
        sep (str): Separator used for key hierarchy.
        preserve_keys (list): Keys whose values should not be flattened.

    Returns:
        dict: A flattened dictionary.
    """
    if preserve_keys is None:
        preserve_keys = ["coordinates", "@context"]

    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k

        if isinstance(v, dict):
            if k in preserve_keys:
                items.append((new_key, v))
            else:
                items.extend(flatten_dict(v, new_key, sep=sep, preserve_keys=preserve_keys).items())

        elif isinstance(v, list):
            if k in preserve_keys:
                items.append((new_key, v))
            else:
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(flatten_dict(item, f"{new_key}[{i}]", sep=sep, preserve_keys=preserve_keys).items())
                    else:
                        items.append((f"{new_key}[{i}]", item))

        else:
            items.append((new_key, v))

    return dict(items)
