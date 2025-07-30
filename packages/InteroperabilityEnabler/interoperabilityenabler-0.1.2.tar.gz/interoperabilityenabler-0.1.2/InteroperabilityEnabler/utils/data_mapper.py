"""
Data Mapper:
To convert the data from the internal formatting (pandas DataFrame) to the NGSI-LD format,
which is the standard adopted within SEDIMARK.

Author: Shahin ABDOUL SOUKOUR - Inria
Maintainer: Shahin ABDOUL SOUKOUR - Inria
"""

from collections import OrderedDict
from datetime import datetime


def data_conversion(df, entity_type=None, context_value=None):
    """
    Convert a DataFrame into NGSI-LD format.

    Args:
        df (DataFrame): The input DataFrame (from CSV, XLS/XLSX or flattened NGSI-LD JSON).
        entity_type (str): The default entity type to use for CSV data.
        context_value (str or list, optional): The default @context value to use if missing or null.

    Returns:
        A NGSI-LD data.
    """
    timestamp_columns = [
        "UnixTime.value",
        "UnixTime",
        "observedAt",
        "createdAt",
        "modifiedAt",
        "deletedAt",
        "start",
        "end",
        "startAt",
        "endAt",
        "dateObserved.value",
        "dateObserved",
        "dateCreated",
        "dateModified",
        "endTimeAt",
        "expriresAt",
        "lastFailure",
        "lastNotification",
        "lastSuccess",
        "notifiedAt",
        "timeAt",
        "testedAt",
    ]

    ngsi_ld_entities = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Handle 'id'
        entity_id = row.get("id")
        if not entity_id or str(entity_id).lower() == "null":
            entity_id = f"urn:ngsi-ld:{entity_type}:{index}"

        # Handle 'type'
        entity_type_value = row.get("type")
        if not entity_type_value or str(entity_type_value).lower() == "null":
            entity_type_value = entity_type

        # Initialize the entity
        entity = OrderedDict()
        entity["id"] = entity_id
        entity["type"] = entity_type_value

        # Handle '@context'
        existing_context = row.get("@context")
        if existing_context and str(existing_context).lower() != "null":
            context_to_add = existing_context  # Preserve the existing @context
        elif context_value is not None:
            context_to_add = (
                context_value if isinstance(context_value, list) else context_value
            )
        else:
            context_to_add = None  # No context specified

        # Process each column
        for column in df.columns:
            # Skip 'id', 'type', and '@context' since they're already handled
            if column in ["id", "type", "@context"]:
                continue

            value = row[column]

            # Check if the column is one of the timestamp columns
            if column in timestamp_columns and isinstance(value, (int, float)):
                try:
                    # Convert timestamp to datetime format
                    value = datetime.utcfromtimestamp(float(value)).strftime(
                        "%Y-%m-%dT%H:%M:%SZ"
                    )
                except (ValueError, TypeError):
                    pass  # If conversion fails, keep the original value

            if "." in column:
                # Handle nested attributes (assume NGSI-LD JSON format)
                parts = column.split(".")
                if parts[0] not in entity:
                    entity[parts[0]] = {}
                current_level = entity[parts[0]]
                for part in parts[1:-1]:
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]
                current_level[parts[-1]] = value
            else:
                # Treat as Property for CSV-originating data
                entity[column] = {
                    "type": "Property",  ### <--
                    "value": value,
                }

        # Check for "type": "null" and replace with "type": "Property"
        for key, attribute in entity.items():
            if isinstance(attribute, dict) and attribute.get("type") == "null":
                attribute["type"] = "Property"

        # Add @context at the end if it exists
        if context_to_add is not None:
            entity["@context"] = context_to_add

        # Append the constructed entity
        ngsi_ld_entities.append(entity)

    return ngsi_ld_entities


def restore_ngsi_ld_structure(ngsi_ld_data):
    """
    Restore the NGSI-LD structure.

    Args:
        data: The NGSI-LD data to be processed. It can be a dictionary or a list of dictionaries.

    Returns:
        A NGSI-LD data restored.
    """
    # Handling list recursively
    # Ensure that nested lists (if any) are processed correctly
    if isinstance(
        ngsi_ld_data, list
    ):  # If data is a list, we recursively process each item in the list
        return [restore_ngsi_ld_structure(item) for item in ngsi_ld_data]

    restored_data = {}
    for key, value in ngsi_ld_data.items():
        if "[" in key:  # If a key contains [number] (e.g., "availableBikeNumber[0]")
            base_key = key.split("[")[
                0
            ]  # Extract base_key (e.g., "availableBikeNumber")
            restored_data.setdefault(base_key, []).append(
                value
            )  # To initialize a list if it does not exist and append the value to the list
        else:
            # If value is another dictionary, recursively process it
            # Otherwise, store the value as is
            restored_data[key] = (
                restore_ngsi_ld_structure(value) if isinstance(value, dict) else value
            )
    return restored_data
