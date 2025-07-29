#####
# Imports
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from shapely import Point
from .core import get_points as _get_points
from .core import get_xs_ys as _get_xs_ys
from .core import get_datetimes as _get_datetimes
from .core import get_zs as _get_zs


#####
# Plots
def spatial(
        df: pd.DataFrame = None,
        points: str | pd.Series | list[tuple[int, int], Point] = None,
        sp_threshold: int | float = None,
        colour: str = '#4d4d4d'):
    """Spatially plot the points with the spatial threshold illustrated by a pale circle around each point."""

    fig, ax = plt.subplots(figsize=(16, 16))

    points = _get_points(df=df, points=points)
    xs, ys = _get_xs_ys(points=points)
    for x, y in zip(xs, ys):
        ax.add_patch(plt.Circle((x, y), sp_threshold / 2,
                                facecolor=colour, alpha=0.2, edgecolor='none', zorder=1))
    ax.scatter(xs, ys, s=2, color=colour)

    ax.set_xlim(min(xs) - sp_threshold, max(xs) + sp_threshold)
    ax.set_ylim(min(ys) - sp_threshold, max(ys) + sp_threshold)
    ax.set_aspect('equal', adjustable='box')


def spatial_thinned(
        df_kept: pd.DataFrame = None,
        points_kept: str | pd.Series | list[tuple[int, int], Point] = None,
        df_removed: pd.DataFrame = None,
        points_removed: str | pd.Series | list[tuple[int, int], Point] = None,
        sp_threshold: int | float = None):
    """Spatially plot the points that were kept (blue) and those that were removed (red) after thinning with the spatial
     threshold illustrated by a pale circle around each point."""

    fig, ax = plt.subplots(figsize=(16, 16))

    points_kept = _get_points(df=df_kept, points=points_kept)
    xs_kept, ys_kept = _get_xs_ys(points=points_kept)
    for x, y in zip(xs_kept, ys_kept):
        ax.add_patch(plt.Circle((x, y), sp_threshold / 2,
                                facecolor='#0055a3', alpha=0.2, edgecolor='none', zorder=1))
    ax.scatter(xs_kept, ys_kept, s=2, color='#0055a3')

    points_removed = _get_points(df=df_removed, points=points_removed)
    xs_removed, ys_removed = _get_xs_ys(points=points_removed)
    for x, y in zip(xs_removed, ys_removed):
        ax.add_patch(plt.Circle((x, y), sp_threshold / 2,
                                facecolor='#fdbe57', alpha=0.2, edgecolor='none', zorder=1))
    ax.scatter(xs_removed, ys_removed, s=2, color='#fdbe57')

    ax.set_xlim(min(xs_kept + xs_removed) - sp_threshold, max(xs_kept + xs_removed) + sp_threshold)
    ax.set_ylim(min(ys_kept + ys_removed) - sp_threshold, max(ys_kept + ys_removed) + sp_threshold)
    ax.set_aspect('equal', adjustable='box')


unit_codes = {
    'year': ['Y', '%Y'],
    'day': ['D', '%Y-%m-%d'],
    'hour': ['h', '%Y-%m-%d %H:%M']
}


def temporal(
        df: pd.DataFrame = None,
        datetimes: pd.Series | list[pd.Timestamp | datetime] = None,
        tm_threshold: int | float = None,
        tm_unit: str = 'day',
        colour: str = '#4d4d4d'):
    """Temporally plot the points with the temporal threshold illustrated by a pale line centred around each point."""

    fig, ax = plt.subplots(figsize=(16, 16))

    datetimes = _get_datetimes(df=df, datetimes=datetimes)
    units = _get_zs(datetimes=datetimes, tm_unit=tm_unit)
    units.sort()
    lines = [[unit - tm_threshold / 2, unit + tm_threshold / 2] for unit in units]
    for index in range(len(units)):
        ax.plot(lines[index], [index, index], color=colour, alpha=0.2)
        ax.plot([units[index], units[index]], [index - 0.1, index + 0.1], color=colour)

    if tm_unit == 'doy':
        ax.set_xlabel('Time (day of year)')
    else:
        ax.set_xlabel('Time')
        labels = ax.get_xticklabels()
        if tm_unit == 'year':
            labels_datetimes = [
                pd.to_datetime(str(int(float(label.get_text()))), format='%Y').strftime(unit_codes[tm_unit][1])
                for label in labels]
        else:
            labels_datetimes = [pd.to_datetime(int(float(label.get_text())),
                                               unit=unit_codes[tm_unit][0]).strftime(unit_codes[tm_unit][1])
                                for label in labels]
        ax.set_xticks([int(float(label.get_text())) for label in labels])
        ax.set_xticklabels(labels_datetimes, ha='right')
        ax.tick_params(axis='x', labelrotation=45)

    ax.set_xlim(min(units) - tm_threshold, max(units) + tm_threshold)
    ax.set_ylim(-1, len(units) + 1)
    ax.tick_params(axis='y', which='both', left=False, labelleft=False)
    fig.set_tight_layout(True)


