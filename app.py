import pandas as pd
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output

# Load data
df = pd.read_csv("data/openings_stats.csv")

app = Dash(__name__)

# Define app layout
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
    dcc.Dropdown(
        id='sort',
        options=[
            {"label": "Number of masters games played", "value": "total_masters"},
            {"label": "Number of lichess games played", "value": "total_lichess"},
            {"label": "Masters white success rate", "value": "white_masters"},
            {"label": "Masters black success rate", "value": "black_masters"},
            {"label": "Masters draw rate", "value": "draws_masters"},
            {"label": "Lichess white success rate", "value": "white_lichess"},
            {"label": "Lichess black success rate", "value": "black_lichess"},
            {"label": "Lichess draw rate", "value": "draws_lichess"}
        ],
        value="total_masters"
    ),
    dcc.Dropdown(
        id="selector",
        options=[
            {"label": op, "value": op} for op in df.name.unique()
        ],
        value=df.name.unique(),
        multi=True
    ),
    dash_table.DataTable(
        id="table",
        fixed_rows={"headers": True},
        style_table={"height": 400}
    )
], style={"width": "45%", "padding": "0px 20px 20px 20px"})


@app.callback(
    Output("table", "data"),
    Input("open-var", "value"),
    Input("color", "value"),
    Input("sort", "value"),
    Input("selector", "value")
)
def update_table(open_var, color, sort, selector):
    dff = df.copy()
    columns = [col for col in dff.columns if col not in ["name", "color", "variation", sort]]

    # Filter openings or variations
    if open_var == "open":
        dff = dff[dff.variation.isna()]
        dff.drop("variation", axis=1, inplace=True)
    else:
        dff = dff[dff.variation.notna()]

    # Filter colors
    dff = dff[dff.color.isin(color)]

    # Filter openings
    dff = dff[dff.name.isin(selector)]

    # Sort
    dff.sort_values(sort, ascending=False, inplace=True)

    dff.drop(columns, axis=1, inplace=True)

    return dff.to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)
