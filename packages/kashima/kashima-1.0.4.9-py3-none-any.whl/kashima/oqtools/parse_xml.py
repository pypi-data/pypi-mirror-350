# kashima/kashima/oqtools/parse_xml.py

import os
import logging
import xml.etree.ElementTree as ET
from shapely.geometry import Point, Polygon

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParseXML:
    @staticmethod
    def locate_point(file_path, lat, lon):
        """
        Check if a point (lat, lon) is contained within *any* polygon
        in the specified XML file (a single file).
        
        Returns the file name if the point is inside a polygon;
        otherwise returns None.
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            ns = {'gml': 'http://www.opengis.net/gml'}

            for polygon in root.findall('.//gml:Polygon', ns):
                pos_list = polygon.find('.//gml:posList', ns)
                if pos_list is not None and pos_list.text:
                    coords = list(map(float, pos_list.text.strip().split()))
                    points = [(coords[i], coords[i+1])
                              for i in range(0, len(coords), 2)]
                    
                    poly = Polygon(points)
                    point = Point(lon, lat)
                    
                    if poly.contains(point):
                        logger.info(f"✅ Point ({lat}, {lon}) found in {os.path.basename(file_path)}")
                        return os.path.basename(file_path)

            logger.info(f"⚠️ Point ({lat}, {lon}) not found in any region of {file_path}")
            return None

        except Exception as e:
            logger.error(f"❌ Error parsing {file_path}: {e}")
            return None

    @staticmethod
    def parse_polygons_from_file(file_path):
        """
        Parse all polygons from a single XML file and return a list of
        (Polygon, filename) tuples.
        """
        polygons = []
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            ns = {'gml': 'http://www.opengis.net/gml'}

            for polygon in root.findall('.//gml:Polygon', ns):
                pos_list = polygon.find('.//gml:posList', ns)
                if pos_list is not None and pos_list.text:
                    coords = list(map(float, pos_list.text.strip().split()))
                    points = [(coords[i], coords[i+1])
                              for i in range(0, len(coords), 2)]
                    if len(points) >= 3:
                        polygons.append((Polygon(points), os.path.basename(file_path)))

            logger.info(f"Parsed {len(polygons)} polygon(s) from {file_path}")
        except Exception as e:
            logger.error(f"Failed to parse {file_path}: {e}")
        return polygons

    @staticmethod
    def load_all_regions_from_folder(folder_path):
        """
        Parse polygons from all *.xml files in a folder.
        Return a list of (Polygon, filename) tuples for *all* polygons
        from all files in that folder.
        """
        if not os.path.exists(folder_path):
            logger.error(f"Folder {folder_path} does not exist!")
            return []

        all_polygons = []
        for file_name in os.listdir(folder_path):
            if file_name.lower().endswith('.xml'):
                full_path = os.path.join(folder_path, file_name)
                polygons = ParseXML.parse_polygons_from_file(full_path)
                all_polygons.extend(polygons)

        logger.info(f"Total polygons loaded from all files: {len(all_polygons)}")
        return all_polygons

    @staticmethod
    def find_region_for_site(lat, lon, polygons):
        """
        Given a point (lat, lon) and a list of (Polygon, filename) tuples,
        return the *first* filename whose Polygon contains the point.

        If no polygon contains the point, return None.
        """
        point = Point(lon, lat)
        for polygon, file_name in polygons:
            if polygon.contains(point):
                logger.info(f"Point ({lat}, {lon}) found in {file_name}")
                return file_name
        logger.warning("No region found for this site!")
        return None
