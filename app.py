from dash import Dash, html, dcc
from flask import Flask
from flask_jwt_extended import JWTManager
import dash
from dash import Dash, html, dcc
from config import JWT_SECRET
from auth.routes import auth_bp
from blog.routes import blog_bp
import dash_bootstrap_components as dbc

import pages.login
import pages.register
import pages.dashboard
import pages.create_post
import pages.edit_post
from components.navbar import navbar

server = Flask(__name__)
server.config["JWT_SECRET_KEY"] = JWT_SECRET
JWTManager(server)

server.register_blueprint(auth_bp)
server.register_blueprint(blog_bp)

app = Dash(
    __name__,
    server=server,
    use_pages=True,
    external_stylesheets=[dbc.themes.CYBORG] 
)
app.layout = html.Div([
    dcc.Location(id="url"),
    navbar(),
    html.Div(dash.page_container)
])

dash.register_page("login", path="/login", layout=pages.login.layout)
dash.register_page("register", path="/register", layout=pages.register.layout)
dash.register_page("dashboard", path="/", layout=pages.dashboard.layout)
dash.register_page("create", path="/create", layout=pages.create_post.layout)
dash.register_page("edit", path_template="/edit/<post_id>", layout=pages.edit_post.layout)

if __name__ == "__main__":
    app.run(debug=True)
