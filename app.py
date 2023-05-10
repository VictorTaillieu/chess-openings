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
    dash_table.DataTable(
        id="table",
        data=df.to_dict("records"),
        fixed_rows={"headers": True},
        style_table={"height": 400}
    )
])


@app.callback(
    Output("table", "data"),
    Input("open-var", "value")
)
def update_open_var(open_var):
    dff = df.copy()

    if open_var == "open":
        dff = dff[dff.variation.isna()]
        dff.drop("variation", axis=1, inplace=True)
    else:
        dff = dff[dff.variation.notna()]

    return dff.to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)
