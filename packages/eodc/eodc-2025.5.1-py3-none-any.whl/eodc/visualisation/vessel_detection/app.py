import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash import ALL, Dash, Input, Output, State, callback_context, dcc, html, no_update

from eodc.visualisation.vessel_detection.navbar import navbar


def get_info(target_row=None, title_string="", info_string=""):
    header = [html.H4(title_string)]
    if isinstance(target_row, type(None)):
        return header + [html.P(info_string)]
    mmsi = target_row["MMSI"]
    return header + [
        dcc.Markdown(
            f"""
                        | MMSI  || TIMESTAMP  |
                        |---|---|---|
                        | {mmsi} || {target_row['TIMESTAMP_UTC']} |
                        |   |   ||
                    """
        )
    ]


info = html.Div(
    children=get_info(
        title_string="OpenEO Vessel",
        info_string="Click on a polygon from an OpenEO layer",
    ),
    id="info",
    className="info",
    style={"position": "absolute", "top": "10%", "right": "10px", "zIndex": "1000"},
)

vessel_info = html.Div(
    children=get_info(
        title_string="PyGeoApi Vessel",
        info_string="Click on a pointer from an PyGeoApi layer",
    ),
    id="pygeoapi-info",
    className="info",
    style={"position": "absolute", "top": "25%", "right": "10px", "zIndex": "1000"},
)

app_layout = dbc.Container(
    [
        dbc.Col(
            [
                dbc.Row(
                    [
                        navbar(),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Card(
                            id="toaster",
                            style={"z-index": 999},
                        ),
                        dl.Map(
                            dl.LayersControl(
                                [
                                    dl.TileLayer(),
                                    dl.FeatureGroup(
                                        [
                                            dl.EditControl(
                                                id="edit_control", position="topleft"
                                            )
                                        ]
                                    ),
                                    info,
                                    vessel_info,
                                ],
                                id="map-layers",
                            ),
                            center=[44, 13],
                            zoom=10,
                            style={"height": "100vh", "z-index": 100},
                            id="map",
                        ),
                    ]
                ),
            ]
        )
    ],
    id="main-app",
    fluid=True,
)


app = Dash(
    "EODC Dashboard",
    title="EODC Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    assets_folder="/vessel_detection/vessel-detection/viz/assets",
)


@app.callback(
    [
        Output("vessels-date-picker", "min_date_allowed"),
        Output("vessels-date-picker", "max_date_allowed"),
    ],
    Input("openeo-query-item", "on"),
    State("openeo-url-input", "value"),
    prevent_initial_call=True,
)
def update_output(on, canonical_url):
    from datetime import date

    from eodc.visualisation.vessel_detection.utils import get_openeo_item_collection

    if on:
        item_collection = get_openeo_item_collection(canonical_url)

        _min = item_collection.items[0].datetime
        _max = item_collection.items[0].datetime

        for item in item_collection.items:
            if item.datetime < _min:
                _min = item.datetime
            if item.datetime > _max:
                _max = item.datetime

        return _min, _max
    return date(2017, 1, 1), date(2023, 12, 31)


app.layout = app_layout


