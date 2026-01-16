import dash_bootstrap_components as dbc

def navbar():
    return dbc.NavbarSimple(
        brand="MyBlog",
        brand_href="/",
        color="dark",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Create Post", href="/create")),
            dbc.NavItem(dbc.NavLink("Login", href="/login")),
            dbc.NavItem(dbc.NavLink("Register", href="/register")),
        ],
    )
