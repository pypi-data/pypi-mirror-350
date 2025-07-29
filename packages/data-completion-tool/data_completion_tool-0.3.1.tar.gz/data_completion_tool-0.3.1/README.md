# Data completion tool

A module to create a dataset with a parent/children hierarchy (H-MECE) and permorm a completion algorithm (parent/children disaggregation and time interpolation). It is used to transform a sparse dataset into a complete dataset ready to be used in a model.

There are some plot functions to visualize the results of the completion algorithm keeping a trace of the aggregations and interpolations made to facilitate any revue of the dataset.

[TOC]

## 📋 Requirements

- Python 3.12 or higher

We recommend using one virtual environment per Python project to manage dependencies and maintain isolation. You can use a package manager like [uv](https://docs.astral.sh/uv/) to help you with library dependencies and virtual environments.

## 📦 Install the data-completion-tool Package

Install the `data-completion-tool` package via pip:

```bash
pip install data-completion-tool
```

## ⚙️ Complete a dataset

Here is an example of a variable completion using a specified hierarchy:

```python
import pandas as pd
from data_completion_tool import dct

# Create a Dataset instance
ds = dct.DataSet()

# Create a dimension dataframe to set the hierarchy
dimension = pd.DataFrame(
    {"name": ["location"], "value": ["france"], "parents_values": ["europe"]}
)
ds.set_dimension(dimension)

# Create a variable to complete
variable = pd.DataFrame(
        {
            "location": ["france", "france", "france", "europe", "europe", "europe"],
            "time": [1950, 1980, 2000, 1920, 1970, 2020],
            "value": [15, 40, 65, 10, 54, 76],
            "unit": ["random", "random", "random", "random", "random", "random"],
            "source_id": [1, 1, 1, 2, 2, 2],
        }
    )

# Create aspect properties
aspect_property = {"location": ["intensive"]}

# Complete the dataset
completed_dataset = ds.completion(variable, aspect_property)
```

## 📊 Visualize Datasets

You can visualise the completed datasets using special methods of the DataSet class:

```python
ds.plot_with_source(completed_dataset, "variable", "lower right", same_figure=True)
```

## 🤝 Contributing

We welcome contributions to the Data providing project! To get started, please refer to the [CONTRIBUTING](CONTRIBUTING.md) file for detailed guidelines.
