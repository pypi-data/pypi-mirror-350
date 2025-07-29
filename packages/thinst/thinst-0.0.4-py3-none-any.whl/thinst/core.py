#####
# Imports
from collections import Counter
from datetime import datetime
from itertools import combinations
import numpy as np
import pandas as pd
from random import choice
from scipy.spatial import cKDTree
from shapely import Point


#####
# Main function
def thinst(
        df: pd.DataFrame = None,
        points: str | pd.Series | list[tuple[int, int], Point] = None,
        sp_threshold: int | float = None,
        datetimes: str | pd.Series | list[str | pd.Timestamp | datetime] = None,
        tm_threshold: int | float = None,
        tm_unit: str = 'day',
        ids: pd.Series | list[str | int | float] = None,
        no_reps: int = 100) \
        -> pd.DataFrame | tuple[list | list | list]:
    """Thin datapoints spatially, temporally, or spatiotemporally.

    Spatial thinning will remove points so that no two points are within a given spatial threshold of each other.
    Temporal thinning will remove points so that no two points are within a given temporal threshold of each other.
    Spatiotemporal thinning will remove points so that no two points are within a given spatial threshold and within a
     given temporal threshold of each other. Accordingly, two points may overlap spatially, provided that they do not
     overlap temporally and vice versa.

    For input, there are two options:
    The first is to input a pandas.DataFrame or geopandas.GeoDataFrame and specify the column(s) that contain the points
     and/or datetimes. In this case, df will be the DataFrame and points and datetimes will be the names of the columns
     that contain the points and datetimes, respectively.
    The second is to input the points and/or datetimes as lists or pandas.Series. In this case, df will be None and
     points and datetimes will be the lists or pandas.Series that contain the points and datetimes, respectively.
    With both input options, the spatial threshold is set with sp_threshold and the temporal threshold with
     tm_threshold. Additionally, the units of the temporal threshold are set with tm_unit.
    If both a spatial and temporal threshold are specified, spatiotemporal thinning will occur. If only a spatial
     threshold is specified, spatial thinning will occur. If only a temporal threshold is specified, temporal thinning
     will occur.
    Note that spatial thinning uses Euclidean distances and so is incompatible with latitude-longitude coordinates.
     Latitude-longitude coordinates must be reprojected into a projected CRS before thinning. Moreover, there will be
     some discrepancy between these Euclidean distances and geodesic distances. Assuming an appropriate CRS is chosen,
     this discrepancy should be negligible over short distances (<0.1% for distances <1000 kms) and medium distances
     (<1% for distances <2500 kms), but may become more significant for longer distances.
    __________
    Parameters:
    df: pd.DataFrame | gpd.GeoDataFrame, optional, default None
      A dataframe containing the points to be thinned. If specified, the column(s) containing the points and/or
       datetimes must be specified with the parameters points and datetimes, respectively.
    points : str | pd.Series | list[tuple[int, int], Point], optional, default None
      One of the following:
        the name of the column in df that contains the points
        a pandas.Series of coordinates as tuples, e.g., (X, Y), or shapely Points, e.g., POINT (X, Y)
        a list of coordinates as tuples, e.g., (X, Y), or shapely Points, e.g., POINT (X, Y)
    sp_threshold : int | float, optional, default None
      The spatial threshold to use for spatial and spatiotemporal thinning in the units of the points.
    datetimes : str | pd.Series | list[str | pd.Timestamp | datetime], optional, default None
      One of the following:
        the name of the column in df that contains the datetimes
        a pandas.Series of datetimes as strings, pandas.Timestamps, or datetime.datetimes
        a list of datetimes as strings, pandas.Timestamps, or datetime.datetimes
    tm_threshold : int | float, optional, default None
      The temporal threshold to use for temporal and spatiotemporal thinning in the units set with tm_unit.
    tm_unit: {'year', 'month', 'day', 'hour', 'moy', 'doy'}, optional, default 'day'
      The temporal units to use for temporal and spatiotemporal thinning. One of the following:
        'year': year (all datetimes from the same year will be given the same value)
        'month': month (all datetimes from the same month and year will be given the same value)
        'day': day (all datetimes with the same date will be given the same value)
        'hour': hour (all datetimes in the same hour on the same date will be given the same value)
        'moy': month of the year (i.e., January is 1, February is 2 regardless of the year)
        'doy': day of the year (i.e., January 1st is 1, December 31st is 365 regardless of the year)
    ids : pd.Series | list[str | int | float], optional, default None
      If using the second option for data input, a pandas.Series or list of IDs to identify the points that were kept
       after thinning.
    no_reps : int, optional, default 100
      The number of repetitions to run when conducting thinning. From these repetitions, one of those that retains the
       most points will be output.
    __________
    Returns:
      One of the following, depending on the input:
        pd.DataFrame | gpd.GeoDataFrame
          A pandas.DataFrame or a geopandas.GeoDataFrame, depending on which was input, containing the points that were
           kept after thinning.
        tuple[list | list | list]
          A tuple containing three lists that contain the points, datetimes, and IDs, respectively. If one or more of
           the points, datetimes, and IDs is not input, an empty list will be returned in its place.
    """

    # get the close pairs
    if (isinstance(sp_threshold, int | float)  # if both a spatial...
            and isinstance(tm_threshold, int | float)):  # ...and temporal threshold are specified...
        points = get_points(df=df, points=points)  # get points
        datetimes = get_datetimes(df=df, datetimes=datetimes)  # get datetimes
        pairs = get_sptm_pairs(  # get spatiotemporal pairs
            points=points,
            sp_threshold=sp_threshold,
            datetimes=datetimes,
            tm_threshold=tm_threshold,
            tm_unit=tm_unit)

    elif (isinstance(sp_threshold, int | float)  # if only a spatial threshold is specified...
          and not isinstance(tm_threshold, int | float)):
        points = get_points(df=df, points=points)  # get points
        pairs = get_sp_pairs(  # get spatial pairs
            points=points,
            sp_threshold=sp_threshold)

    elif (isinstance(tm_threshold, int | float)  # if only a temporal threshold is specified...
          and not isinstance(sp_threshold, int | float)):
        datetimes = get_datetimes(df=df, datetimes=datetimes)  # get datetimes
        pairs = get_tm_pairs(  # get temporal pairs
            datetimes=datetimes,
            tm_threshold=tm_threshold,
            tm_unit=tm_unit)

    else:
        raise Exception('neither sp_threshold nor tm_threshold specified.')

    # thin
    if len(pairs) > 0:  # if there are close pairs (i.e., if thinning is required)...
        remove = selector(  # ...thin the pairs and get the indices to be removed and...
            pairs=pairs,
            no_reps=no_reps)
        removed = remover(  # ...return the thinned dataset
            remove=remove,
            df=df,
            points=points,
            datetimes=datetimes,
            ids=ids)
        return removed
    else:  # else if there are no close pairs (i.e., if thinning is not required), return what was input
        if isinstance(df, pd.DataFrame):
            return df
        else:
            return points, datetimes, ids


