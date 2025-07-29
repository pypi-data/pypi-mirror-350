"""
This is the main module to test features.

Copyright (C) 2025 @verzierf <francois.verzier@univ-grenoble-alpes.fr>

SPDX-License-Identifier: LGPL-3.0-or-later
"""

import pandas as pd

import src.mater_data_providing as mdp

# 1. Build a DataFrame
input_data = pd.DataFrame(
    [
        {
            "location": "france",
            "object": "car",
            "value": 15,
            "unit": "year",
            "time": 2015,
            "scenario": "historical",
            "variable": "lifetime_mean_value",
        },
        {
            "location": "france",
            "object": "car",
            "value": 17,
            "unit": "year",
            "time": 2020,
            "scenario": "historical",
            "variable": "lifetime_mean_value",
        },
    ]
)

# 2. Create a provider and metadata dictionnary
provider = mdp.provider_definition("Jon", "Do", "jon.do@mail.com")
metadata = mdp.metadata_definition("source_link", "my_source", "my_project")

# 3. Dump the data into a serialized json
j = mdp.dump_json(input_data, provider, metadata)
print(j)
