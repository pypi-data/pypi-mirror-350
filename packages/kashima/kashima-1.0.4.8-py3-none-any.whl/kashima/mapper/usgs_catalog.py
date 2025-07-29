import pandas as pd
import requests
import logging
import random
import time
from datetime import datetime, timedelta
from io import StringIO

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class USGSCatalog:
    """Class for fetching earthquake events from the USGS API."""
    def __init__(
        self,
        min_magnitude=4.5,
        verbose=True,
        url="https://earthquake.usgs.gov/fdsnws/event/1/query",
        timeout=30
    ):
        self.min_magnitude = min_magnitude
        self.verbose = verbose
        self.url = url
        self.timeout = timeout
        self.dataframe = None

    def get_events(
        self,
        start_date: datetime = None,
        end_date: datetime = None,
        min_latitude: float = None,
        max_latitude: float = None,
        min_longitude: float = None,
        max_longitude: float = None,
        latitude: float = None,
        longitude: float = None,
        maxradiuskm: float = None,
        min_depth: float = None,
        max_depth: float = None,
        min_magnitude: float = None,
        max_magnitude: float = None,
        magnitude_type: str = None,
        event_type: str = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Download earthquake data from the USGS API.

        Parameters:
            start_date (datetime, optional): Start date.
            end_date (datetime, optional): End date.
            min_latitude (float, optional): Minimum latitude.
            max_latitude (float, optional): Maximum latitude.
            min_longitude (float, optional): Minimum longitude.
            max_longitude (float, optional): Maximum longitude.
            latitude (float, optional): Central latitude for radial search.
            longitude (float, optional): Central longitude for radial search.
            maxradiuskm (float, optional): Maximum distance from center point in km.
            min_depth (float, optional): Minimum depth.
            max_depth (float, optional): Maximum depth.
            min_magnitude (float, optional): Minimum magnitude.
            max_magnitude (float, optional): Maximum magnitude.
            magnitude_type (str, optional): Type of magnitude (e.g., 'mb', 'ms', 'mw').
            event_type (str, optional): Type of event (e.g., 'earthquake').

        Returns:
            pd.DataFrame: Compiled earthquake data, also stored in self.dataframe.
        """
        if start_date is None:
            start_date = datetime(1800, 1, 1)
        if end_date is None:
            end_date = datetime.now()

        if start_date >= end_date:
            logger.error("Start date must be before end date.")
            return None

        all_data = []
        max_events = 20000
        delta_days = 700  # Initial estimate of days per interval
        current_date = start_date

        if self.verbose:
            logger.info("Starting data download...")

        # Adjust logger level
        if self.verbose:
            logger.setLevel(logging.INFO)
        else:
            logger.setLevel(logging.WARNING)

        while current_date < end_date:
            interval_end = current_date + timedelta(days=delta_days)
            if interval_end > end_date:
                interval_end = end_date

            retry = True
            retries = 0
            max_retries = 5

            while retry and retries < max_retries:
                # Construct API request
                params = {
                    "format": "csv",
                    "orderby": "time-asc",
                    "limit": max_events  # To ensure we don't exceed the maximum
                }

                # Add time parameters
                params["starttime"] = current_date.strftime("%Y-%m-%d")
                params["endtime"] = interval_end.strftime("%Y-%m-%d")

                # Add magnitude parameters
                params["minmagnitude"] = min_magnitude if min_magnitude is not None else self.min_magnitude
                if max_magnitude is not None:
                    params["maxmagnitude"] = max_magnitude

                # Add depth parameters
                if min_depth is not None:
                    params["mindepth"] = min_depth
                if max_depth is not None:
                    params["maxdepth"] = max_depth

                # Add geographic parameters
                if min_latitude is not None:
                    params["minlatitude"] = min_latitude
                if max_latitude is not None:
                    params["maxlatitude"] = max_latitude
                if min_longitude is not None:
                    params["minlongitude"] = min_longitude
                if max_longitude is not None:
                    params["maxlongitude"] = max_longitude
                if latitude is not None and longitude is not None and maxradiuskm is not None:
                    params["latitude"] = latitude
                    params["longitude"] = longitude
                    params["maxradiuskm"] = maxradiuskm

                # Add magnitude type
                if magnitude_type is not None:
                    params["magnitudetype"] = magnitude_type

                # Add event type
                if event_type is not None:
                    params["eventtype"] = event_type

                # Update params with any additional kwargs
                params.update(kwargs)

                if self.verbose:
                    logger.info(f"Requesting data from {current_date.date()} to {interval_end.date()}...")

                try:
                    response = requests.get(self.url, params=params, timeout=self.timeout)
                    response.raise_for_status()
                    df = pd.read_csv(StringIO(response.text))
                    event_count = len(df)
                    if self.verbose:
                        logger.info(f"Retrieved {event_count} events.")
                    if event_count >= max_events:
                        # Interval too large, split further
                        delta_days = max(1, delta_days // 2)
                        if self.verbose:
                            logger.info(f"Too many events. Reducing interval to {delta_days} days.")
                    else:
                        all_data.append(df)
                        # Increase interval if event count is less than half of max_events
                        if event_count < max_events / 2 and delta_days < 700:
                            delta_days = min(700, delta_days * 2)
                        retry = False
                except requests.exceptions.RequestException as e:
                    retries += 1
                    backoff_time = random.uniform(1, 3) * (2 ** retries)
                    logger.error(f"Request failed ({retries}/{max_retries}): {e}. Retrying in {backoff_time:.2f} seconds...")
                    time.sleep(backoff_time)
                except pd.errors.EmptyDataError:
                    logger.warning("No data returned for this interval.")
                    retry = False
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 429:
                        # Handle rate limiting
                        backoff_time = int(e.response.headers.get("Retry-After", 60))
                        logger.error(f"Rate limit exceeded. Retrying after {backoff_time} seconds...")
                        time.sleep(backoff_time)
                        retries += 1
                    else:
                        retries += 1
                        logger.error(f"HTTP error occurred: {e}. Retrying...")

            if retries >= max_retries:
                logger.error("Max retries reached. Exiting data download.")
                break

            current_date = interval_end

        # Before concatenating, filter out empty or all-NA DataFrames
        non_empty_dfs = [df for df in all_data if not df.empty and not df.isna().all().all()]

        # Proceed with concatenation if there are valid DataFrames
        if non_empty_dfs:
            # Align DataFrames by specifying columns
            common_columns = list(set.intersection(*(set(df.columns) for df in non_empty_dfs)))
            self.dataframe = pd.concat(non_empty_dfs, ignore_index=True)[common_columns]
            if not self.dataframe.empty:
                self.dataframe.drop_duplicates(subset='id', inplace=True)
        else:
            self.dataframe = pd.DataFrame()  # Handle the case when no data is available
            logger.warning("No data was downloaded.")

        return self.dataframe
