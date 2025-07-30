from datetime import date

import dash_bootstrap_components as dbc
from dash import dcc, html

PYGEOAPI_VESSEL_CARD = dbc.Collapse(
    [
        html.Div(
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dcc.DatePickerSingle(
                                date=date(2021, 10, 1),
                                min_date_allowed=date(2021, 1, 1),
                                max_date_allowed=date(2021, 12, 31),
                                id="vessels-date-picker",
                            )
                        ],
                        style={"padding-top": "1vh"},
                    ),
                    dbc.Row(
                        [
                            "From: ",
                            dcc.Input(
                                placeholder="HH:MM:SS",
                                pattern=r"[0-9]{2}:[0-9]{2}:[0-9]{2}",
                                id="vessels-start-time",
                                style={
                                    "width": "30%",
                                    "margin-left": "3%",
                                    "margin-right": "3%",
                                },
                            ),
                            "Until: ",
                            dcc.Input(
                                placeholder="HH:MM:SS",
                                pattern=r"[0-9]{2}:[0-9]{2}:[0-9]{2}",
                                id="vessels-end-time",
                                style={"width": "30%", "margin-left": "3%"},
                            ),
                        ],
                        style={"padding-top": "1vh"},
                    ),
                    dbc.Row(
                        [
                            dbc.Button(
                                [
                                    html.I(
                                        className="fa-regular fa-plus",
                                    )
                                ],
                                id="vessels-layer-add-button",
                                outline=False,
                                color="primary",
                                n_clicks=0,
                            )
                        ],
                        style={"padding-top": "1vh"},
                    ),
                ]
            ),
        )
    ],
    id="collapse",
    is_open=False,
    style={"width": "90%", "margin-left": "5%"},
)