#####
# Functions
def get_points(df: pd.DataFrame = None, points: str | pd.Series | list = None)\
        -> list[tuple[float | int, float | int] | Point]:
    if isinstance(df, pd.DataFrame) and isinstance(points, str):  # option 1: dataframe and column name
        if points in df:  # if points is a column in the dataframe...
            points = list(df[points])  # ...convert the column to a list
        else:  # else if points is not a column in the dataframe...
            raise KeyError(f'the column {points} could not be found in the dataframe.')  # ...raise error
    elif isinstance(points, (pd.Series, list)):  # option 2: list or series
        points = list(points)  # convert points to list
    else:  # else an unknown combination of df and points, raise error...
        raise TypeError('df and/or points are of an invalid type.'
                        f'\nThe datatype of df is {type(df).__name__}'
                        f'\nThe datatype of points is {type(points).__name__}'
                        '\nPlease use one of the following options:'
                        '\n  Option 1: df is a pandas.DataFrame or geopandas.GeoDataFrame and '
                        'points is a string indicating the name of a column in df.'
                        '\n  Option 2: df is None and points is a list or pandas.Series.')

    # points is a list, now to check the datatypes of its elements
    dtypes = list(set([type(dt) for dt in points]))  # get the datatypes of the points
    if len(dtypes) == 1:  # else if there is only one datatype...
        if isinstance(points[0], (tuple, Point)):  # ...and that is tuple or Point...
            pass  # ...leave them as they are
        else:  # ...and that is some other datatype, raise error
            raise TypeError('the points are of an invalid datatype.'
                            f'\nPlease ensure that all points are of one of the following datatypes:'
                            f'\n  tuple (containing an x and y coordinate)'
                            f'\n  shapely.Point')
    elif len(dtypes) > 1:  # if there is more than one datatype, raise error
        raise TypeError('the points are of more than one datatype.'
                        f'\nThe datatypes are: {", ".join([dtype.__name__ for dtype in dtypes])}'
                        f'\nPlease ensure that all points are of one of the following datatypes:'
                        f'\n  tuple (containing an x and y coordinate)'
                        f'\n  shapely.Point')
    else:
        raise Exception('points is empty')
    return points  # return a list of points that are either tuples or Points


