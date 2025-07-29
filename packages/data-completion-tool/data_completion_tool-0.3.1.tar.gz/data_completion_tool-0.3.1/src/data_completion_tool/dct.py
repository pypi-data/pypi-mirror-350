"""Create the class to perform data completion algorithms on a preformated database."""

import os
from typing import Callable, Dict, List, Literal, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.lines import Line2D
from matplotlib.pyplot import Axes


class DataSet:
    def __init__(self):
        self.color_mapping = None
        self.marker_mapping = None

    def set_dimension(self, dimension: pd.DataFrame):
        if "equivalence" in dimension.columns:
            dimension = dimension.drop("equivalence", axis=1)
        self.dimension = dimension
        # self._set_mappers()

    def set_default_weightings(self, weightings: Dict[str, pd.DataFrame]):
        self.default_weightings = weightings

    def completion(
        self, df: pd.DataFrame, aspect_property: Dict[str, List[Literal["intensive", "extensive"]]]
    ) -> pd.DataFrame:
        merged_df = df.copy()
        self._set_indexes(merged_df)
        # prepare the source_id to keep trace of the reconstitution parent
        merged_df["source_id"] = merged_df.index.droplevel(["time", "unit"]).tolist()
        # interpolated_df initialization
        completed_df = pd.DataFrame()
        # aspects
        extensive_key = next((key for key, value in aspect_property.items() if "extensive" in value), None)
        intensive_aspects = [key for key, value in aspect_property.items() if "intensive" in value]
        # init counter for the while loop
        i = 0
        while not merged_df.equals(completed_df):
            if i != 0:
                merged_df = completed_df.copy()
            # interpolation
            interpolated_df_template = self._df_interpolation(merged_df, limit_area="inside")
            interpolated_df = interpolated_df_template.dropna()
            # For loop on the aspects
            for aspect in intensive_aspects:
                # rename hierarchy columns for the aspect name to match the dimension name ("object_parent" to "object_composition_parent")

                dim = aspect.split("_")[0]
                dimension = self.dimension[self.dimension["name"] == dim].drop(columns=["name"])
                dimension.rename(columns={"value": aspect, "parents_values": f"{aspect}_parent"}, inplace=True)
                # parent value to children
                ## rename aspect to aspect_parent
                df1 = interpolated_df.rename_axis(index={aspect: f"{aspect}_parent"}).reset_index()
                ## merge to find corresponding children (enable to pass the value to the children)
                df2 = df1.merge(dimension, how="left", on=f"{aspect}_parent").dropna()
                self._set_indexes(df2)
                # Filter df2 if extensive aspect
                if extensive_key:
                    # Extracting the intensive_aspects present in interpolated_df
                    existing_keys = set(interpolated_df.groupby(level=intensive_aspects).count().index)
                    # Dropping irrelevant levels from df2 before comparison
                    df2_reduced = df2.index.droplevel([lvl for lvl in df2.index.names if lvl not in intensive_aspects])
                    # Creating a boolean mask
                    mask = ~df2_reduced.isin(existing_keys)
                    # Applying the mask correctly to df2
                    df2 = df2[mask]
                # When merged_df.equals(completed_df), df2 is empty
                if not df2.empty:
                    interpolated_df = interpolated_df.combine_first(df2).droplevel(f"{aspect}_parent")
            # update completed_df before next while loop
            completed_df = interpolated_df.copy()
            # update counter
            i += 1
        # Final filtering to get rid off interpolated values
        return completed_df[completed_df["source_id"] != "interpolation"]

    def figure_production(
        self,
        dataframes: List[Tuple[pd.DataFrame, str | Callable[..., Axes], str, int]],
        figure_name: str,
        legend_loc: str,
        font_size: int = 16,
    ):
        unique_objects = np.unique(np.concatenate([df[0].columns.values for df in dataframes]))
        self._get_mappers(unique_objects, unique_objects)

        # Dictionary to keep track of figures and axes
        figures_axes = {}

        # Plot each DataFrame in a separate subplot
        for df, plot_func, ylabel, i in dataframes:
            if i not in figures_axes:
                # Create a new figure and axis if not already created for this index
                fig, ax = plt.subplots(1, 1, figsize=(8, 5))
                figures_axes[i] = (fig, ax)
            else:
                # Get the existing figure and axis
                fig, ax = figures_axes[i]

            # Plot the data
            if plot_func == "area":
                ax.stackplot(
                    df.index,
                    [df[col] for col in df.columns],
                    labels=df.columns,
                    colors=[self.color_mapping[col] for col in df.columns],
                )
            else:
                for column in df.columns:
                    if column in self.marker_mapping:
                        plot_func(
                            ax,
                            df.index,
                            df[column],
                            label=column,
                            color=self.color_mapping.get(column, None),
                            marker=self.marker_mapping[column],
                        )
                    else:
                        plot_func(
                            ax,
                            df.index,
                            df[column],
                            label=column,
                            color=self.color_mapping.get(column, None),
                        )
            ax.set_ylabel(ylabel, fontsize=font_size)

        # After plotting all data, add legends and save figures
        for i, (fig, ax) in figures_axes.items():
            ax.tick_params(axis="both", which="major", labelsize=font_size)
            ax.legend(fontsize=font_size, loc=legend_loc)
            fig.savefig(
                os.path.join("images", f"{figure_name}{i}.png"),
                dpi=300,
                bbox_inches="tight",
            )
            plt.close(fig)

    def plot_with_source(
        self,
        df: pd.DataFrame,
        figure_name: str,
        legend_loc: str,
        same_figure: bool = True,
        font_size: int = 16,
    ):
        df = df.reset_index()
        # List of aspects
        aspects = np.setdiff1d(df.columns.tolist(), ["time", "unit", "value", "source_id"]).tolist()
        # get a color map for each aspects tuple and a marker map for each source_id
        unique_aspects = df.groupby(list(aspects)).size().index.tolist()
        unique_sources = df["source_id"].unique()
        self._get_mappers(unique_aspects, unique_sources)

        # Create the plot
        if same_figure:
            fig, ax = plt.subplots(figsize=(8, 5))
            # Create custom legend handles for markers
            marker_legend_handles = [
                Line2D(
                    [0],
                    [0],
                    marker=self.marker_mapping[key],
                    color="w",
                    markerfacecolor="black",
                    markersize=font_size / 2,
                    label=key,
                )
                for key in unique_sources
            ]
            # Add a custom legend handle for interpolation
            interpolation_handle = Line2D([0], [0], color="black", lw=font_size / 10, label="interpolation")

        # Plot each source_id with different colors
        for aspect, group_df in df.groupby(aspects):
            if not same_figure:
                fig, ax = plt.subplots(figsize=(8, 5))
            for source_id, group in group_df.groupby("source_id"):
                ax.scatter(
                    group["time"],
                    group["value"],
                    label=f"{source_id}",
                    color=self.color_mapping[aspect],
                    marker=self.marker_mapping[source_id],
                )
            ax.plot(
                group_df["time"],
                group_df["value"],
                label="interpolation",
                color=self.color_mapping[aspect],
            )
            if not same_figure:
                # Set labels and title
                ax.set_ylabel("Value", fontsize=font_size)
                # ax.set_xlabel("time", fontsize=14)
                ax.tick_params(axis="both", which="major", labelsize=font_size)  # Customize tick parameters
                ax.legend(loc=legend_loc, fontsize=font_size)
                plt.savefig(
                    os.path.join("images", f"{figure_name} {aspect}.png"),
                    dpi=300,
                    bbox_inches="tight",
                )
        if same_figure:
            # Set labels and title
            ax.set_ylabel("Value", fontsize=font_size)
            # ax.set_xlabel("time", fontsize=14)
            ax.tick_params(axis="both", which="major", labelsize=font_size)  # Customize tick parameters
            # Calculate dynamic positioning for legends
            # color_legend_height = (
            #     len(color_legend_handles) * 0.01 * font_size
            # )  # height per legend item
            first_legend = ax.legend(
                handles=marker_legend_handles + [interpolation_handle],
                # title="markers",
                fontsize=font_size,
                loc=legend_loc,
                bbox_to_anchor=(0, 1),
                bbox_transform=ax.transAxes,
            )
            ax.add_artist(first_legend)
            # ax.add_artist(second_legend)
            plt.savefig(
                os.path.join("images", f"{figure_name}_with_source.png"),
                dpi=300,
                bbox_inches="tight",
            )

    def _df_interpolation(self, df: pd.DataFrame, limit_area: str | None = None) -> pd.DataFrame:
        interpol_df = df["value"].unstack("time")
        # drop nan in date column
        interpol_df = interpol_df.loc[:, interpol_df.columns.notna()]

        # perform interpolation
        if limit_area:
            interpolated_df = interpol_df.interpolate(axis=1, limit_area=limit_area, method="time")
        else:
            interpolated_df = interpol_df.interpolate(
                axis=1, limit_area=limit_area, method="time", limit_direction="both"
            )
        interpolated_df = interpolated_df.stack("time", future_stack=True).to_frame("value")
        # add source
        interpolated_df["source_id"] = "interpolation"
        # add interpolated_df to initial df
        df = df.combine_first(interpolated_df)

        return df

    # def _set_mappers(self) -> Dict[str, Dict[str, Tuple[np.float64] | str]]:
    #     unique_objects = self.dimension["object"].unique()

    #     # Generate a color palette
    #     colors = plt.colormaps["Set1"]
    #     markers = ["o", "s", "^", "D", "v", "P", "*", "X"]  # List of markers

    #     # Create a dictionary mapping each object to a color
    #     self.color_mapping = {src: colors(i) for i, src in enumerate(unique_objects)}
    #     self.marker_mapping = {
    #         src: markers[i % len(markers)] for i, src in enumerate(np.setdiff1d(unique_objects, "interpolation"))
    #     }

    def _get_mappers(self, unique_objects, unique_sources):
        if not self.color_mapping:
            colors = plt.colormaps["Set1"]
            self.color_mapping = {src: colors(i) for i, src in enumerate(unique_objects)}
        if not self.marker_mapping:
            markers = ["o", "s", "^", "D", "v", "P", "*", "X"]  # List of markers
            self.marker_mapping = {
                src: markers[i % len(markers)] for i, src in enumerate(np.setdiff1d(unique_sources, "interpolation"))
            }

    def _set_indexes(self, df: pd.DataFrame):
        """Set indexes of a no index dataframe keeping only the "value" and "source_id" in columns.

        :param df: DataFrame to operate on
        :type df: pd.DataFrame
        """
        df.set_index(
            list(np.setdiff1d(df.columns.values, np.array(["value", "source_id"]))),
            inplace=True,
        )


def convert_to_datetime(column: pd.Series) -> pd.Series:
    """
    Converts a column of mixed date formats (float, string, or int) to pandas datetime.
    Handles formats like YYYYMMDD and epoch time systematically.

    :param column: pandas Series containing date values.
    :return: pandas Series with converted datetime values.
    """

    def parse_date(value):
        try:
            # Handle float and integer
            if isinstance(value, (float, int)):
                return pd.to_datetime(str(int(value)), errors="coerce")

            # Handle strings
            elif isinstance(value, str):
                return pd.to_datetime(value, errors="coerce")

        except Exception:
            return pd.NaT

    # Apply the parsing function to each value in the column
    return column.apply(parse_date)
