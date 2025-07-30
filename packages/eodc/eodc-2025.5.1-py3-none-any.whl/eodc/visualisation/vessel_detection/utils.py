import datetime
import re

import geopandas as gpd
import requests
from owslib.ogcapi.features import Features
from pystac import ItemCollection


def time_from_id(_id: str):
    """Return datetime for stac item from Sentinel 1 ID."""
    time_re = r"[0-9]{8}T[0-9]{6}"

    time_string = re.search(time_re, _id).group()
    return datetime.datetime.strptime(time_string, "%Y%m%dT%H%M%S")


def pygeoapi_from_item(item, input_datetime, return_features=False):
    """Make request to pygeoapi vessels collection."""

    start_time = datetime.datetime.strptime(input_datetime[:-4], "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(input_datetime[:-4], "%Y-%m-%d %H:%M:%S")

    diff = end_time - start_time
    if diff.total_seconds() < 1800:
        start_time = start_time - datetime.timedelta(minutes=15)
        end_time = end_time + datetime.timedelta(minutes=15)

    str_start_time = datetime.datetime.strftime(start_time, "%Y-%m-%dT%H:%M:%S")
    str_end_time = datetime.datetime.strftime(end_time, "%Y-%m-%dT%H:%M:%S")

    EODC_OGCAPI_URL = "https://features.dev.services.eodc.eu/"
    eodc_ogcapi = Features(EODC_OGCAPI_URL)
    cql_filter_before = f"TIMESTAMP_UTC AFTER {str_start_time}Z"
    filter_after = f"AND TIMESTAMP_UTC BEFORE {str_end_time}Z"

    cql_filter = cql_filter_before + filter_after
    # get all items in the yipeeo_yield_fl collection
    features = eodc_ogcapi.collection_items(
        "adriatic_vessels", bbox=item.bbox, limit=2000, filter=cql_filter
    )
    if not features["features"]:
        return

    if return_features:
        return gpd.GeoDataFrame.from_features(features["features"])

    self_href = [link for link in features["links"] if link["rel"] == "self"][0]["href"]
    return self_href


def pygeoapi_time_request(bbox, date, stime, etime):
    """Make request to pygeoapi vessels collection."""

    EODC_OGCAPI_URL = "https://features.dev.services.eodc.eu/"

    eodc_ogcapi = Features(EODC_OGCAPI_URL)

    cql_filter = (
        f"TIMESTAMP_UTC AFTER {date}T{stime}Z AND TIMESTAMP_UTC BEFORE {date}T{etime}Z"
    )

    # get all items in the yipeeo_yield_fl collection
    features = eodc_ogcapi.collection_items(
        "adriatic_vessels", bbox=bbox, limit=2000, filter=cql_filter
    )
    if not features["features"]:
        return

    self_href = [link for link in features["links"] if link["rel"] == "self"][0]["href"]
    return self_href


def get_openeo_item_collection(canon_url: str):
    """Get item collection from openeo job results."""
    job_results = requests.get(canon_url)

    job_links = job_results.json()["links"]

    items_link = {
        link["rel"]: link["href"]
        for link in job_links
        if link["rel"] in ["items", "canonical"]
    }

    result_item_collection = ItemCollection.from_file(items_link["items"])
    return result_item_collection
