import dash_bootstrap_components as dbc
from dash import dcc, html

from eodc.visualisation.vessel_detection.cards import PYGEOAPI_VESSEL_CARD


def openeo_collapse():
    return dbc.Collapse(
        [
            html.Div(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    "Canonical URL: ",
                                    dcc.Input(
                                        id="openeo-url-input",
                                        placeholder="input url",
                                        style={"width": "75%"},
                                    ),
                                    dbc.Button(
                                        id="openeo-url-button",
                                        style={
                                            "width": "15%",
                                            "margin-left": "5%",
                                        },
                                        className="fa-solid fa-arrow-right",
                                    ),
                                ],
                                style={"padding-top": "1vh"},
                            ),
                            dbc.Row(
                                dbc.Button(
                                    "Preview",
                                    id="openeo-item-preview",
                                ),
                                style={"padding-top": "1vh"},
                            ),
                            dbc.Row(
                                [
                                    "Items: ",
                                    dcc.Dropdown(
                                        placeholder="No canonical url supplied",
                                        id="openeo-job-items",
                                    ),
                                ],
                                style={"padding-top": "1vh"},
                            ),
                            dbc.Row(
                                [
                                    "Item Assets: ",
                                    dcc.Dropdown(
                                        placeholder="No asset selected",
                                        id="openeo-item-assets",
                                    ),
                                    dcc.Store(
                                        id="openeo-asset-store", storage_type="memory"
                                    ),
                                ],
                                style={"padding-top": "1vh"},
                            ),
                            dbc.Row(
                                [
                                    dcc.Slider(
                                        id="openeo-asset-date-slider",
                                        disabled=True,
                                        min=1,
                                        max=2,
                                        step=1,
                                        included=False,
                                    )
                                ],
                                style={"padding-top": "1vh"},
                            ),
                            dbc.Row(
                                [
                                    dbc.Button(
                                        "Add",
                                        id="openeo-asset-add",
                                    )
                                ],
                                style={"padding-top": "1vh"},
                            ),
                        ]
                    )
                ],
                style={
                    "width": "90%",
                    "margin-left": "5%",
                },
            )
        ],
        id="openeo-collapse",
        is_open=False,
    )


def navbar():
    comp = dbc.Navbar(
        dbc.Container(
            [
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Button(
                                    html.I(className="fa-solid fa-layer-group"),
                                    n_clicks=0,
                                    id="sidebar-toggle",
                                ),
                                dbc.Offcanvas(
                                    [
                                        html.Div(
                                            dbc.Button(
                                                [
                                                    html.H4(
                                                        "OpenEO Job",
                                                        style={"padding-top": "2vh"},
                                                    ),
                                                    html.I(
                                                        style={
                                                            "display": "block",
                                                            "padding-top": "2vh",
                                                            "padding-bottom": "2vh",
                                                        },
                                                        id="openeo-collapse-icon",
                                                    ),
                                                ],
                                                id="openeo-collapse-button",
                                                color="dark",
                                                outline=True,
                                                n_clicks=0,
                                            ),
                                            className="d-grid gap-2",
                                            style={"margin-top": "5vh"},
                                        ),
                                        openeo_collapse(),
                                        html.Div(
                                            dbc.Button(
                                                [
                                                    html.H4(
                                                        "Adriatic Vessels",
                                                        style={"padding-top": "2vh"},
                                                    ),
                                                    html.I(
                                                        style={
                                                            "display": "block",
                                                            "padding-top": "2vh",
                                                            "padding-bottom": "2vh",
                                                        },
                                                        id="vessels-collapse-icon",
                                                    ),
                                                ],
                                                id="collapse-button",
                                                color="dark",
                                                outline=True,
                                                n_clicks=0,
                                            ),
                                            className="d-grid gap-2",
                                            style={"margin-top": "5vh"},
                                        ),
                                        PYGEOAPI_VESSEL_CARD,
                                    ],
                                    id="offcanvas",
                                    is_open=False,
                                ),
                            ]
                        ),
                        dbc.Col(
                            dbc.NavbarBrand("UC2 - Vessel Detection", className="ms-2")
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            ],
            fluid=True,
        ),
        id="main-navbar",
        color="dark",
        dark=True,
    )

    return comp
