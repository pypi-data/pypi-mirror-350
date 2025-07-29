"""Test the data completion tool with the small example in the excel file in the databases folder."""

import logging
import os

import numpy as np
import pandas as pd
from matplotlib.axes import Axes

from src.data_completion_tool.dct import DataSet, convert_to_datetime


def main():
    # logging configuration
    logging.basicConfig(
        encoding="utf-8",
        format="[%(asctime)s] %(levelname)s: %(message)s",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # import .\data_completion_tool as dc

    path = os.path.join("databases", "worse_case_dataset.xlsx")
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
    ds.plot_with_source(final_df.loc[["child 1", "child 2"], :, :], "worst_case", "upper left")
    df = final_df.droplevel("unit")["value"].unstack("time").T
    # plot
    raw_df = (
        variable.dropna().drop(["unit", "source_id"], axis=1).set_index(["object", "time"])["value"].unstack("time").T
    )
    weightings_df = (
        df_dict["object_default_weightings"]
        .drop(["unit", "source_id", "object_parent"], axis=1)
        .set_index(["object", "time"])["value"]
        .unstack("time")
    )
    weights = pd.DataFrame(np.nan, index=weightings_df.index, columns=df.index)
    weightings = weightings_df.add(weights, fill_value=0)
    weightings = weightings.interpolate(method="index", axis=1, limit_direction="both").T
    # weighted average
    df["children w.a."] = (df[["child 1", "child 2"]] * weightings.loc[df.index]).sum(axis=1)
    dataframes = [
        (raw_df, Axes.scatter, "value", 0),
        (weightings, "area", "(dmls)", 1),
        (df[["parent", "children w.a."]], Axes.plot, "value", 3),
    ]

    ds.figure_production(dataframes, "worst_case_dataset", "upper left")


if __name__ == "__main__":
    main()
