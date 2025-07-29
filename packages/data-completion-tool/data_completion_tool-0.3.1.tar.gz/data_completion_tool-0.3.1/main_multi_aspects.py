"""Test the data completion tool with the small example in the excel file in the databases folder."""

import logging
import os

import numpy as np
import pandas as pd
from matplotlib.axes import Axes

from data_completion_tool.dct import DataSet, convert_to_datetime


def main():
    # logging configuration
    logging.basicConfig(
        encoding="utf-8",
        format="[%(asctime)s] %(levelname)s: %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # import .\data_completion_tool as dc

    path = os.path.join("databases", "paper_dataset_multiaspects.xlsx")
    df_dict = pd.read_excel(path, None)  # dict of all the database tables

    ds = DataSet()

    # set hierarchy dataframe
    ds.set_dimension(df_dict["dimension"])

    # # Not able to do extensive dimension for now.
    # w = {key: df_dict[key] for key in ["location_default_weightings", "object_default_weightings"]}
    # w["time"] = convert_to_datetime(w["time"])
    # ds.set_default_weightings(w)
    # # operation table by table
    variable_name = "object_composition"
    variable = df_dict[variable_name]
    # because not in date format in excel
    variable["time"] = convert_to_datetime(variable["time"])

    # make it for multiple variables

    variable_aspects = df_dict["variable_dimension"][df_dict["variable_dimension"]["variable"] == variable_name]
    aspect_property = variable_aspects[["dimension", "property"]].set_index("dimension").T.to_dict("list")
    # completion function

    final_df = ds.completion(variable, aspect_property)

    ds.plot_with_source(final_df, "multi_intensive_aspect", "lower right", same_figure=False)
    # plot
    index = np.setdiff1d(variable.columns, ["unit", "value", "source_id"]).tolist()
    raw_df = variable.dropna().set_index(index)["value"].unstack("time").T
    dataframes = [(raw_df, Axes.scatter, "value", 0)]

    ds.figure_production(dataframes, "multi_intensive_aspect", "lower right")


if __name__ == "__main__":
    main()
