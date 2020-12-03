import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import graphs
import dash_bootstrap_components as dbc

# Get external CSS:
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
app.title = "Homepages"
app.css.append_css(
    {'external_url': 'assets/styles.css'})
app.css.config.serve_locally = False
app.config['suppress_callback_exceptions'] = True
app.prevent_initial_callbacks = True

# Open file with all daya for this py
with open("new_input_data/extracted_metrics.json") as file:
    data = json.load(file)

"""

LAYOUT of the tab Domains

"""
app.layout = html.Div(
    id="layout_plot_domains_and_pie_charts",
    style={'backgroundColor': '#f6f6f6',
           'display': 'flex', 'flexDirection': 'column'},
    children=[
        html.Div(
                className="section-title ",
                children=[
                    html.Div(children=["Domains classification + Metrics"])
                        ]
                ),
        html.Div(
                style={'textAlign': 'center'},
                children=[
                            dcc.Markdown(
                                        children=[f'''
                                                            *The following plots have being calculated from the **{len(data['df_acces']):,}** unique websites* 
                                                            
                                                            *from an amount of **{data['total_len_tools']:,}** bioinformatics tools.*

                                                            '''],  
                                        style={"fontSize": "23px"}
                                        )
                                ]
                ),
        html.Hr(style={"margin": "1.5em"}),
        html.Div(
                style={"display": "flex", "margin": "1em auto"},
                children=[
                            dcc.Markdown(
                                style={"fontSize": "20px"},
                                children='''
                                                            **Universities:** individual research groups or oficial Universities.
                                                        
                                                            **Institutional:** known bioinformatics institutions and data centers.

                                                            **Tools Collections:** group of tools from different procedences.

                                                            **Generic:** generic repositories of software.
                                                        
                                                            **Life Sciences:** software collections related to biology.                               

                                                        ''')
                        ]
                    ),
        html.Div(
                children=[
                            dcc.Checklist(
                                        id='my_checklist',
                                        options=[
                                            {'label': 'Universities', 'value': 'university'},
                                            {'label': 'Institutional',
                                            'value': 'institucional'},
                                            {'label': 'Tools Collections',
                                            'value': 'collections'},
                                            {'label': 'Generic', 'value': 'generic'},
                                            {'label': 'Life Sciences', 'value': 'lifeScience'},
                                            {'label': 'Others', 'value': 'others'},
                                        ],
                                        value=['university', 'institucional',  'collections',
                                            'generic', 'lifeScience', 'others'],
                                        labelStyle={
                                            'display': 'inline-block', 'margin': '5px'},
                                        style={'border': '1px solid #d6d6d6',
                                            'padding': '10px', 'backgroundColor': 'white'}
                                        ),
                            html.Button(
                                "All", id="all_button", n_clicks=0, autoFocus=False, style={'backgroundColor': 'white', 'margin': '5px'},
                            ),
                            html.Button(
                                "Clear", id="clear_button", n_clicks=0, autoFocus=False,  style={'backgroundColor': 'white'}
                            )
                        ],
                style={
                    'height': 'auto', 'display': 'flex', 'flexWrap': 'wrap', 'textAlign': 'center', 'justifyContent': 'center', 'alignItems': 'center'
                }
        ),
        html.Div(
                id='layout_pie_charts_and_http_codes',
                style={'backgroundColor': '	#f6f6f6', 'boxSize': 'border-box',
                    'height': 'auto', 'width': 'auto', 'display': 'flex'},
                children=[
                    dcc.Graph(id='plot_domains',
                            figure=graphs.create_histogram_domains(
                                ['Universities', 'Institutional', 'Tools Collections', 'Generic',  'Life Sciences', 'others'], graphs.domains, graphs.values_36),
                            className='six columns',
                            style={'height': '980px', 'margin': '1%', 'border': '1px solid #808080',
                                    'maxHeight': 'inherit'},
                            config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                    html.Div(
                        id='layout_pies',
                        className='six columns',
                        children=[
                            html.Div(
                                className='six columns',
                                children=[
                                    dbc.Card(
                                        style={
                                            "width": "400px", "border": "1px solid #808080", "margin": "4%"},
                                        children=[
                                            dbc.CardBody(
                                                [
                                                    html.Div(
                                                        style={
                                                            "height": "27px", "backgroundColor": "white"},
                                                        children=[html.Img(
                                                            id="popover-bottom-target_1",
                                                            src="assets/boton-de-informacion.svg",
                                                            n_clicks=0,
                                                            className="info-icon",
                                                            style={
                                                                "margin": "5px"},
                                                        )
                                                        ]
                                                    ),
                                                    dbc.Popover(
                                                        [
                                                            dbc.PopoverHeader(
                                                                "HTTP vs HTTPS"),
                                                            dbc.PopoverBody(
                                                                children=[
                                                                    html.P(
                                                                        "HTTP: unsecured Hypertext Transfer Protocol. Does not require domain validation. No encryption."),
                                                                    html.P(
                                                                        "HTTPS: secure Hypertext Transfer Protocol. Requires domain validation. Has encryption."),
                                                                ],
                                                                style={
                                                                    "padding": "15px"}
                                                            ),
                                                        ],
                                                        id="popover_1",
                                                        target="popover-bottom-target_1",  # needs to be the same as dbc.Button id
                                                        placement="bottom",
                                                        is_open=False,
                                                        style={
                                                                            "backgroundColor": "white", "border": "1px solid #808080", "borderRadius" : "5px",
                                                                                    "padding": "15px"}
                                                    ),
                                                    dcc.Graph(id='pie_chart_1',

                                                            figure=graphs.create_pie_chart(
                                                                graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["https"], ['HTTPS', 'HTTP'], "HTTP vs HTTPS"),
                                                            config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                                                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                                                ]
                                            ),
                                        ],
                                        color="light",
                                    ),
                                    dbc.Card(
                                        style={
                                            "width": "400px", "border": "1px solid #808080", "margin": "4%"},

                                        children=[
                                            dbc.CardBody(

                                                [
                                                    html.Div(
                                                        style={
                                                            "height": "27px", "backgroundColor": "white"},
                                                        children=[html.Img(
                                                            id="popover-bottom-target_2",
                                                            src="assets/boton-de-informacion.svg",
                                                            n_clicks=0,
                                                            className="info-icon",
                                                            style={
                                                                "margin": "5px"},
                                                        )
                                                        ]
                                                    ),
                                                    dbc.Popover(
                                                        [
                                                            dbc.PopoverHeader(
                                                                "BIOSCHEMAS"),
                                                            dbc.PopoverBody(
                                                                children=[
                                                                    html.P(
                                                                        "Bioschemas extends Schema.org to include descriptions of relevant resources for the Life Sciences Community."),
                                                                    html.P(
                                                                        "Bioschemas uses Schema.org enabling machines to understand what it is the metadata of the data, increasing his Findability, integration, and re-use."),
                                                                    html.A(
                                                                        "Bioschemas.org", href='https://bioschemas.org/', target="_blank")

                                                                ],
                                                                style={
                                                                    "padding": "15px"}
                                                            ),
                                                        ],
                                                        id="popover_2",
                                                        target="popover-bottom-target_2",  # needs to be the same as dbc.Button id
                                                        placement="bottom",
                                                        is_open=False,
                                                        style={
                                                                "backgroundColor": "white", "border": "1px solid #808080", "borderRadius" : "5px",
                                                                                    "padding": "15px"}
                                                    ),
                                                    dcc.Graph(id='pie_chart_2',
                                                            figure=graphs.create_pie_chart(graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["bioschemas"],
                                                                                            ['Yes', 'No'], "BIOSCHEMAS"),
                                                            config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                                                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),

                                                ]
                                            ),
                                        ],
                                        color="light",
                                    ),

                                ]),
                            html.Div(
                                className='six columns',
                                children=[
                                    html.Div(
                                        children=[
                                            dbc.Card(
                                                style={
                                                    "width": "400px", "border": "1px solid #808080", "margin": "4%"},
                                                children=[
                                                    dbc.CardBody(
                                                        [
                                                            html.Div(
                                                                style={
                                                                    "height": "27px", "backgroundColor": "white"},
                                                                children=[html.Img(
                                                                    id="popover-bottom-target_3",
                                                                    src="assets/boton-de-informacion.svg",
                                                                    n_clicks=0,
                                                                    className="info-icon",
                                                                    style={
                                                                        "margin": "5px"},
                                                                    )
                                                                ]
                                                            ),
                                                            dbc.Popover(
                                                                [
                                                                    dbc.PopoverHeader(
                                                                        "SSL Certificates"),
                                                                    dbc.PopoverBody(
                                                                        children=[
                                                                            html.P(
                                                                                "Are a global security standard that allows the transfer of encrypted data between a browser and a web server signed by a CA (certification authority).")
                                                                        ],
                                                                        style={
                                                                            "padding": "15px"}
                                                                    ),
                                                                ],
                                                                id="popover_3",
                                                                target="popover-bottom-target_3",
                                                                placement="bottom",
                                                                is_open=False,
                                                                style={
                                                                            "backgroundColor": "white", "border": "1px solid #808080", "borderRadius" : "5px",
                                                                                    "padding": "15px"}
                                                            ),
                                                            dcc.Graph(id='pie_chart_3',
                                                                    figure=graphs.create_pie_chart(
                                                                        graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["ssl"], ['SSL', 'No SSL'], "SSL Certificates"),
                                                                    config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                                                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                                                        ]
                                                    ),
                                                ],
                                                color="light",
                                            ),
                                        ]),
                                    html.Div(
                                        children=[
                                            dbc.Card(
                                                style={
                                                    "width": "400px", "border": "1px solid #808080", "margin": "4%"},

                                                children=[
                                                    dbc.CardBody(
                                                                [
                                                                    html.Div(
                                                                        style={
                                                                            "height": "30px", "backgroundColor": "white"},
                                                                        children=[html.Img(
                                                                            id="popover-bottom-target_4",
                                                                            src="assets/boton-de-informacion.svg",
                                                                            n_clicks=0,
                                                                            className="info-icon",
                                                                            style={
                                                                                "margin": "6px"},
                                                                                        )   
                                                                        ]
                                                                    ),
                                                                    dbc.Popover(
                                                                        # style={"border": "1px solid #808080",
                                                                        #             "padding": "15px"},
                                                                        children=[
                                                                            dbc.PopoverHeader(
                                                                                "HTTP Codes"),
                                                                            dbc.PopoverBody(
                                                                                children=[
                                                                                    html.P(
                                                                                        "HTTP response status codes indicate whether a specific HTTP request has been successfully completed."),
                                                                                    html.A(
                                                                                        "HTTP response status codes.", href='https://developer.mozilla.org/en-US/docs/Web/HTTP/Status', target="_blank")
                                                                                ],
                                                                           
                                                                                
                                                                            ),
                                                                        ],
                                                                         
                                                                        id="popover_4",
                                                                        target="popover-bottom-target_4",
                                                                        placement="bottom",
                                                                        is_open=False,
                                                                        style={
                                                                            "backgroundColor": "white", "border": "1px solid #808080", "borderRadius" : "5px",
                                                                                    "padding": "15px"}
                                                                    ),
                                                                    dcc.Graph(id='histogram_HTTP_codes',
                                                                            figure=graphs.create_bar_http_codes(
                                                                                graphs.metrics['http_codes_by_classification'][-1]["total"]),
                                                                            config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                                                                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                                                                ]
                                                    ),
                                                ],
                                                color="light",
                                            ),

                                        ]),




                                ])
                        ]
                    )]
            )])

"""
Callback in tab_domains:

"""


@app.callback(
    Output("popover_1", "is_open"),
    [Input("popover-bottom-target_1", "n_clicks")],
    [State("popover_1", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("popover_2", "is_open"),
    [Input("popover-bottom-target_2", "n_clicks")],
    [State("popover_2", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("popover_3", "is_open"),
    [Input("popover-bottom-target_3", "n_clicks")],
    [State("popover_3", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("popover_4", "is_open"),
    [Input("popover-bottom-target_4", "n_clicks")],
    [State("popover_4", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output(component_id='my_checklist', component_property='value'),
    [Input(component_id='all_button', component_property='n_clicks'),
     Input(component_id='clear_button', component_property='n_clicks'),
     ])
def update_layout(all_n_clicks, clear_n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if changed_id == ".":
        raise PreventUpdate
    elif changed_id == "clear_button.n_clicks":
        return []
    elif changed_id == "all_button.n_clicks":
        return ['university', 'institucional', 'collections',  'generic', 'lifeScience', 'others']


@app.callback(
    [Output(component_id='pie_chart_1', component_property='figure'),
     Output(component_id='pie_chart_2', component_property='figure'),
     Output(component_id='pie_chart_3', component_property='figure'),
     Output(component_id='histogram_HTTP_codes', component_property='figure'),
     Output(component_id='plot_domains', component_property='figure'),
     ],
    [Input(component_id='my_checklist', component_property='value')])
def update_graph(values):
    all_http_codes, all_ssl_results, all_bioschema_results, all_http_codes_for_hist = graphs.get_initial_values_for_update()
    final_values_http = [0, 0]
    final_values_ssl = [0, 0]
    final_values_bioschema = [0, 0]
    final_dict_http_codes = {
        x: 0 for x in graphs.metrics['http_codes_by_classification'][-1]["total"]}
    if not values:
        return graphs.create_pie_chart(final_values_http, ['HTTPS', 'HTTP'], "HTTP vs HTTPS"), graphs.create_pie_chart(final_values_bioschema, ['Yes', 'No'], "BIOSCHEMAS"), graphs.create_pie_chart(final_values_ssl, ['SSL', 'No SSL'], "SSL Certificates"),  graphs.create_bar_http_codes(final_dict_http_codes), graphs.create_histogram_domains(values, graphs.domains, graphs.values_36)
    if values and 'clear' not in values:
        for index, t in enumerate(values):
            if t in all_http_codes.keys():
                final_values_http[0] += all_http_codes[t][0]
                final_values_http[1] += all_http_codes[t][1]
                final_values_ssl[0] += all_ssl_results[t][0]
                final_values_ssl[1] += all_ssl_results[t][1]
                final_values_bioschema[0] += all_bioschema_results[t][0]
                final_values_bioschema[1] += all_bioschema_results[t][1]
                for i in final_dict_http_codes:
                    if i in all_http_codes_for_hist[t]:
                        final_dict_http_codes[i] += all_http_codes_for_hist[t][i]
        return graphs.create_pie_chart(final_values_http, ['HTTPS', 'HTTP'], "HTTP vs HTTPS"), graphs.create_pie_chart(final_values_bioschema, ['Yes', 'No'], "BIOSCHEMAS"), graphs.create_pie_chart(final_values_ssl, ['SSL', 'No SSL'], "SSL Certificates"), graphs.create_bar_http_codes(final_dict_http_codes), graphs.create_histogram_domains(values, graphs.domains, graphs.values_36)
    return graphs.create_pie_chart(graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["https"], ['HTTPS', 'HTTP'], "HTTP vs HTTPS"), graphs.create_pie_chart(graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["bioschemas"], ['Bioschemas', 'No bioschemas'], "BIOSCHEMAS"), graphs.create_pie_chart(graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["ssl"], ['SSL', 'No SSL'], "SSL Certificates"), graphs.create_bar_http_codes(graphs.metrics['http_codes_by_classification'][-1]["total"]), graphs.create_histogram_domains(
        ['Universities', 'Institutional', 'Tools Collections', 'Generic',  'Life Sciences', 'others'], graphs.domains, graphs.values_36)


if __name__ == '__main__':
    app.run_server(debug=True)
