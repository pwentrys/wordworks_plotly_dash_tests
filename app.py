import dash
import dash_core_components as dcc
import dash_html_components as html
import os

import pandas as pd


path = 'O:\Code\python\scraper_proto__py_361_win_64\data\IRBT.csv'
base = os.path.basename(path)
base_name, base_ext = os.path.splitext(base)

df = pd.read_csv(path)


def generate_table(dataframe, max_rows=1000):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash()

app.layout = html.Div(children=[
    html.H4(children=base_name),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)
