## What is it?

Interoperability Enabler (IE) component is designed to facilitate seamless integration and interaction among various artefacts within the SEDIMARK ecosystem, including data, AI models, and service offerings.


## Key Feature

- Data Formatter - Convert data from various formats into the SEDIMARK internal processing format (pandas DataFrames)
- Data Quality Annotations - Enable adding any kind of quality annotations to data inside pandas DataFrames
- Data Mapper – Convert data from pandas DataFrames into NGSI-LD json
- Data Extractor – Extract relevant data from a pandas DataFrame
- Metadata Restorer – Restore metadata to a pandas DataFrame
- Data Merger – Merge two DataFrames by matching column names

## Installation

The source code can be found on GitHub at https://github.com/Sedimark/InteroperabilityEnabler.

To install the package, you can use pip:

```bash
pip install InteroperabilityEnabler
```

## Quick Start Examples

#### Data Formatter (to convert the input data into a pandas DataFrame)

```python
from InteroperabilityEnabler.utils.data_formatter import data_to_dataframe

FILE_PATH="sample.jsonld"
df = data_to_dataframe(FILE_PATH)
```

It recursively flattens dictionaries while preserving key hierarchies, supporting nested structures and ensuring efficient processing and interoperability.


#### Data Quality Annotations (to enrich pandas DataFrames by adding quality annotations)

Instance-level annotations:
```python
from InteroperabilityEnabler.utils.annotation_dataset import add_quality_annotations_to_df

entity_type_annotation = "entity_type_value" # entity type for quality annotations
annotated_df = add_quality_annotations_to_df(
    df,
    entity_type = entity_type_annotation,
    assessed_attrs = None,
    # type = "new_type", # If there is no type in the input file, a new one can be created
    # context_value = [link1, link2] # If there is no @context in the input file, a new one can be created
)
```

Attribut-level annotation:
```python
from InteroperabilityEnabler.utils.annotation_dataset import add_quality_annotations_to_df

entity_type_annotation = "entity_type_value" # entity type for quality annotations
assessed_attrs = ["attribut_name"]  # Base attribute name (metadata)
annotated_df = add_quality_annotations_to_df(
     df, entity_type = entity_type_annotation, assessed_attrs = assessed_attrs
)
```

Granular-level annotation:
```python
from InteroperabilityEnabler.utils.annotation_dataset import add_quality_annotations_to_df

entity_type_annotation = "entity_type_value" # entity type for quality annotations
assessed_attrs = ["currentTripCount[0]"]  # Base attribute name (metadata) - with the indice
annotated_df = add_quality_annotations_to_df(
   df, entity_type = entity_type_annotation, assessed_attrs = assessed_attrs
)
```

#### Data Mapper (to convert the DataFrame into NGSI-LD json format)

```python
from InteroperabilityEnabler.utils.data_mapper import data_conversion, restore_ngsi_ld_structure

data = data_conversion(annotated_df)
data_restored = restore_ngsi_ld_structure(data) # to restore the original NGSI-LD structure
```

#### Data Extractor (to extract and return specific columns from a pandas DataFrame)

```python
from InteroperabilityEnabler.utils.extract_data import extract_columns

# Select columns by index
column_indices = [5, 7]

selected_df, selected_column_names = extract_columns(df, column_indices)

print("\nSelected DataFrame:")
print(selected_df)

print("\nSelected Column Names:")
print(selected_column_names)

```

#### Metadata Restorer (to restore column names into a pandas DataFrame)

```python
import pandas as pd
from InteroperabilityEnabler.utils.add_metadata import add_metadata_to_predictions_from_dataframe

PREDICTED_DATA = "predicted_data.csv" # example - prediction results from an AI model
predicted_df = pd.read_csv(PREDICTED_DATA, header=None)
predicted_df = add_metadata_to_predictions_from_dataframe(
    predicted_df, selected_column_names
)
```

#### Data Merger (merge two DataFrames)

```python
from InteroperabilityEnabler.utils.merge_data import merge_predicted_data

# To combine the original input data with the corresponding prediction results from an AI model
merged_df = merge_predicted_data(df, predicted_df)
```

## Acknowledgement

This software has been developed by the [Inria](https://www.inria.fr/fr) under the [SEDIMARK(SEcure Decentralised Intelligent Data MARKetplace)](https://sedimark.eu/) project. 
SEDIMARK is funded by the European Union under the Horizon Europe framework programme [grant no. 101070074]. 