def get_sp_pairs(points: list[tuple[float | int, float | int] | Point], sp_threshold: int | float)\
        -> list[tuple[int, int]]:
    xs, ys = get_xs_ys(points=points)  # get xs and ys
    tree = cKDTree(np.array([xs, ys]).T)  # create a cKD tree from the x and y coordinates
    pairs_list = list(tree.query_pairs(sp_threshold))  # get indices of pairs that are too close
    return pairs_list


def get_xs_ys(points: list[tuple[float | int, float | int] | Point]) -> tuple[list[float | int], list[float | int]]:
    # points is a list of points that are either tuples or Points
    if isinstance(points[0], Point):  # if the points are Points...
        xs = [point.x for point in points]  # ...get the x coordinates of the points
        ys = [point.y for point in points]  # ...get the y coordinates of the points
    elif isinstance(points[0], tuple):  # if the points are tuples of x and y coordinates...
        xs = [point[0] for point in points]  # ...get the x coordinates of the points
        ys = [point[1] for point in points]  # ...get the y coordinates of the points
    else:  # else the points are neither Points nor tuples (should never be reached given checks in get_points)
        raise TypeError('points are of an invalid datatype')
    return xs, ys  # return the xs and ys as lists of integers


def get_datetimes(df: pd.DataFrame = None, datetimes: str | pd.Series | list = None) -> list[datetime | pd.Timestamp]:
    if isinstance(df, pd.DataFrame) and isinstance(datetimes, str):  # option 1: dataframe and column name
        if datetimes in df:  # if datetimes is a column in the dataframe...
            datetimes = list(df[datetimes])  # ...convert the column to a list
        else:  # else if datetimes is not a column in the dataframe...
            raise KeyError(f'the column {datetimes} could not be found in the dataframe.')  # ...raise error
    elif isinstance(datetimes, (pd.Series, list)):  # option 2: list or series
        datetimes = list(datetimes)  # convert datetimes to list
    else:  # else an unknown combination of df and points, raise error...
        raise TypeError('df and/or datetimes are of an invalid type.'
                        f'\nThe datatype of df is {type(df).__name__}'
                        f'\nThe datatype of datetimes is {type(datetimes).__name__}'
                        '\nPlease use one of the following options:'
                        '\n  Option 1: df is a pandas.DataFrame or geopandas.GeoDataFrame and '
                        'datetimes is a string indicating the name of a column in df.'
                        '\n  Option 2: df is None and datetimes is a list or pandas.Series.')

    # datetimes is a list, now to check the datatypes of its elements
    dtypes = list(set([type(dt) for dt in datetimes]))  # get the datatypes of the datetimes
    if len(dtypes) == 1:  # else if there is only one datatype...
        if isinstance(datetimes[0], str):  # ...and that is str...
            datetimes = [pd.to_datetime(date) for date in datetimes]  # ...convert the strings to Timestamps
        elif isinstance(datetimes[0], (pd.Timestamp, datetime)):  # ...and that is Timestamp or datetime...
            pass  # ...leave them as they are
        else:  # ...and that is some other datatype, raise error
            raise TypeError('the datetimes are of an invalid datatype.'
                            f'\nPlease ensure that all datetimes are of one of the following datatypes:'
                            f'\n  str'
                            f'\n  pandas.Timestamp'
                            f'\n  datetime.datetime')
    elif len(dtypes) > 1:  # if there is more than one datatype, raise error
        raise TypeError('the datetimes are of more than one datatype.'
                        f'\nThe datatypes are: {", ".join([dtype.__name__ for dtype in dtypes])}'
                        f'\nPlease ensure that all datetimes are of one of the following datatypes:'
                        f'\n  str'
                        f'\n  pandas.Timestamp'
                        f'\n  datetime.datetime')
    else:
        raise Exception('datetimes is empty')
    return datetimes  # return a list of datetimes or Timestamps


