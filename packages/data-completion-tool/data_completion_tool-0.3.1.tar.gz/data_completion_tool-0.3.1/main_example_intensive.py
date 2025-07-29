"""Test the data completion tool with the small example in the excel file in the databases folder."""

import logging
import os

import pandas as pd
from matplotlib.axes import Axes

from src.data_completion_tool.dct import DataSet, convert_to_datetime


def main():
    # logging configuration
    logging.basicConfig(
        encoding="utf-8",
        format="[%(asctime)s] %(levelname)s: %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # import .\data_completion_tool as dc

    path = os.path.join("databases", "paper_dataset.xlsx")
    df_dict = pd.read_excel(path, None)  # dict of all the database tables

    ds = DataSet()
    ds.set_hierarchy(df_dict["object_hierarchy"])
    w = df_dict["object_default_weightings"]
    w["time"] = convert_to_datetime(w["time"])
    ds.set_default_weightings(w)
    # operation table by table

    variable = df_dict["variable"]
    variable["time"] = convert_to_datetime(variable["time"])

    reconstitution_mode = variable[variable["source_id"].isna()]["object"].values[0]

    # completion function

    final_df = ds.completion(variable, reconstitution_mode)

    ds.plot_with_source(final_df, "intensive_example", "lower right", same_figure=False)
    # plot
    raw_df = (
        variable.dropna().drop(["unit", "source_id"], axis=1).set_index(["object", "time"])["value"].unstack("time").T
    )
    dataframes = [(raw_df, Axes.scatter, "value", 0)]

    ds.figure_production(dataframes, "intensive_example", "lower right")


if __name__ == "__main__":
    main()
