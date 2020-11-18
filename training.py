import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from graphs import create_pie_chart
import pandas as pd
import dash
from data_reader import*
from graphs import*
from dash.exceptions import PreventUpdate



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_ok_codes = df_codes[df_codes["HTTP Codes"].str.startswith( ("1", "2", "3"))]
df_not_ok_codes = df_codes[df_codes["HTTP Codes"].str.startswith(("4", "5"))]


fig = create_pie_chart([df_ok_codes['Count'].sum(), df_not_ok_codes['Count'].sum()+ df_exceptions['Count'].sum()+df_extensions['Count'].sum()], ['OK', 'Not OK'], "Get Count")
fig_http_codes_ok = create_px_bar_http_codes(df_ok_codes, "HTTP Codes", "Count", "OK HTTP Codes response count", '#1976d3')
fig_http_codes_not_ok = create_px_bar_http_codes(df_not_ok_codes, "HTTP Codes", "Count", "NOT OK HTTP Codes response count", '#64b5f6')

fig_exceptions = create_px_bar_horizontal(df_exceptions, "Count",
                                          "Exceptions",
                                          "Exceptions count recieved",
                                          '#64b5f6',)
fig_extensions = create_px_bar_horizontal(df_extensions, "Count",
                                          "Extensions",
                                          "Extensions count recieved",
                                          '#64b5f6',)


app.layout = html.Div([
    dcc.Graph(
        id='basic-interactions',
        className="plot_ok_not_ok",
        config={'editable': True},
        figure=fig
    ),

    html.Div(
        children=[
            html.Div([
                dcc.Graph(id="hover-data-graph-1",
                          className="histogram_ok_not_ok",
                          config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                  'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                          ),
            ], id="div_left", style={'display': "None", "border": "1px solid #808080"}),
            html.Div([
                dcc.Graph(id="hover-data-graph-2",
                          className="histogram_ok_not_ok",
                          config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                  'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                          ),
            ],


                id="div_right", style={'display': "None", "border": "1px solid #808080"}),
            html.Div([
                dcc.Graph(id="hover-data-graph-3",
                          className="histogram_ok_not_ok",
                          config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                  'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                          ),
            ],
                id="div_down", style={'display': "None", "border": "1px solid #808080"}),
        ], style={"display": "flex", 'flexWrap': 'wrap', "justify-content": "space-around", 'alignItems' : 'space-around', 'alignContent': 'space-around' })
])


@app.callback(
    [
        Output('hover-data-graph-1', 'figure'),
        Output('div_left', 'style'),
        Output('hover-data-graph-2', 'figure'),
        Output('div_right', 'style'),
        Output('hover-data-graph-3', 'figure'),
        Output('div_down', 'style'),
    ],
    [Input('basic-interactions', 'hoverData')])
def display_hover_data(hoverData):
    if not hoverData:
        raise PreventUpdate
    if hoverData['points'][0]['label'] == "Not OK":
        return fig_http_codes_not_ok,  {'display': "Block"}, fig_exceptions, {'display': "Block"}, fig_extensions, {'display': "Block"}
    elif hoverData['points'][0]['label'] == "OK":
        return fig_http_codes_ok, {'display': "Block"}, fig_http_codes_ok, {'display': "None"}, fig_extensions, {'display': "None"}


if __name__ == '__main__':
    app.run_server(debug=True)
