import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import graphs


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

"""

Layout of the tab Domains

"""
app.layout = html.Div(
    id="layout_plot_domains_and_pie_charts",
    style={'backgroundColor': '#f6f6f6',
           'display': 'flex', 'flexDirection': 'column'},
    children=[
        html.Div(
            children=[
                dcc.Checklist(
                    id='my_checklist',
                    options=[
                        {'label': 'Universities', 'value': 'university'},
                        {'label': 'Institucional',
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
                          figure= graphs.create_histogram_domains(
                              ['Universities', 'Institutional', 'Tools Collections', 'Generic',  'Life Sciences', 'others'], graphs.domains, graphs.values_36),
                          className='six columns',
                          style={'height': '820px', 'margin': '1%', 'border': '1px solid #808080',
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
                                html.Div(
                                    children=[
                                        dcc.Graph(id="pie_chart_1",
                                                  className="little_plots",
                                                  figure=graphs.create_pie_chart(
                                                      graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["https"], ['HTTPS', 'HTTP'], "HTTP vs HTTPS"),
                                                  config={"displaylogo": False, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                                    ]),
                                html.Div(
                                    children=[
                                        dcc.Graph(id="pie_chart_2",
                                                  className="little_plots",
                                                  figure=graphs.create_pie_chart(graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["bioschemas"], [
                                                      'Bioschemas', 'No bioschemas'], "BIOSCHEMAS"),
                                                  config={"displaylogo": False, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                                    ]),
                            ]),
                        html.Div(
                            className='six columns',
                            children=[
                                html.Div(
                                    children=[
                                        dcc.Graph(id="pie_chart_3",
                                                  className="little_plots",
                                                  figure=graphs.create_pie_chart(
                                                      graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["ssl"], ['SSL', 'No SSL'], "SSL Certificates"),
                                                  config={"displaylogo": False, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                                    ]),
                                html.Div(
                                    children=[
                                        dcc.Graph(id="histogram_HTTP_codes",
                                                  className="little_plots",
                                                  figure=graphs.create_bar_http_codes(
                                                      graphs.metrics['http_codes_by_classification'][-1]["total"]),
                                                  config={"displaylogo": False, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                                    ]),
                            ])
                    ]
                )])])

"""
Callback in tab_domains:

"""
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
        return graphs.create_pie_chart(final_values_http, ['HTTPS', 'HTTP'], "HTTP vs HTTPS"), graphs.create_pie_chart(final_values_bioschema, ['Bioschemas', 'No bioschemas'], "BIOSCHEMAS"), graphs.create_pie_chart(final_values_ssl, ['SSL', 'No SSL'], "SSL Certificates"),  graphs.create_bar_http_codes(final_dict_http_codes), graphs.create_histogram_domains(values, graphs.domains, graphs.values_36)
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
        return graphs.create_pie_chart(final_values_http, ['HTTPS', 'HTTP'], "HTTP vs HTTPS"), graphs.create_pie_chart(final_values_bioschema, ['Bioschemas', 'No bioschemas'], "BIOSCHEMAS"), graphs.create_pie_chart(final_values_ssl, ['SSL', 'No SSL'], "SSL Certificates"), graphs.create_bar_http_codes(final_dict_http_codes), graphs.create_histogram_domains(values, graphs.domains, graphs.values_36)
    return graphs.create_pie_chart(graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["https"], ['HTTPS', 'HTTP'], "HTTP vs HTTPS"), graphs.create_pie_chart(graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["bioschemas"], ['Bioschemas', 'No bioschemas'], "BIOSCHEMAS"), graphs.create_pie_chart(graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["ssl"], ['SSL', 'No SSL'], "SSL Certificates"), graphs.create_bar_http_codes(graphs.metrics['http_codes_by_classification'][-1]["total"]), graphs.create_histogram_domains(
        ['Universities', 'Institutional', 'Tools Collections', 'Generic',  'Life Sciences', 'others'], graphs.domains, graphs.values_36)


if __name__ == '__main__':
    app.run_server(debug=True)