def temporal_thinned(
        df_kept: pd.DataFrame = None,
        datetimes_kept: pd.Series | list[pd.Timestamp | datetime] = None,
        df_removed: pd.DataFrame = None,
        datetimes_removed: pd.Series | list[pd.Timestamp | datetime] = None,
        tm_threshold: int | float = None,
        tm_unit: str = 'day'):
    """Temporally plot the points that were kept (blue) and those that were removed (red) after thinning with the
     temporal threshold illustrated by a pale line centred around each point."""

    fig, ax = plt.subplots(figsize=(16, 16))

    datetimes_kept = _get_datetimes(df=df_kept, datetimes=datetimes_kept)
    datetimes_removed = _get_datetimes(df=df_removed, datetimes=datetimes_removed)
    units_kept = _get_zs(datetimes=datetimes_kept, tm_unit=tm_unit)
    units_removed = _get_zs(datetimes=datetimes_removed, tm_unit=tm_unit)
    units = pd.concat([pd.DataFrame({'units': units_kept, 'colours': '#0055a3'}),
                       pd.DataFrame({'units': units_removed, 'colours': '#fdbe57'})])
    units = units.sort_values('units').reset_index(drop=True)

    for index, unit, colour in zip(units.index, units['units'], units['colours']):
        ax.plot([unit - tm_threshold / 2, unit + tm_threshold / 2], [index, index], color=colour, alpha=0.2)
        ax.plot([unit, unit], [index - 0.1, index + 0.1], color=colour)

    if tm_unit == 'doy':
        ax.set_xlabel('Time (day of year)')
    else:
        ax.set_xlabel('Time')
        labels = ax.get_xticklabels()
        labels_datetimes = [pd.to_datetime(int(label.get_text()),
                                           unit=unit_codes[tm_unit][0]).strftime(unit_codes[tm_unit][1])
                            for label in labels]
        ax.set_xticks([int(label.get_text()) for label in labels])
        ax.set_xticklabels(labels_datetimes, ha='right')
        ax.tick_params(axis='x', labelrotation=45)

    ax.set_xlim(min(units['units']) - tm_threshold, max(units['units']) + tm_threshold)
    ax.set_ylim(-1, len(units) + 1)
    ax.tick_params(axis='y', which='both', left=False, labelleft=False)


def _cylinder(
        ax,
        x: int | float,
        y: int | float,
        z: int | float,
        radius: int | float,
        half_height: int | float,
        no_edges: int | float = 20,
        colour: str = '#4d4d4d'):
    theta = np.linspace(0, 2 * np.pi, no_edges)
    zs = np.linspace(z - half_height, z + half_height, 2)
    theta_cylinder, z_cylinder = np.meshgrid(theta, zs)
    x_cylinder = radius * np.cos(theta_cylinder) + x
    y_cylinder = radius * np.sin(theta_cylinder) + y
    ax.plot_surface(x_cylinder, y_cylinder, z_cylinder, color=colour, alpha=0.2)

    x_cap_bot = radius * np.cos(theta) + x
    y_cap_bot = radius * np.sin(theta) + y
    z_cap_bot = z - half_height * np.ones(no_edges)
    ax.plot_trisurf(x_cap_bot, y_cap_bot, z_cap_bot, color=colour, alpha=0.2)

    x_cap_top = radius * np.cos(theta) + x
    y_cap_top = radius * np.sin(theta) + y
    z_cap_top = z + half_height * np.ones(no_edges)
    ax.plot_trisurf(x_cap_top, y_cap_top, z_cap_top, color=colour, alpha=0.2)


