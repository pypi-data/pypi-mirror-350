#!/usr/bin/env python

import logging
import os

from kashima.mapper import (
    MapConfig, EventConfig, FaultConfig, EventMap, USGSCatalog
)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# 1) Download all global events if not present
usgs_path = 'data/usgs.csv'
if not os.path.exists(usgs_path):
    catalog = USGSCatalog()
    events = catalog.get_events(event_type='earthquake')
    events.to_csv(usgs_path, index=False)
    logger.info(f"USGS events saved to {usgs_path}")

# 2) MapConfig
map_config = MapConfig(
    project_name='Johannesburg',
    client='SRK',
    latitude=-26.195246,
    longitude=28.034088,
    radius_km=7000,
    epicentral_circles_title='Epicentral Distance',
    epicentral_circles=5,    # e.g., 5 circles
    base_zoom_level=3,
    min_zoom_level=3,
    max_zoom_level=15,
    default_tile_layer='Esri.WorldImagery'
)

# 3) EventConfig
event_config = EventConfig(
    vmin=4.5,
    vmax=9.0,
    color_palette='magma',
    color_reversed=True,
    scaling_factor=1.0,
    legend_position='bottomright',
    legend_title='Magnitude (Mw)',
    heatmap_radius=20,
    heatmap_blur=15,
    heatmap_min_opacity=0.5,
    event_radius_multiplier=1.0
)

# 4) Optional FaultConfig
fault_config = FaultConfig(
    include_faults=True,
    faults_gem_file_path='data/gem_active_faults_harmonized.geojson',
    regional_faults_color='darkgreen',
    regional_faults_weight=4
)

# 5) Create EventMap
event_map = EventMap(
    map_config=map_config,
    event_config=event_config,
    events_csv=usgs_path,
    legend_csv=None,            # or 'data/my_legend.csv'
    mandatory_mag_col='mag',
    calculate_distance=True,
    fault_config=fault_config,
    show_distance_in_tooltip=True  # We do want Repi in tooltips
)

# 6) Load data & build
event_map.load_data()
map_object = event_map.get_map()

# 7) Save the map
os.makedirs('output', exist_ok=True)
map_html = 'output/index.html'
map_object.save(map_html)
logger.info(f"Map saved to {map_html}")

# 8) Save final events without monkey-patching
epicenters = event_map.events_df  # direct reference to the final DF
epicenters_path = 'output/epicenters.csv'
epicenters.to_csv(epicenters_path, index=False)
logger.info(f"Epicenters saved to {epicenters_path}")

