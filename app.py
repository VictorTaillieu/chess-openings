import pandas as pd
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output

df = pd.read_csv("data/openings_stats.csv")

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id="open-var",
        options=[
            {"label": "Opening", "value": "open"},
            {"label": "Variation", "value": "var"}
        ],
        value="open"
    ),
    dcc.Dropdown(
        id="color",
        options=[
            {"label": "White", "value": "white"},
            {"label": "Black", "value": "black"}
        ],
        value=["white", "black"],
        multi=True
    ),
    dash_table.DataTable(
        id="table",
        fixed_rows={"headers": True},
        style_table={"height": 400}
    )
])


@app.callback(
    Output("table", "data"),
    Input("open-var", "value"),
    Input("color", "value")
)
def update_table(open_var, color):
    dff = df.copy()

    if open_var == "open":
        dff = dff[dff.variation.isna()]
        dff.drop("variation", axis=1, inplace=True)
    else:
        dff = dff[dff.variation.notna()]

    dff = dff[dff.color.isin(color)]

    return dff.to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)
