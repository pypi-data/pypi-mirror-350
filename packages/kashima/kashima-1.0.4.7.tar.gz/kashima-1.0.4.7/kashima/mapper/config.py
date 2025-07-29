# file: config.py

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

EARTH_RADIUS_KM = 6371.0  # Earth's radius in kilometers

# ----------------------------------------------------------------
# Extended TILE_LAYERS dict to include OpenStreetMap, Stamen, etc.
# ----------------------------------------------------------------
TILE_LAYERS = {
    'ESRI_SATELLITE': 'Esri.WorldImagery',
    'OPEN_TOPO': 'OpenTopoMap',
    'ESRI_NATGEO': 'Esri.NatGeoWorldMap',
    'CYCL_OSM': 'CyclOSM',
    'CARTO_POSITRON': 'CartoDB positron',
    'CARTO_DARK': 'CartoDB dark_matter',
    'ESRI_STREETS': 'Esri.WorldStreetMap',
    'ESRI_TERRAIN': 'Esri.WorldTerrain',
    'ESRI_RELIEF': 'Esri.WorldShadedRelief',

    # Newly added recognized strings by Folium:
    'OPENSTREETMAP': 'OpenStreetMap',
    'STAMEN_TERRAIN': 'Stamen Terrain',
    'STAMEN_TONER': 'Stamen Toner',
    'CARTO_VOYAGER': 'CartoDB voyager'
}

# ----------------------------------------------------------------
# Each key -> a dict with 'tiles' (the actual Folium identifier or URL)
# and 'attr' for attribution
# ----------------------------------------------------------------
TILE_LAYER_CONFIGS = {
    TILE_LAYERS['ESRI_SATELLITE']: {
        'tiles': 'Esri.WorldImagery',
        'attr': 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, etc.'
    },
    TILE_LAYERS['OPEN_TOPO']: {
        'tiles': 'OpenTopoMap',
        'attr': 'Map data: © OpenStreetMap contributors, SRTM | Map style: © OpenTopoMap'
    },
    TILE_LAYERS['ESRI_NATGEO']: {
        'tiles': 'Esri.NatGeoWorldMap',
        'attr': 'Tiles &copy; Esri &mdash; National Geographic, Esri, DeLorme, NAVTEQ, etc.'
    },
    TILE_LAYERS['CYCL_OSM']: {
        'tiles': 'CyclOSM',
        'attr': '<a href="https://github.com/cyclosm/cyclosm-cartocss-style/releases">CyclOSM</a>'
    },
    TILE_LAYERS['CARTO_POSITRON']: {
        'tiles': 'CartoDB positron',
        'attr': '© CartoDB © OpenStreetMap contributors'
    },
    TILE_LAYERS['CARTO_DARK']: {
        'tiles': 'CartoDB dark_matter',
        'attr': '© CartoDB © OpenStreetMap contributors'
    },
    TILE_LAYERS['ESRI_STREETS']: {
        'tiles': 'Esri.WorldStreetMap',
        'attr': 'Tiles &copy; Esri &mdash; Source: Esri, DeLorme, NAVTEQ, etc.'
    },
    TILE_LAYERS['ESRI_TERRAIN']: {
        'tiles': 'Esri.WorldTerrain',
        'attr': 'Tiles &copy; Esri &mdash; Source: USGS, Esri, TANA, DeLorme, etc.'
    },
    TILE_LAYERS['ESRI_RELIEF']: {
        'tiles': 'Esri.WorldShadedRelief',
        'attr': 'Tiles &copy; Esri &mdash; Source: Esri'
    },

    # New layers
    TILE_LAYERS['OPENSTREETMAP']: {
        'tiles': 'OpenStreetMap',
        'attr': '© OpenStreetMap contributors'
    },
    TILE_LAYERS['STAMEN_TERRAIN']: {
        'tiles': 'Stamen Terrain',
        'attr': 'Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors'
    },
    TILE_LAYERS['STAMEN_TONER']: {
        'tiles': 'Stamen Toner',
        'attr': 'Map tiles by Stamen Design, CC BY 3.0 — Map data © OpenStreetMap contributors'
    },
    # Additional tile config
    TILE_LAYERS['CARTO_VOYAGER']: {
        'tiles': 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}.png',
        'attr': 'Map tiles by CartoDB, under CC BY 3.0. Data by OSM.'
    }
}

@dataclass
class MapConfig:
    project_name: str = 'Project Name'
    client: str = 'Client Name'
    latitude: float = 0.0
    longitude: float = 0.0
    radius_km: float = 2000
    base_zoom_level: int = 5
    max_zoom_level: int = 18
    min_zoom_level: int = 1
    epicentral_circles_title: str = 'Epicentral Distance'
    epicentral_circles: int = 10
    MIN_EPICENTRAL_CIRCLES: int = 5
    MAX_EPICENTRAL_CIRCLES: int = 25
    default_tile_layer: str = TILE_LAYERS['ESRI_SATELLITE']  # You can pick from the keys in TILE_LAYERS

    def __post_init__(self):
        if self.default_tile_layer not in TILE_LAYER_CONFIGS:
            logger.warning(f"Invalid tile layer '{self.default_tile_layer}'. Using 'Esri.WorldImagery'")
            self.default_tile_layer = 'Esri.WorldImagery'

        if self.epicentral_circles < self.MIN_EPICENTRAL_CIRCLES:
            logger.warning(f"epicentral_circles < {self.MIN_EPICENTRAL_CIRCLES}, forcing to {self.MIN_EPICENTRAL_CIRCLES}")
            self.epicentral_circles = self.MIN_EPICENTRAL_CIRCLES
        elif self.epicentral_circles > self.MAX_EPICENTRAL_CIRCLES:
            logger.warning(f"epicentral_circles > {self.MAX_EPICENTRAL_CIRCLES}, forcing to {self.MAX_EPICENTRAL_CIRCLES}")
            self.epicentral_circles = self.MAX_EPICENTRAL_CIRCLES

@dataclass
class EventConfig:
    event_file_path: str = ''
    vmin: float = None
    vmax: float = None
    color_palette: str = 'magma'
    color_reversed: bool = True
    scaling_factor: float = 4
    legend_position: str = 'bottomright'
    legend_title: str = 'Magnitude'
    heatmap_radius: int = 25
    heatmap_blur: int = 15
    heatmap_min_opacity: float = 0.5
    event_radius_multiplier: float = 1.0

@dataclass
class FaultConfig:
    include_faults: bool = False
    faults_gem_file_path: str = ''
    regional_faults_color: str = 'darkblue'
    regional_faults_weight: int = 3
    coordinate_system: str = 'EPSG:4326'

@dataclass
class StationConfig:
    station_file_path: str = ''
    coordinate_system: str = 'EPSG:4326'
    layer_title: str = 'Seismic Stations'

@dataclass
class BlastConfig:
    blast_file_path: str = ''
    coordinate_system: str = 'EPSG:32722'
    f_TNT: float = 0.90
    a_ML: float = 0.75
    b_ML: float = -1.0

__version__ = "1.0.1.7"