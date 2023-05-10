import pandas as pd
from dash import Dash, dash_table

df = pd.read_csv("data/openings_stats.csv")

app = Dash(__name__)

app.layout = dash_table.DataTable(df.to_dict("records"))

if __name__ == "__main__":
    app.run_server(debug=True)
