"""Test the data completion tool with the small example in the excel file in the databases folder."""

import logging
import os

import numpy as np
import pandas as pd
from matplotlib.axes import Axes

from src.data_completion_tool import dct


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

    ds = dct.DataSet()
    ds.set_hierarchy(df_dict["object_hierarchy"])
    w = df_dict["object_default_weightings"]
    w["time"] = dct.convert_to_datetime(w["time"])
    ds.set_default_weightings(w)
    # operation table by table

    variable = df_dict["extensive variable"]
    variable["time"] = dct.convert_to_datetime(variable["time"])

    reconstitution_mode = variable[variable["source_id"].isna()]["object"].values[0]

    # completion function

    final_df = ds.completion(variable, reconstitution_mode)
    ds.plot_with_source(
        final_df.loc[["child 1.1", "child 1.2", "parent 2"], :, :],
        "extensive_example",
        "upper left",
    )
    # plot
    df = final_df.droplevel("unit")["value"].unstack("time").T
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
    dataframes = [
        (df[["child 1.1", "child 1.2", "parent 2"]], "area", "value", 1),
        (raw_df, Axes.scatter, "value", 1),  # df, plot type, y_label, figure number
        (weightings[["parent 1", "parent 2"]], "area", "(dmls)", 2),
        (weightings[["child 1.1", "child 1.2"]], "area", "(dmls)", 3),
    ]

    ds.figure_production(dataframes, "extensive_example", "upper left")


if __name__ == "__main__":
    main()
