import dash
from dash import html, dcc, callback, Output, Input, State, ALL
import dash_bootstrap_components as dbc
import requests


layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H2("All Blog Posts", className="text-center mb-4"),
            width=12
        )
    ),

    dbc.Row(
        dbc.Col(
            dbc.Button("Load Posts", id="load", color="primary", className="mb-4"),
            width=12,
            className="text-center"
        )
    ),

    dcc.Store(id="token-store", storage_type="session"),

    dbc.Row(
        dbc.Col(
            html.Div(id="posts"),
            width=12
        )
    )
], fluid=True, className="mt-4")


def render_posts(data):
    return [
        dbc.Card(
            dbc.CardBody([
                html.H4(p["title"], className="card-title"),
                html.P(p["content"], className="card-text"),

                dbc.Row([
                    dbc.Col(
                        dbc.Button(
                            "Edit",
                            href=f"/edit/{p['_id']}",
                            color="secondary",
                            size="sm"
                        ),
                        width="auto"
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Delete",
                            id={"type": "delete-btn", "index": p["_id"]},
                            color="danger",
                            size="sm"
                        ),
                        width="auto"
                    )
                ], className="g-2"),

            ]),
            className="mb-3 shadow-sm"
        )
        for p in data
    ]


@callback(
    Output("posts", "children"),
    Input("load", "n_clicks"),
    State("token-store", "data")
)
def load_posts(n, token):
    if not n:
        return ""

    res = requests.get("http://localhost:8050/posts")
    data = res.json()

    return render_posts(data)


@callback(
    Output("posts", "children", allow_duplicate=True),
    Input({"type": "delete-btn", "index": ALL}, "n_clicks"),
    State("token-store", "data"),
    prevent_initial_call=True
)
def delete_post(n_clicks, token):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update

    post_id = ctx.triggered[0]["prop_id"].split(".")[0]
    post_id = eval(post_id)["index"]

    headers = {"Authorization": f"Bearer {token}"}

    requests.delete(
        f"http://localhost:8050/posts/{post_id}",
        headers=headers
    )

    # reload posts
    res = requests.get("http://localhost:8050/posts")
    data = res.json()

    return render_posts(data)