def get_tm_pairs(datetimes: list[datetime | pd.Timestamp], tm_threshold: int | float, tm_unit: str = 'day')\
        -> list[tuple[int, int]]:
    zs = get_zs(datetimes=datetimes, tm_unit=tm_unit)  # get the zs
    if tm_unit.lower() in ['year', 'month', 'day', 'hour']:  # if the temporal unit is linear
        tree = cKDTree(np.array([zs]).T)  # create a cKD tree from the x and y coordinates
        pairs_list = list(tree.query_pairs(tm_threshold))  # get indices of pairs that are too close
    elif tm_unit.lower() in ['moy', 'doy']:  # else if the temporal unit is cyclical
        if ((tm_unit == 'moy' and tm_threshold >= 6)  # if temporal threshold equal to or more than half...
                or (tm_unit == 'doy' and tm_threshold >= 182.5)):  # ...a cycle (12 months / 365 days)...
            pairs_list = list(combinations(range(0, len(zs)), r=2))  # ...then all pairs overlap
        else:  # else if temporal threshold less than half a cycle...
            tm_threshold_complementary = (  # ...get the complementary threshold
                    12 - tm_threshold) if tm_unit == 'moy' \
                else 365 - tm_threshold if tm_unit == 'doy' \
                else None
            pairs_list = []  # empty pairs list
            for pair in list(combinations(range(0, len(zs)), r=2)):  # for each possible pair
                za = zs[pair[0]]  # get the first z
                zb = zs[pair[1]]  # get the second z
                inner_diff = max(za, zb) - min(za, zb)  # get the inner difference between the zs
                if (inner_diff <= tm_threshold  # if the inner difference is less than the threshold or...
                        or inner_diff >= tm_threshold_complementary):  # more than the complementary...
                    pairs_list.append(pair)  # the pair is too close so append them
    else:  # else if temporal unit not recognised
        raise ValueError(' temporal unit not recognised.')
    return pairs_list


# get the location along the z axis (time) from the datetimes
#   (i.e., convert each datetime into an integer or float in the specified temporal units)
def get_zs(datetimes: list[datetime | pd.Timestamp], tm_unit: str = 'day'):
    date_min = pd.to_datetime('1970-01-01')  # set minimum date (does not matter when but 1970-01-01 is conventional)
    if tm_unit in ['year']:
        zs = [date.year for date in datetimes]  # year
    elif tm_unit in ['month']:
        zs = [(date.year - 1970) * 12 + date.month for date in datetimes]  # number of months since 1970-01-01
    elif tm_unit in ['moy']:
        zs = [date.month for date in datetimes]  # month of the year (1-12)
    elif tm_unit in ['day']:
        zs = [(date - date_min).days for date in datetimes]  # number of days since 1970-01-01
    elif tm_unit in ['doy']:
        zs = [min(365, int(date.strftime('%j'))) for date in datetimes]  # day of the year (1-365)
    elif tm_unit in ['hour']:
        zs = [(date - date_min).days * 24 + (date - date_min).seconds / 3600 for date in datetimes]  # hours
    else:
        raise ValueError
    return zs


