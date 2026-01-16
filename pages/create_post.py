from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import requests

layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H2("Create New Post", className="mb-4 text-center"),

                    dbc.Label("Title"),
                    dbc.Input(id="title", placeholder="Enter post title", type="text", className="mb-3"),

                    dbc.Label("Content"),
                    dbc.Textarea(
                        id="content",
                        placeholder="Write your post here...",
                        style={"height": "200px"},
                        className="mb-3"
                    ),

                    dcc.Store(id="token-store", storage_type="session"),

                    dbc.Button("Publish Post", id="create", color="primary", className="w-100"),

                    html.Div(id="msg", className="mt-3 text-center")
                ])
            ], className="shadow-lg p-2"),
            width=8
        ),
        justify="center",
        className="mt-5"
    )
], fluid=True)


@callback(
    Output("msg", "children"),
    Input("create", "n_clicks"),
    State("title", "value"),
    State("content", "value"),
    State("token-store", "data")
)
def create_post(n, title, content, token):
    if not n:
        return ""

    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(
        "http://localhost:8050/posts",
        json={"title": title, "content": content},
        headers=headers
    )

    if res.status_code == 200:
        return dbc.Alert("Post created successfully", color="success")
    else:
        return dbc.Alert("Failed to create post", color="danger")
