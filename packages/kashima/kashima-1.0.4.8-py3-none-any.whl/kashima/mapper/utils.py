# file: utils.py

import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import Transformer, CRS

EARTH_RADIUS_KM = 6371.0  # Earth's radius in kilometers

def calculate_zoom_level(radius_km):
    """
    Calculate an appropriate zoom level based on the radius in kilometers.
    """
    max_zoom = 18
    zoom_level = int(max_zoom - np.log2(radius_km / 500))
    return max(min(zoom_level, max_zoom), 1)

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth surface.
    lat1, lon1, lat2, lon2 in decimal degrees.
    Returns distance in kilometers.
    """
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    return EARTH_RADIUS_KM * c

def convert_xy_to_latlon(x, y, source_crs='EPSG:32722', target_crs='EPSG:4326'):
    """
    Convert arrays/lists of X, Y coordinates to longitude and latitude 
    via pyproj Transformer.
    """
    transformer = Transformer.from_crs(
        CRS.from_user_input(source_crs),
        CRS.from_user_input(target_crs),
        always_xy=True
    )
    lon, lat = transformer.transform(x, y)
    return lon, lat

def calculate_magnitude(Q, f_TNT, a_ML, b_ML):
    """
    Calculate a magnitude from explosive charge (Q),
    given TNT equivalence factor f_TNT, 
    and magnitude formula constants a_ML, b_ML.
    """
    Q_TNT = Q * f_TNT
    return a_ML * np.log10(Q_TNT) + b_ML

def calculate_distances_vectorized(
    events_df, 
    center_lat, 
    center_lon, 
    lat_col='latitude', 
    lon_col='longitude', 
    out_col='Repi'
):
    """
    Vectorized calculation of distance from a center point (center_lat, center_lon)
    to each row's lat/lon in events_df. Stores the result in events_df[out_col].
    """
    lat1_rad = np.radians(center_lat)
    lon1_rad = np.radians(center_lon)

    lat2_rad = np.radians(events_df[lat_col].values)
    lon2_rad = np.radians(events_df[lon_col].values)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))

    dist_km = EARTH_RADIUS_KM * c
    events_df[out_col] = dist_km

def load_faults(faults_gem_file_path, coordinate_system='EPSG:4326'):
    """
    Load fault lines from a GeoJSON/shape file, transform to EPSG:4326 if needed,
    return a GeoDataFrame.
    """
    try:
        gdf = gpd.read_file(faults_gem_file_path)
    except Exception as e:
        raise IOError(f"Cannot read faults file {faults_gem_file_path}: {e}")

    # Check if we need to reproject
    if coordinate_system:
        try:
            gdf = gdf.to_crs('EPSG:4326')
        except Exception as e:
            raise ValueError(f"Failed to transform fault geometries to WGS84: {e}")

    return gdf

def load_stations_csv(station_file_path, station_crs='EPSG:4326'):
    """
    Load station data from CSV, do XY->lat/lon if needed.
    Returns a pandas DataFrame with 'latitude', 'longitude', plus other columns.
    """
    try:
        stations_df = pd.read_csv(station_file_path)
    except Exception as e:
        raise IOError(f"Could not read station file {station_file_path}: {e}")

    # We assume columns 'x', 'y' if we need to convert. If 'latitude'/'longitude' exist, skip
    if 'latitude' not in stations_df.columns or 'longitude' not in stations_df.columns:
        if 'x' in stations_df.columns and 'y' in stations_df.columns:
            lon, lat = convert_xy_to_latlon(
                stations_df['x'].values,
                stations_df['y'].values,
                source_crs=station_crs,
                target_crs='EPSG:4326'
            )
            stations_df['latitude'] = lat
            stations_df['longitude'] = lon
        else:
            raise ValueError("No latitude/longitude or x,y columns found in station CSV.")
    return stations_df