def get_sptm_pairs(points: list[Point], sp_threshold: int | float,
                   datetimes: list[pd.Timestamp | datetime], tm_threshold: int | float, tm_unit: str = 'day') \
        -> list[tuple[int, int]]:
    sp_pairs_list = get_sp_pairs(  # get spatial pairs
        points=points,
        sp_threshold=sp_threshold)
    tm_pairs_list = get_tm_pairs(  # get temporal pairs
        datetimes=datetimes,
        tm_threshold=tm_threshold,
        tm_unit=tm_unit)
    pairs_list = list(set(sp_pairs_list) & set(tm_pairs_list))  # get spatiotemporal pairs
    return pairs_list


def selector(pairs: list[tuple[int, int]], no_reps: int = 100) -> list[int]:
    reps_list = []  # list for the results from each repetition
    for rep_no in range(int(no_reps)):  # for each repetition
        pairs_rep = pairs.copy()  # copy pairs indices
        remove_rep = []  # list for the indices to remove
        while pairs_rep:  # while there are pairs
            counts = Counter([index for pair in pairs_rep for index in pair])  # count how many pairs each index is in
            count_max = max(counts.values())  # maximum number of pairs that any index is in
            indices_max = [index for index, count in counts.items() if count == count_max]  # indices in maximum number
            index_remove = choice(indices_max)  # randomly select one of these indices and...
            remove_rep.append(index_remove)  # ...add it to the list of indices to remove
            pairs_rep = [pair for pair in pairs_rep if index_remove not in pair]  # remove pairs that include removed
        reps_list.append({'remove': remove_rep, 'count': len(remove_rep)})  # append removed and count to list

    reps = pd.DataFrame(reps_list)  # make a dataframe of repetitions
    removed_min = reps['count'].min()  # minimum number of indices that any repetition removed
    reps_min = reps[reps['count'] == removed_min]  # repetitions that removed the minimum number of indices
    rep_min = choice(reps_min.index.tolist())  # randomly select one of these repetitions...
    remove = reps.iloc[rep_min]['remove']  # ...and get the indices to be removed and...
    return remove  # ...return them


def remover(remove: list[int], df: pd.DataFrame = None, points: pd.Series | list[tuple[int, int], Point] = None,
            datetimes: pd.Series | list[str | pd.Timestamp | datetime] = None, ids: list[str | int | float] = None) \
        -> pd.DataFrame | tuple[list, list, list]:
    if isinstance(df, pd.DataFrame):  # if a DataFrame is specified, return the thinned DataFrame
        thinned_df = df.copy().reset_index(drop=True)  # copy the DataFrame
        thinned_df = thinned_df.loc[~df.index.isin(remove)]  # remove indices
        return thinned_df
    else:  # if a DataFrame is not specified
        thinned_points = [points[i] for i in range(len(points)) if i not in remove] \
            if (isinstance(points, list)) else None  # thinned points (if points provided)
        thinned_datetimes = [points[i] for i in range(len(datetimes)) if i not in remove] \
            if (isinstance(datetimes, list)) else None  # thinned datetimes (if datetimes provided)
        thinned_ids = [points[i] for i in range(len(ids)) if i not in remove] \
            if (isinstance(ids, list)) else None  # thinned ids (if ids provided)
        return thinned_points, thinned_datetimes, thinned_ids  # return the thinned points, datetimes, and ids
