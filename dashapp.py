import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

_data = pd.read_excel('data.xlsx')
df = pd.DataFrame(dict(learning=_data['Learning Rate'], testing=_data['Test Performance'], crime=_data['Crime'],
                          housing=_data['Normalized Housing Price'], farms=_data['FARMS Rate with Multiplier If Applicable'],
                          absence=_data['Absence Rate'], discipline=_data['discipline rate'], prop=_data['Proportion of Revenue Spent on Teachers']))

app.layout = html.Div([
    html.Div([html.H1("Florida EJNQI")],
             style={'textAlign': "center", "padding-bottom": "10", "padding-top": "10"}),
    html.Div(
        [html.Div(dcc.Dropdown(id="select-xaxis", options=[{'label': i.title(), 'value': i} for i in df.columns],
                               value='learning', ), className="four columns",
                  style={"display": "block", "margin-left": "auto",
                         "margin-right": "auto", "width": "25%"}),
         html.Div(dcc.Dropdown(id="select-yaxis", options=[{'label': i.title(), 'value': i} for i in df.columns],
                               value='testing', ), className="four columns",
                  style={"display": "block", "margin-left": "auto",
                         "margin-right": "auto", "width": "25%"}),
         html.Div(dcc.Dropdown(id="select-zaxis", options=[{'label': i.title(), 'value': i} for i in df.columns],
                               value='crime', ), className="four columns",
                  style={"display": "block", "margin-left": "auto",
                         "margin-right": "auto", "width": "25%"}),
         html.Div(dcc.Dropdown(id="select-color", options=[{'label': i.title(), 'value': i} for i in df.columns],
                               value='housing', ), className="four columns",
                  style={"display": "block", "margin-left": "auto",
                         "margin-right": "auto", "width": "25%"})
         ], className="row", style={"padding": 14, "display": "block", "margin-left": "auto",
                                    "margin-right": "auto", "width": "80%"}),
    html.Div([dcc.Graph(id="my-graph")])
], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("select-xaxis", "value"),
     dash.dependencies.Input("select-yaxis", "value"),
     dash.dependencies.Input("select-zaxis", "value"),
     dash.dependencies.Input("select-color", "value")]

)
def ugdate_figure(selected_x, selected_y, selected_z, selected_color):
    trace = [go.Scatter3d(
        x=df[selected_x], y=df[selected_y], z=df[selected_z],
        mode='markers', marker={'size': 8, 'color': df[selected_color], 'colorscale': 'Blackbody', 'opacity': 0.8, "showscale": True,
                                "colorbar": {"thickness": 15, "len": 0.5, "x": 0.8, "y": 0.6, }, })]
    return {"data": trace,
            "layout": go.Layout(
                height=700, title=f"Edudata<br>{selected_x.title(), selected_y.title(), selected_z.title(), selected_color.title()}",
                paper_bgcolor="#f3f3f3",
                scene={"aspectmode": "cube", "xaxis": {"title": f"{selected_x.title()}", },
                       "yaxis": {"title": f"{selected_y.title()}", },
                       "zaxis": {"title": f"{selected_z.title()}", }})
            }

app.run_server(debug=True)
