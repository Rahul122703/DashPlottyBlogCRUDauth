from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import requests


layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H2("Create Account", className="text-center mb-4"),

                    dbc.Label("Email"),
                    dbc.Input(
                        id="reg-email",
                        placeholder="Enter your email",
                        type="email",
                        className="mb-3"
                    ),

                    dbc.Label("Password"),
                    dbc.Input(
                        id="reg-password",
                        placeholder="Create a password",
                        type="password",
                        className="mb-3"
                    ),

                    dbc.Button(
                        "Register",
                        id="reg-btn",
                        color="success",
                        className="w-100"
                    ),

                    html.Div(id="reg-msg", className="mt-3 text-center")
                ])
            ], className="shadow-lg p-2"),
            width=6
        ),
        justify="center",
        className="mt-5"
    )
], fluid=True)


@callback(
    Output("reg-msg", "children"),
    Input("reg-btn", "n_clicks"),
    State("reg-email", "value"),
    State("reg-password", "value")
)
def register(n, email, password):
    if not n:
        return ""

    res = requests.post(
        "http://localhost:8050/register",
        json={
            "email": email,
            "password": password
        }
    )

    if res.status_code == 200:
        return dbc.Alert("Account created successfully", color="success")
    else:
        return dbc.Alert("Registration failed", color="danger")
