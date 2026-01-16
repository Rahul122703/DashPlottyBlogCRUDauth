from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import requests


layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H2("Edit Post", className="mb-4 text-center"),

                    dcc.Location(id="url"),
                    dcc.Store(id="token-store", storage_type="session"),

                    dbc.Label("Title"),
                    dbc.Input(
                        id="edit-title",
                        placeholder="Update title",
                        type="text",
                        className="mb-3"
                    ),

                    dbc.Label("Content"),
                    dbc.Textarea(
                        id="edit-content",
                        placeholder="Update content",
                        style={"height": "200px"},
                        className="mb-3"
                    ),

                    dbc.Button("Update Post", id="update-btn", color="warning", className="w-100"),

                    html.Div(id="edit-msg", className="mt-3 text-center")
                ])
            ], className="shadow-lg p-2"),
            width=8
        ),
        justify="center",
        className="mt-5"
    )
], fluid=True)


@callback(
    Output("edit-msg", "children"),
    Input("update-btn", "n_clicks"),
    State("edit-title", "value"),
    State("edit-content", "value"),
    State("url", "pathname"),
    State("token-store", "data")
)
def update_post(n, title, content, path, token):
    if not n:
        return ""

    post_id = path.split("/")[-1]

    headers = {"Authorization": f"Bearer {token}"}

    res = requests.put(
        f"http://localhost:8050/posts/{post_id}",
        json={"title": title, "content": content},
        headers=headers
    )

    if res.status_code == 200:
        return dbc.Alert("Post updated successfully", color="success")
    else:
        return dbc.Alert("Failed to update post", color="danger")
