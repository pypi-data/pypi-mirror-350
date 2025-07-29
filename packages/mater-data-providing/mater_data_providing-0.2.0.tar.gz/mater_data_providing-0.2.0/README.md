# MATER data providing

A library to help providing the right json files to feed the mater database.

It can be used to create a local json database to run mater simulations locally.

[TOC]

## 📋 Requirements

- Python 3.12 or higher

We recommend using one virtual environment per Python project to manage dependencies and maintain isolation. You can use a package manager like [uv](https://docs.astral.sh/uv/) to help you with library dependencies and virtual environments.

## 📦 Install the mater-data-providing Package

Install the `mater` package via uv:

```bash
uv add mater-data-providing
```

Install the `mater` package via pip:

```bash
pip install mater-data-providing
```

## ⚙️ API

### metadata_definition

```python
import mater-data-providing as mdp
metadata = mdp.metadata_definition("source_link", "my_source", "my_project")
print(metadata)
```

```bash
{"link": "source_link", "source": "my_source", "project": "my_project"}
```

### provider_definition

```python
import mater-data-providing as mdp
provider = mdp.provider_definition("Jon", "Do", "jon.do@mail.com")
print(provider)
```

```bash
{"first_name": "Jon", "last_name": "Do", "email_address": "jon.do@mail.com"}
```

### dump_json

This function is used at the end of your providing script to dump into a serialized json the input dataframe, the provider dictionnary and the metadata dictionnary.

```python
import mater_data_providing as mdp
import pandas as pd

# 1. Build a DataFrame
df = pd.DataFrame([
    {"location": "france", "object": "car", "value": 15, "unit": "year", "time": 2015, "scenario": "historical", "variable": "lifetime_mean_value"},
    {"location": "france", "object": "car", "value": 17, "unit": "year", "time": 2020, "scenario": "historical", "variable": "lifetime_mean_value"},
])

# 2. Create a provider and metadata dictionnary
provider = mdp.provider_definition("Jon", "Do", "jon.do@mail.com")
metadata = mdp.metadata_definition("source_link", "my_source", "my_project")

# 3. Dump the data into a serialized json
j = mdp.dump_json(input_data, provider, metadata)
print(j)
```

```bash
{
  "input_data": [
    {
      "location": "france",
      "object": "car",
      "value": 15,
      "unit": "year",
      "time": 2015,
      "scenario": "historical",
      "variable": "lifetime_mean_value"
    },
    {
      "location": "france",
      "object": "car",
      "value": 17,
      "unit": "year",
      "time": 2020,
      "scenario": "historical",
      "variable": "lifetime_mean_value"
    }
  ],
  "provider": {
    "first_name": "Jon",
    "last_name": "Do",
    "email_address": "jon.do@mail.com"
  },
  "metadata": {
    "link": "source_link",
    "source": "my_source",
    "project": "my_project"
  }
}
```

### replace_equivalence

data\dimension\dimension.json:

```json
[
  {
    "value": "car",
    "equivalence": {
      "short": "PLDV",
      "long": "personal_vehicle"
    }
  },
  {
    "value": "france",
    "equivalence": {
      "ISO3": "FRA"
    }
  }
]
```

Python scrip at the root of the project:

```python
import mater_data_providing as mdp
import pandas as pd

# 1. Build a DataFrame
df = pd.DataFrame([
    {"location": "FRA", "object": "personal_vehicle", "value": 15, "unit": "year", "time": 2015, "scenario": "historical", "variable": "lifetime_mean_value"},
    {"location": "france", "object": "PLDV", "value": 17, "unit": "year", "time": 2020, "scenario": "historical", "variable": "lifetime_mean_value"},
])

df_uniform = mdp.replace_equivalence(df)
print(df_uniform)
```

```bash
  location object  value  unit  time    scenario             variable
0   france    car     15  year  2015  historical  lifetime_mean_value
1   france    car     17  year  2020  historical  lifetime_mean_value
```

### to_json

replace the equivalences into the serialized json returned from mdp.dump_json funciton and write into a specific directory.

data\dimension\dimension.json:

```json
[
  {
    "value": "car",
    "equivalence": {
      "short": "PLDV",
      "long": "personal_vehicle"
    }
  },
  {
    "value": "france",
    "equivalence": {
      "ISO3": "FRA"
    }
  }
]
```

Python scrip at the root of the project:

```python
import mater_data_providing as mdp
import pandas as pd

# 1. Build a DataFrame
df = pd.DataFrame([
    {"location": "FRA", "object": "personal_vehicle", "value": 15, "unit": "year", "time": 2015, "scenario": "historical", "variable": "lifetime_mean_value"},
    {"location": "france", "object": "PLDV", "value": 17, "unit": "year", "time": 2020, "scenario": "historical", "variable": "lifetime_mean_value"},
])

# 2. Create a provider and metadata dictionnary
provider = mdp.provider_definition("Jon", "Do", "jon.do@mail.com")
metadata = mdp.metadata_definition("source_link", "my_source", "my_project")

# 3. Dump the data into a serialized json
j = mdp.dump_json(input_data, provider, metadata)

# 4. Write out as "input_data/sample.json"
#    (creates data/input_data/sample.json)
mdp.to_json(
    j,
    name="sample",       # filename will be sample.json
    mode="w"             # write (overwrite) – this is the default
)
```

Creates data/input_data/sample.json:

```json
[
  {
    "location": "france",
    "object": "car",
    "value": 15,
    "unit": "year",
    "time": 2015,
    "scenario": "historical",
    "variable": "lifetime_mean_value"
  },
  {
    "location": "france",
    "object": "car",
    "value": 17,
    "unit": "year",
    "time": 2020,
    "scenario": "historical",
    "variable": "lifetime_mean_value"
  }
]
```
