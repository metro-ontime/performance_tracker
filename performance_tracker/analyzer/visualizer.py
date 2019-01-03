import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
import pendulum


class Marey:
    def __init__(self, minTime, maxTime, vehicle_positions, schedule, stations):
        self.stations = stations
        self.train_ids = list(vehicle_positions["trip_id"].unique())
        self.colors = assignColorsToTrains(self.train_ids)
        self.trips = vehicle_positions.sort_values("datetime").groupby("trip_id")
        self.minTime = mpl.dates.date2num(minTime)
        self.maxTime = mpl.dates.date2num(maxTime)
        self.schedule = schedule.sort_values("datetime").groupby("trip_id")

    def plot(self, width, height):
        plt.style.use("dark_background")
        fig = plt.figure(figsize=[width, height])
        axis = fig.add_subplot(121)
        format_time_axis(axis, self.maxTime, self.minTime)
        format_location_axis(axis)

        draw_marey(axis, self.trips, "#ff0000")
        draw_marey(axis, self.schedule, "#444444")

        for station in self.stations.itertuples():
            axis.axvline(
                station.relative_position, color="#555555", lw=1, linestyle="-."
            )
            axis.text(
                station.relative_position,
                self.maxTime,
                station.stop_name + "  ",
                fontSize="18",
                color="#999999",
                rotation="vertical",
                horizontalalignment="center",
                verticalalignment="top",
            )


def draw_marey(axis, trips, col):
    for index, trip in trips:
        times = [
            mpl.dates.date2num(pendulum.parse(str(dt)))
            for dt in trip["datetime"].values
        ]
        positions = trip["relative_position"].values
        axis.plot(positions, times, lw=2, color=col)


def makeLineMap(line):
    line_plot = gpd.GeoSeries(line)
    line_plot = line_plot.plot(figsize=(24, 24), color="white")
    line_plot.set_facecolor("#111111")
    line_plot.spines["bottom"].set_color("white")
    line_plot.spines["left"].set_color("white")
    line_plot.xaxis.label.set_color("white")
    line_plot.tick_params(axis="x", colors="white")
    line_plot.yaxis.label.set_color("white")
    line_plot.tick_params(axis="y", colors="white")
    line_plot.set_xlabel("Longitude")
    line_plot.set_ylabel("Latitude")
    return line_plot


def assignColorsToTrains(train_ids):
    vals = np.linspace(0, 1, len(train_ids))
    np.random.shuffle(vals)
    colors = plt.cm.colors.ListedColormap(plt.cm.jet(vals))
    return {train_ids[index]: colors(index) for index in range(len(train_ids))}


def format_time_axis(axis, time_min, time_max):
    time_interval = mpl.dates.MinuteLocator(byminute=None, interval=5, tz=None)
    interval_format = mpl.dates.DateFormatter("%H:%M")
    axis.set_ylim(time_min, time_max)
    axis.yaxis.set_major_locator(time_interval)
    axis.yaxis.set_major_formatter(interval_format)
    axis.set_xlim(0, 1)


def format_location_axis(axis):
    axis.set_xticks([])
