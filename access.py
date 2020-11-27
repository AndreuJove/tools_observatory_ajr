import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from graphs import create_pie_chart
import pandas as pd
import json
import dash
import graphs
from dash.exceptions import PreventUpdate


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
app.title = "Access"
app.css.append_css(
    {'external_url': 'assets/styles.css'})
app.css.config.serve_locally = False
app.config['suppress_callback_exceptions'] = True
app.prevent_initial_callbacks = True


# Open file with all daya for this py
with open("new_input_data/extracted_metrics.json") as file:
    data = json.load(file)


# Create dataframe from plots:
df_access = pd.DataFrame(data['df_acces'])
df_codes = pd.DataFrame(list(data['dict_http_codes_count'].items()), columns=[
                        'HTTP Code', 'Count'])
df_days_up = pd.DataFrame(list(data['dict_uptimes_days'].items()), columns=[
                        'Days OK', 'Number of websites'])


# Filter dataframe codes by OK not OK
df_ok_codes = df_codes[df_codes["HTTP Code"].astype(
    str).str.startswith(("1", "2", "3"))].sort_values(by='Count', ascending=False).reset_index(drop=True)
df_not_ok_codes = df_codes[df_codes["HTTP Code"].astype(
    str).str.startswith(("4", "5"))]


fig_http_codes_ok = graphs.create_px_bar_http_codes(
    df_ok_codes, "HTTP Code", "Count", "OK HTTP Codes response count", '#1976d3')
fig_http_codes_not_ok = graphs.create_px_bar_http_codes(
    df_not_ok_codes, "HTTP Code", "Count", "NOT OK HTTP Codes response count", '#64b5f6')


app.layout = html.Div(
    children=[
        html.Div(
            className="section-title ",
            children=[
                html.Div(children=["Access Websites"])
            ]
        ),
        html.Div(
            style={'textAlign': 'center'},
            children=[
                dcc.Markdown(
                    children=[f'''
                                        *The following plots have being calculated from the **{len(data['df_acces'])}** unique websites* 
                                        
                                        *from an amount of **{data['total_len_tools']}** bioinformatics tools.*

                                        '''],  style={"fontSize": "23px"})
            ]
        ),
        html.Hr(style={"margin": "4em"}),
        html.Div(
            className= "div_markdown",
            
            children=[
                dcc.Markdown(
                    children=[f'''
                                        HTTP Codes recieved and classified from {len(data['df_acces'])} unique websites.
                                        
                                        For more information visit:

                                        ''']),
                html.A("HTTP response status codes.", href='https://developer.mozilla.org/en-US/docs/Web/HTTP/Status', target="_blank")  
            ]
        ),
        
        html.Div(
            id="div_parent_access_websites",
            children=[
                html.Div(
                        id="div_pie_codes_and_histogram_codes",
                         children=[
                                    html.Div(
                                                id="pie_ok_not_ok_markdown",
                                                children=[
                                                    dcc.Graph(
                                                        id='http_codes_ok_not_ok',
                                                        config={
                                                            'editable': True},
                                                        figure=create_pie_chart([df_ok_codes['Count'].sum(), df_not_ok_codes['Count'].sum()], ['OK', 'Not OK'], "Total HTTP Codes received")
                                                                ),
                                                    dcc.Markdown(   
                                                                    children=['''
                                                                                    
                                                                                    **OK**:

                                                                                    ``1xx``: Informational.

                                                                                    ``2xx``: Success.
                                                                                    
                                                                                    3xx: Redirection.
                                                                                    
                                                                                    **NOT OK**:

                                                                                    4xx: Client Error.

                                                                                    5xx: Server Error.

                                                                                    '''],

                                                                    style={
                                                                            "fontSize": "20px"}
                                                                    )


                                                            ]),

                                    dcc.Graph(  id="histogram_ok_not_ok_codes",
                                                config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                                'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                                    ),
                        ]
                ),

             
            ]),
        html.Hr(style={"margin": "4em"}),
        html.Div(
            className= "div_markdown",
            children=[
                dcc.Markdown(
                    children=[f'''
                                        Stadistics obtained from the websites for the last 30 days:

                                        ''']
                            )               
            ]
        ),
        html.Div(  id="div_30_days",
                    children=[
                            html.Div(
                                        id="div_average_access_time_and_markdown",
                                        children=[                         
                                                    dcc.Graph(
                                                                id="average_access_box_plot",
                                                                config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                                                        'modeBarButtonsToRemove': ['pan2d', 'lasso2d']},
                                                                figure=graphs.create_box_plot_time_access(
                                                                    df_access)
                                                            ),
                                                    dcc.Markdown(
                                                                children=['''                                                                   
                                                                            **Average Access Time (AAT):**

                                                                            *is average of time in*
                                                                            
                                                                            *miliseconds to get the*

                                                                            *the response of the server*
                                                                            
                                                                            *during the last 30 days.*

                                                                            *The first website and*
                                                                            
                                                                            *and his redirections are*

                                                                            *showed in the outliers.*

                                                                            *As shown in the plot*
                                                                            
                                                                            *AAT is related with*

                                                                            *the redirections (3xx).*

                                                                            '''],
                                                                style={
                                                                    "fontSize": "20px"})                   
                                                ]
                                            ),  
                                
                            html.Div( id ="histogram_days_up_and_markdown",
                                        children=[  
                                                dcc.Graph(
                                                            id="histogram_days_up",
                                                            config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                                                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d']},
                                                            figure=graphs.create_px_bar_days_up(df_days_up, "Days OK", "Number of websites", "Days UP in the last 30 days", '#1976d3')                                   
                                                        ),
                                                dcc.Markdown(
                                                            children=['''
                                                                                            
                                                                        *This figure shows for each website the*

                                                                        _number of **Days UP** (OK HTTP Code)_

                                                                        *of the last 30 days.*                                                                        

                                                                        '''],

                                                            style={
                                                                "fontSize": "20px"})

                                            ])
                            ]
                        )
    ])

@app.callback(
    Output('histogram_ok_not_ok_codes', 'figure'),
    [Input('http_codes_ok_not_ok', 'hoverData')])
def display_hover_data(hoverData):
    if not hoverData:
        return fig_http_codes_ok
    if hoverData['points'][0]['label'] == "Not OK":
        return fig_http_codes_not_ok
    elif hoverData['points'][0]['label'] == "OK":
        return fig_http_codes_ok


PORT = 8000
if __name__ == '__main__':
    app.run_server(debug=True, port=PORT)
