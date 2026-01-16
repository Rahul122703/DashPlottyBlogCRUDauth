from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import requests


layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H2("Login", className="text-center mb-4"),

                    dbc.Label("Email"),
                    dbc.Input(
                        id="email",
                        placeholder="Enter your email",
                        type="email",
                        className="mb-3"
                    ),

                    dbc.Label("Password"),
                    dbc.Input(
                        id="password",
                        placeholder="Enter your password",
                        type="password",
                        className="mb-3"
                    ),

                    dbc.Button(
                        "Login",
                        id="login-btn",
                        color="primary",
                        className="w-100"
                    ),

                    html.Div(id="login-msg", className="mt-3 text-center"),

                    dcc.Store(id="token-store", storage_type="session")
                ])
            ], className="shadow-lg p-2"),
            width=6
        ),
        justify="center",
        className="mt-5"
    )
], fluid=True)


@callback(
    Output("login-msg", "children"),
    Output("token-store", "data"),
    Input("login-btn", "n_clicks"),
    State("email", "value"),
    State("password", "value")
)
def login(n, email, password):
    if not n:
        return "", None

    res = requests.post(
        "http://localhost:8050/login",
        json={
            "email": email,
            "password": password
        }
    )

    if res.status_code == 200:
        return dbc.Alert("Logged in successfully", color="success"), res.json()["access_token"]
    else:
        return dbc.Alert("Invalid email or password", color="danger"), None