## VESSELS
@app.callback(
    Output("offcanvas", "is_open"),
    Input("sidebar-toggle", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(
    [Output("collapse", "is_open"), Output("vessels-collapse-icon", "className")],
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        open = not is_open
        if open:
            return open, "fa-solid fa-arrow-up"
        else:
            return open, "fa-solid fa-arrow-down"
    return False, "fa-solid fa-arrow-down"


@app.callback(
    Output("map-layers", "children"),
    Input("vessels-layer-add-button", "n_clicks"),
    State("map", "bounds"),
    State("vessels-date-picker", "date"),
    State("vessels-start-time", "value"),
    State("vessels-end-time", "value"),
    State("map-layers", "children"),
    prevent_initial_call=True,
)
def add_vessel_layer(n, bounds, date, stime, etime, map_layers):
    from eodc.visualisation.vessel_detection.utils import pygeoapi_time_request

    flattened_bounds = [item for bound in bounds for item in bound]
    flattened_bounds = [bounds[0][1], bounds[0][0], bounds[1][1], bounds[1][0]]

    features = pygeoapi_time_request(flattened_bounds, date, stime, etime)

    if not features:
        return map_layers

    new_layer = [
        dl.Overlay(
            dl.GeoJSON(
                url=features, cluster=False, id={"type": "pygeoapi-layer", "index": n}
            ),
            name=f"Marine Traffic Overlay: {date}T{stime}Z",
            checked=True,
        )
    ]

    map_layers = map_layers + new_layer

    return map_layers


@app.callback(
    Output("pygeoapi-info", "children", allow_duplicate=True),
    Input({"type": "pygeoapi-layer", "index": ALL}, "clickData"),
    State("map-layers", "children"),
    prevent_initial_call=True,
)
def display_output(values, children):
    if not children:
        children = []

    tigger = callback_context.triggered[0]

    if tigger["value"]:
        data = values[0]

        return get_info(data["properties"], title_string="PyGeoApi Vessel")
    return no_update


## OPENEO
@app.callback(
    [Output("openeo-collapse", "is_open"), Output("openeo-collapse-icon", "className")],
    [Input("openeo-collapse-button", "n_clicks")],
    [State("openeo-collapse", "is_open")],
)
def openeo_toggle_collapse(n, is_open):
    if n:
        open = not is_open
        if open:
            return open, "fa-solid fa-arrow-up"
        else:
            return open, "fa-solid fa-arrow-down"
    return False, "fa-solid fa-arrow-down"


@app.callback(
    Output("openeo-job-items", "options"),
    Input("openeo-url-button", "n_clicks"),
    State("openeo-url-input", "value"),
    prevent_initial_call=True,
)
def set_openeo_item_options(n, canonical_url):
    from eodc.visualisation.vessel_detection.utils import get_openeo_item_collection

    item_collection = get_openeo_item_collection(canonical_url)

    options = [item.id for item in item_collection.items]

    return options


@app.callback(
    [
        Output("map-layers", "children", allow_duplicate=True),
    ],
    [Input("openeo-item-preview", "n_clicks")],
    [State("openeo-url-input", "value"), State("map-layers", "children")],
    prevent_initial_call=True,
)
def set_openeo_items(n, canonical_url, map_layers):
    if n:
        from requests import get

        if not canonical_url:
            return no_update

        if not map_layers:
            return no_update

        job_results = get(canonical_url).json()
        job_id = job_results["id"]

        items_link = {
            link["rel"]: link["href"]
            for link in job_results["links"]
            if link["rel"] in ["items", "canonical"]
        }

        new_layer = [
            dl.Overlay(
                dl.GeoJSON(
                    url=items_link["items"],
                    cluster=False,
                    id={"type": "openeo-items", "index": n},
                ),
                name=f"OpenEO Job: {job_id}",
                checked=True,
            )
        ]

        map_layers = map_layers + new_layer

        return [map_layers]
    return no_update


@app.callback(
    Output("openeo-item-assets", "options"),
    [Input("openeo-job-items", "value")],
    [State("openeo-url-input", "value")],
    prevent_initial_call=True,
)
def set_item_assets(item_id, canonical_url):
    from eodc.visualisation.vessel_detection.utils import get_openeo_item_collection

    item_collection = get_openeo_item_collection(canonical_url)

    matching_item = next(
        (item for item in item_collection.items if item.id == item_id), None
    )

    options = [asset for asset in matching_item.assets]

    return options


# TODO SLIDER CALLBACK
@app.callback(
    [
        Output("openeo-asset-date-slider", "min"),
        Output("openeo-asset-date-slider", "max"),
        Output("openeo-asset-date-slider", "marks"),
        Output("openeo-asset-date-slider", "value"),
        Output("openeo-asset-date-slider", "disabled"),
        Output("openeo-asset-store", "data"),
    ],
    [Input("openeo-item-assets", "value")],
    [State("openeo-job-items", "value"), State("openeo-url-input", "value")],
    prevent_initial_call=True,
)
def set_slider_range(asset_title, item_id, canonical_url):
    from eodc.visualisation.vessel_detection.utils import get_openeo_item_collection

    if "raster" in asset_title:
        return no_update

    item_collection = get_openeo_item_collection(canonical_url)

    matching_asset = next(
        (
            item.assets[asset]
            for item in item_collection.items
            if item.id == item_id
            for asset in item.assets
            if asset == asset_title
        ),
        None,
    )

    import geopandas as gpd

    data = gpd.GeoDataFrame.from_file(matching_asset.href)

    if "datetime" not in data.columns:
        return no_update

    dates = []
    for row in data.datetime:
        tmp = row.to_pydatetime()
        if tmp not in dates:
            dates.append(tmp)

    marks = {
        date.strftime("%Y-%m-%dT%H:%M:%SZ"): {"label": date.strftime("%d H:%H")}
        for date in dates
    }

    data["datetime"] = data["datetime"].astype(str)
    store_data = {"data": data.to_json(), "dates": dates}

    return 1, len(marks.keys()), marks, 1, False, store_data


@app.callback(
    Output("map-layers", "children", allow_duplicate=True),
    [Input("openeo-asset-add", "n_clicks")],
    [
        State("openeo-item-assets", "value"),
        State("openeo-job-items", "value"),
        State("openeo-url-input", "value"),
        State("map-layers", "children"),
        State("openeo-asset-store", "data"),
        State("openeo-asset-date-slider", "value"),
    ],
    prevent_initial_call=True,
)
def render_item(n, asset_title, item_id, canonical_url, map_layers, data, date):
    if n:
        import json

        import geopandas as gpd
        import httpx

        from eodc.visualisation.vessel_detection.utils import get_openeo_item_collection

        if "vector" in asset_title:
            if "data" not in data:
                item_collection = get_openeo_item_collection(canonical_url)

                matching_asset = next(
                    (
                        item.assets[asset]
                        for item in item_collection.items
                        if item.id == item_id
                        for asset in item.assets
                        if asset == asset_title
                    ),
                    None,
                )
                data_layer = dl.GeoJSON(
                    url=matching_asset.href,
                    cluster=False,
                    id={"type": "openeo-asset-layer", "index": n},
                )
                layer_name = f"{item_id}: {asset_title}"
            else:
                date -= 1

                new_data = gpd.GeoDataFrame.from_features(json.loads(data["data"]))
                # Really ugly. Filter dates out of geojson,
                # and then convert back to json, and load
                # into dict repalce T in string for dataframe filter
                to_render = json.loads(
                    new_data[
                        (
                            new_data["datetime"]
                            == str(data["dates"][date]).replace("T", " ")[:-3]
                        )
                    ].to_json()
                )
                layer_name = (
                    f"{item_id}: {asset_title}: {str(data['dates'][date])[:-3]}"
                )

                data_layer = dl.GeoJSON(
                    data=to_render,
                    cluster=False,
                    id={"type": "openeo-asset-layer", "index": n},
                )
        else:
            item_collection = get_openeo_item_collection(canonical_url)

            matching_asset = next(
                (
                    item.assets[asset]
                    for item in item_collection.items
                    if item.id == item_id
                    for asset in item.assets
                    if asset == asset_title
                ),
                None,
            )

            titiler_endpoint = "https://titiler.xyz"
            r = httpx.get(
                f"{titiler_endpoint}/cog/tilejson.json",
                params={"url": matching_asset.href, "rescale": "0,255"},
            ).json()

            data_layer = dl.TileLayer(
                url=r["tiles"][0], id={"type": "openeo-asset-layer", "index": n}
            )

            layer_name = f"{item_id}: {asset_title}"

        new_layer = [dl.Overlay(data_layer, name=layer_name, checked=True)]

        map_layers = map_layers + new_layer

        return map_layers
    return no_update


@app.callback(
    Output("info", "children"),
    Input({"type": "openeo-asset-layer", "index": ALL}, "clickData"),
    [
        State("map-layers", "children"),
        State("openeo-url-input", "value"),
        State("openeo-job-items", "value"),
    ],
    prevent_initial_call=True,
)
def openeo_display_output(values, children, canonical_url, item_id):
    from shapely.geometry import shape

    from eodc.visualisation.vessel_detection.utils import (
        get_openeo_item_collection,
        pygeoapi_from_item,
    )

    if not children:
        children = []

    trigger = callback_context.triggered[0]

    if trigger["value"]:
        data = values[-1]

        clicked_polygon = shape(data["geometry"])
        item_collection = get_openeo_item_collection(canonical_url)

        matching_item = next(
            (item for item in item_collection.items if item.id == item_id), None
        )

        current_vessels = pygeoapi_from_item(
            matching_item, data["properties"]["datetime"], True
        )

        polygon_index = current_vessels.distance(clicked_polygon).sort_values().index[0]

        target_row = current_vessels.loc[polygon_index]

        return get_info(target_row, title_string="OpenEO Vessel")
    return no_update


if __name__ == "__main__":
    app.run(debug=True)