def spatiotemporal(
        df: pd.DataFrame = None,
        points: str | pd.Series | list[tuple[int, int], Point] = None,
        sp_threshold: int | float = None,
        datetimes: pd.Series | list[pd.Timestamp | datetime] = None,
        tm_threshold: int | float = None,
        tm_unit: str = 'day',
        colour: str = '#4d4d4d',
        no_edges: int | float = 20):
    """Spatiotemporally plot the points as cylinders with the spatial threshold illustrated by the diameter (x and y
     axes) and the temporal threshold illustrated by the height (z axis). The plot will be interactive and can be
     rotated.
    Note that the plot will be slow to make and rotate if the number of points is large (e.g., >200)."""

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    points = _get_points(df=df, points=points)
    xs, ys = _get_xs_ys(points=points)
    datetimes = _get_datetimes(df=df, datetimes=datetimes)
    units = _get_zs(datetimes=datetimes, tm_unit=tm_unit)
    for x, y, z in zip(xs, ys, units):
        _cylinder(ax=ax, x=x, y=y, z=z, radius=sp_threshold / 2, half_height=tm_threshold / 2,
                  no_edges=no_edges, colour=colour)

    ax.set_xlim(min(xs) - sp_threshold, max(xs) + sp_threshold)
    ax.set_ylim(min(ys) - sp_threshold, max(ys) + sp_threshold)
    ax.set_zlim(min(units) - tm_threshold, max(units) + tm_threshold)
    ax.set_xlabel('space (x axis)')
    ax.set_ylabel('space (y axis)')
    ax.set_zlabel('time (z axis)')
    ax.tick_params(axis='z', which='both', left=False, labelleft=False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.set_aspect('equalxy', adjustable='box')


def spatiotemporal_thinned(
        df_kept: pd.DataFrame = None,
        points_kept: str | pd.Series | list[tuple[int, int], Point] = None,
        datetimes_kept: pd.Series | list[pd.Timestamp | datetime] = None,
        df_removed: pd.DataFrame = None,
        points_removed: str | pd.Series | list[tuple[int, int], Point] = None,
        datetimes_removed: pd.Series | list[pd.Timestamp | datetime] = None,
        sp_threshold: int | float = None,
        tm_threshold: int | float = None,
        tm_unit: str = 'day',
        no_edges: int | float = 20):
    """Spatiotemporally plot the points that were kept (blue) and those that were removed (red) after thinning as
     cylinders with the spatial threshold illustrated by the diameter (x and y axes) and the temporal threshold
     illustrated by the height (z axis). The plot will be interactive and can be rotated.
    Note that the plot will be slow to make and rotate if the number of points is large (e.g., >200)."""

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    points_kept = _get_points(df=df_kept, points=points_kept)
    xs_kept, ys_kept = _get_xs_ys(points=points_kept)
    datetimes_kept = _get_datetimes(df=df_kept, datetimes=datetimes_kept)
    units_kept = _get_zs(datetimes=datetimes_kept, tm_unit=tm_unit)
    for x, y, z in zip(xs_kept, ys_kept, units_kept):
        _cylinder(ax=ax, x=x, y=y, z=z, radius=sp_threshold / 2, half_height=tm_threshold / 2,
                  no_edges=no_edges, colour='#0055a3')

    points_removed = _get_points(df=df_removed, points=points_removed)
    xs_removed, ys_removed = _get_xs_ys(points=points_removed)
    datetimes_removed = _get_datetimes(df=df_removed, datetimes=datetimes_removed)
    units_removed = _get_zs(datetimes=datetimes_removed, tm_unit=tm_unit)
    for x, y, z in zip(xs_removed, ys_removed, units_removed):
        _cylinder(ax=ax, x=x, y=y, z=z, radius=sp_threshold / 2, half_height=tm_threshold / 2,
                  no_edges=no_edges, colour='#fdbe57')

    ax.set_xlim(min(xs_kept + xs_removed) - sp_threshold, max(xs_kept + xs_removed) + sp_threshold)
    ax.set_ylim(min(ys_kept + ys_removed) - sp_threshold, max(ys_kept + ys_removed) + sp_threshold)
    ax.set_zlim(min(units_kept + units_removed) - tm_threshold, max(units_kept + units_removed) + tm_threshold)
    ax.set_xlabel('space (x axis)')
    ax.set_ylabel('space (y axis)')
    ax.set_zlabel('time (z axis)')
    ax.tick_params(axis='z', which='both', left=False, labelleft=False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.set_aspect('equalxy', adjustable='box')

