import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html

import colorlover as cl
import datetime as dt
import flask
import os
import pandas as pd
import numpy as np
import sys
from pandas_datareader.data import DataReader
import time
from utilities.SQL import SQL as SQLs


sql = SQLs('mysql+pymysql://gappi:92cf6cc2050f9830996b42433da09d03a4baa26e5524b3b8075c2f076451650a@192.168.1.172:3306/stocks?charset=utf8')

server = flask.Flask('stock-tickers')
app = dash.Dash('stock-tickers', server=server, url_base_pathname='/dash/gallery/stock-tickers/', csrf_protect=False)
server.secret_key = os.environ.get('secret_key', 'secret')

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-finance-1.28.0.min.js'

colorscale = cl.scales['9']['qual']['Paired']

__path = f'O:\Code\python\scraper_proto__py_361_win_64'
__path = os.path.join(__path, 'models')
__path = os.path.join(__path, 'stocks.csv')

PROJECT_PATH = sys.path[0]
DATA_DIR = os.path.join(PROJECT_PATH, 'data')
DATA_PATH = pathlib.Path(DATA_DIR)
if not DATA_PATH.is_dir():
    DATA_PATH.mkdir()

src_text = pathlib.Path(__path).read_text(encoding='utf-8')
dst_path = pathlib.Path(os.path.join(DATA_DIR, 'stocks.csv'))
text_list = src_text.splitlines()
text_list = sorted(text_list, key=lambda x: x.split(',')[2])
text_list.insert(0, 'day,name,symbol,backtrack')
dst_text = '\n'.join(text_list)
dst_text = dst_text.replace('_', ' ')
dst_path.write_text(dst_text, encoding='utf-8')


csv_data = pd.read_csv(dst_path, delimiter=',', usecols=['name', 'symbol'])
# csv_symbols = csv_data.get('symbol').values

sql_data = sql.execute_table_cols('stock', ['name', 'symbol'])
# sql_symbols = sql_data.get('symbol').values

# to_add = []
# for item in csv_symbols:
#     if not sql_symbols.__contains__(item):
#         to_add.append(item)
#
out = csv_data[~csv_data.symbol.isin(sql_data.symbol)]

class Stock:
    @staticmethod
    def get_insert_single(row):
        out = []
        for item in row[1:]:
            out.append(f"'{item}'")
        joined = ','.join(out)
        return f'({joined}),'

    @staticmethod
    def get_insert_multiple(rows):
        joined = ''.join([Stock.get_insert_single(row) for row in rows.itertuples()])
        return joined[:-1]

    @staticmethod
    def get_insert_prefix(schema, table, columns):
        cols = []
        for column in columns:
            cols.append(f"`{column}`")
        cols = ','.join(cols)
        return f'INSERT INTO `{schema}`.`{table}` ({cols}) VALUES '

    @staticmethod
    def get_full_insert(schema, table, rows):
        prefix = Stock.get_insert_prefix(schema, table, rows.columns)
        return f'{prefix}{Stock.get_insert_multiple(rows)};'


if len(out) > 0:
    stock_query = Stock.get_full_insert('stocks', 'stock', out)
    sql.execute(stock_query)
# for row in out.iterrows():
#     print(row)

exit()
df_symbol.to_sql('stock', con=sql.conn, schema='stocks')
# sql.execute_table_cols()
exit()
from pprint import pprint


for item in df_symbol:
    print(item.data)
    print(item.data.obj)
    pprint(dir(item.data.obj))
    print(item.tobytes())
    # print(item.tofile)
    print(item.tolist())
    print(item.tostring())
    # print(dir(item))
exit()
# df_symbol = pd.read_sql_query('SELECT name, symbol, id FROM stock;', sql.conn)
res = df_symbol.columns
print(res)
print(dir(res))
exit()
print(df_symbol.columns)
for i in range(0, len(header)):
    print(i)

df_symbol.columns[0] = header[0]
print(dir(df_symbol.columns))
# print(df_symbol.T)
exit()
# .name = 'Company'
for sym in df_symbol:
    print(sym)
    # print(dir(sym))
    # print(dir(df_symbol))

app.layout = html.Div([
    html.Div([
        html.H2('Google Finance Explorer',
                style={'display': 'inline',
                       'float': 'left',
                       'font-size': '2.65em',
                       'margin-left': '7px',
                       'font-weight': 'bolder',
                       'font-family': 'Product Sans',
                       'color': "rgba(117, 117, 117, 0.95)",
                       'margin-top': '20px',
                       'margin-bottom': '0'
                       }),
        html.Img(src="https://s3-us-west-1.amazonaws.com/plotly-tutorials/logo/new-branding/dash-logo-by-plotly-stripe.png",
                style={
                    'height': '100px',
                    'float': 'right'
                },
        ),
    ]),
    dcc.Dropdown(
        id='stock-ticker-input',
        options=[{'label': s[0], 'value': s[1]}
                 for s in zip(df_symbol.Company, df_symbol.Symbol)],
        value=['YHOO', 'GOOGL'],
        multi=True
    ),
    html.Div(id='graphs')
], className="container")

def bbands(price, window_size=10, num_of_std=5):
    rolling_mean = price.rolling(window=window_size).mean()
    rolling_std  = price.rolling(window=window_size).std()
    upper_band = rolling_mean + (rolling_std*num_of_std)
    lower_band = rolling_mean - (rolling_std*num_of_std)
    return rolling_mean, upper_band, lower_band

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('stock-ticker-input', 'value')])
def update_graph(tickers):
    graphs = []
    for i, ticker in enumerate(tickers):
        try:
            df = DataReader(ticker, 'google',
                            dt.datetime(2017, 1, 1),
                            dt.datetime.now())
        except:
            graphs.append(html.H3(
                'Data is not available for {}'.format(ticker),
                style={'marginTop': 20, 'marginBottom': 20}
            ))
            continue

        candlestick = {
            'x': df.index,
            'open': df['Open'],
            'high': df['High'],
            'low': df['Low'],
            'close': df['Close'],
            'type': 'candlestick',
            'name': ticker,
            'legendgroup': ticker,
            'increasing': {'line': {'color': colorscale[0]}},
            'decreasing': {'line': {'color': colorscale[1]}}
        }
        bb_bands = bbands(df.Close)
        bollinger_traces = [{
            'x': df.index, 'y': y,
            'type': 'scatter', 'mode': 'lines',
            'line': {'width': 1, 'color': colorscale[(i*2) % len(colorscale)]},
            'hoverinfo': 'none',
            'legendgroup': ticker,
            'showlegend': True if i == 0 else False,
            'name': '{} - bollinger bands'.format(ticker)
        } for i, y in enumerate(bb_bands)]
        graphs.append(dcc.Graph(
            id=ticker,
            figure={
                'data': [candlestick] + bollinger_traces,
                'layout': {
                    'margin': {'b': 0, 'r': 10, 'l': 60, 't': 0},
                    'legend': {'x': 0}
                }
            }
        ))

    return graphs


external_css = ["https://fonts.googleapis.com/css?family=Product+Sans:400,400i,700,700i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/2cc54b8c03f4126569a3440aae611bbef1d7a5dd/stylesheet.css"]

for css in external_css:
    app.css.append_css({"external_url": css})


if __name__ == '__main__':
    app.run_server(debug=True)
