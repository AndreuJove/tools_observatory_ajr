import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from data_reader import*
from graphs import*


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

tabs_styles = {
    'height': '2.5em',
    'margin': '10px',
    'display': 'flex'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

app.layout = html.Div([
    dcc.Tabs(id="tabs-styled-with-inline", value='tab-2',
             children=[
                dcc.Tab(label='Domains and Metrics', value='tab-1',
                        style=tab_style, selected_style=tab_selected_style),
                dcc.Tab(label='Access', value='tab-2', style=tab_style,
                        selected_style=tab_selected_style),
                dcc.Tab(label='JavaScript', value='tab-3',
                        style=tab_style, selected_style=tab_selected_style),
             ], style={'display': 'flex', 'flexWrap': 'wrap'}

             ),
    html.Div(id='tabs-content-inline')
])


"""

Layout of the tab Domains

"""
tab_domains = html.Div(
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
                          figure=create_histogram_domains(
                              ['Universities', 'Institutional', 'Tools Collections', 'Generic',  'Life Sciences', 'others'], domains, values_36),
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
                                                  figure=create_pie_chart(
                                                      metrics_bioschemas_ssl_https_by_classification[-1]["total"]["https"], ['HTTPS', 'HTTP'], "HTTP vs HTTPS"),
                                                  config={"displaylogo": False, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                                    ]),
                                html.Div(
                                    children=[
                                        dcc.Graph(id="pie_chart_2",
                                                  className="little_plots",
                                                  figure=create_pie_chart(metrics_bioschemas_ssl_https_by_classification[-1]["total"]["bioschemas"], [
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
                                                  figure=create_pie_chart(
                                                      metrics_bioschemas_ssl_https_by_classification[-1]["total"]["ssl"], ['SSL', 'No SSL'], "SSL Certificates"),
                                                  config={"displaylogo": False, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                                    ]),
                                html.Div(
                                    children=[
                                        dcc.Graph(id="histogram_HTTP_codes",
                                                  className="little_plots",
                                                  figure=create_bar_http_codes(
                                                      http_codes_by_classification[-1]["total"]),
                                                  config={"displaylogo": False, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                                    ]),
                            ])
                    ]
                )])])

"""

Layout of the tab acces

"""

tab_acces = html.Div(
    id='container_father_access_websites',
    style={'backgroundColor': '#f6f6f6',
           'display': 'flex', 'flexDirection': 'column'},
    children=[
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(
                            children=[
                                dcc.Graph(id="histogram_ok_not_ok",
                                          className="plot_ok_not_ok",
                                          figure=create_pie_chart(
                                                      [23000, 3000], ['OK', 'Not OK'], "Access Websites"),
                                          config={"displaylogo": False, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                            ]),
                        dcc.RadioItems(
                            id='data-view',
                            options=[
                                {'label': 'HTTP Codes response',
                                 'value': 'codes'},
                                {'label': 'Exceptions',
                                 'value': 'exceptions'},
                                {'label': 'Problematic extensions',
                                 'value': 'extensions'},
                            ],
                            value='codes',
                            labelStyle={
                                'display': 'inline-block',  'margin': '5px'},
                            style={'height': 'auto', 'display': 'flex', 'flexWrap': 'wrap', 'textAlign': 'center', 'justifyContent': 'center', 'alignItems': 'center',
                                   'border': '1px solid #d6d6d6', 'width': '35vw',
                                   'backgroundColor': 'white', 'margin': '7px auto'
                                   }
                        ),
                        dcc.Graph(
                            id='plot_to_change',
                            figure=create_px_bar_http_codes(http_codes,
                                                            http_codes_count,
                                                            "HTTP Codes",
                                                            "Count",
                                                            "HTTP Codes response count recieved",
                                                            '#7bc0f7'),
                            style={'height': '750px', 'margin': '1%', 'border': '1px solid #808080',
                                   'maxHeight': 'inherit'},
                            config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                        ),
                    ]
                )
            ]

        )])


"""

Layout of Homepages -> JavaScript

"""

tab_javascript = html.Div(
    id='container_father_access_websites',
    style={'display': 'flex', 'flex-direction': 'column', 'background': 'white'},
    children=[
        html.Div(
            style={'backgroundColor': '#f6f6f6',
                   'display': 'flex', 'flexDirection': 'column'},
            children=[
                html.Div(
                    children=[
                        dcc.RadioItems(
                            id='data_view_javascript',
                            options=[
                                {'label': 'Generic',
                                 'value': 'generic'},

                                {'label': 'Universities',
                                 'value': 'universities'},

                                {'label': 'Institutions',
                                 'value': 'institutions'},

                                {'label': 'Life Sciences',
                                 'value': 'lifesciences'},

                                {'label': 'Tools Collections',
                                 'value': 'collections'},

                                {'label': 'Total Dynamic Sites',
                                 'value': 'total'},

                            ],
                            value='generic',
                            labelStyle={
                                'display': 'inline-block',  'margin': '5px'},
                            style={'height': 'auto', 'display': 'flex', 'flexWrap': 'wrap', 'textAlign': 'center', 'justifyContent': 'center', 'alignItems': 'center',
                                   'border': '1px solid #d6d6d6', 'width': '35vw',
                                   'backgroundColor': 'white', 'margin': '7px auto'
                                   }
                        ),
                        dcc.Graph(id='histogram_dynamic_percentages',

                                  className='six columns',
                                  style={'height': '750px', 'margin': '1%', 'border': '1px solid #808080',
                                         'maxHeight': 'inherit'},
                                  config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                        dcc.Graph(id='boxplot_plot',
                                  className='six columns',
                                  style={'height': '750px', 'margin': '1%', 'border': '1px solid #808080',
                                         'maxHeight': 'inherit'},
                                  config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                    ]
                )]
        )])


"""

Callback for the tabs of domains, acces and javascript:

"""


@app.callback(Output('tabs-content-inline', 'children'),
              [Input('tabs-styled-with-inline', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return tab_domains
    elif tab == 'tab-2':
        return tab_acces
    elif tab == 'tab-3':
        return tab_javascript


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
    all_http_codes, all_ssl_results, all_bioschema_results, all_http_codes_for_hist, all_http_codes_for_hist = get_initial_values_for_update()
    final_values_http = [0, 0]
    final_values_ssl = [0, 0]
    final_values_bioschema = [0, 0]
    final_dict_http_codes = {
        x: 0 for x in http_codes_by_classification[-1]["total"]}
    if not values:
        return create_pie_chart(final_values_http, ['HTTPS', 'HTTP'], "HTTP vs HTTPS"), create_pie_chart(final_values_bioschema, ['Bioschemas', 'No bioschemas'], "BIOSCHEMAS"), create_pie_chart(final_values_ssl, ['SSL', 'No SSL'], "SSL Certificates"),  create_bar_http_codes(final_dict_http_codes), create_histogram_domains(values, domains, values_36)
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
        return create_pie_chart(final_values_http, ['HTTPS', 'HTTP'], "HTTP vs HTTPS"), create_pie_chart(final_values_bioschema, ['Bioschemas', 'No bioschemas'], "BIOSCHEMAS"), create_pie_chart(final_values_ssl, ['SSL', 'No SSL'], "SSL Certificates"), create_bar_http_codes(final_dict_http_codes), create_histogram_domains(values, domains, values_36)
    return create_pie_chart(metrics_bioschemas_ssl_https_by_classification[-1]["total"]["https"], ['HTTPS', 'HTTP'], "HTTP vs HTTPS"), create_pie_chart(metrics_bioschemas_ssl_https_by_classification[-1]["total"]["bioschemas"], ['Bioschemas', 'No bioschemas'], "BIOSCHEMAS"), create_pie_chart(metrics_bioschemas_ssl_https_by_classification[-1]["total"]["ssl"], ['SSL', 'No SSL'], "SSL Certificates"), create_bar_http_codes(http_codes_by_classification[-1]["total"]), create_histogram_domains(
        ['Universities', 'Institutional', 'Tools Collections', 'Generic',  'Life Sciences', 'others'], domains, values_36)


"""
Callback for tab access:
"""


@app.callback(dash.dependencies.Output('plot_to_change', 'figure'),
              [dash.dependencies.Input('data-view', 'value')])
def update_fig(value):
    if value == "codes":
        return create_px_bar_http_codes(http_codes,
                                        http_codes_count,
                                        "HTTP Codes",
                                        "Count",
                                        "HTTP Codes response count recieved",
                                        '#7bc0f7')
    elif value == "exceptions":
        return create_px_bar_horizontal(exceptions,
                                        exceptions_count,
                                        "Count",
                                        "Exceptions",
                                        "Exceptions count recieved",
                                        '#7bc0f7',)
    elif value == "extensions":
        return create_px_bar_horizontal(problematics_extensions,
                                        problematic_extensions_count,
                                        "Count",
                                        "Problematic extensions",
                                        "Problematic extensions count recieved",
                                        '#7bc0f7')


"""
Callback for tab JavaScript:
"""


@app.callback([Output('boxplot_plot', 'figure'), Output('histogram_dynamic_percentages', 'figure'), Output('boxplot_plot', 'style')],
              [dash.dependencies.Input('data_view_javascript', 'value')])
def update_fig(value):
    if value == "generic":
        return create_box_plot("Generic Repositories", *dynamic_percentages_groupation[0]['dynamic_percentages'][4]["generic"]), create_df_and_fig_bar_dynamic_percentages(extract_number_of_domains(4, 'generic'), "Generic Repositories"), {'height': '750px', 'margin': '1%', 'border': '1px solid #808080',
                                                                                                                                                                                                                                              'maxHeight': 'inherit'}
    elif value == "universities":
        return create_box_plot("Universities", *dynamic_percentages_groupation[0]['dynamic_percentages'][0]['university']), create_df_and_fig_bar_dynamic_percentages(extract_number_of_domains(0, 'university'), "Universities"), {'height': '750px', 'margin': '1%', 'border': '1px solid #808080',
                                                                                                                                                                                                                                    'maxHeight': 'inherit'}
    elif value == "institutions":
        return create_box_plot("Institutions", *dynamic_percentages_groupation[0]['dynamic_percentages'][1]["institucional"]), create_df_and_fig_bar_dynamic_percentages(extract_number_of_domains(1, 'institucional'),  "Institutions"), {'height': '750px', 'margin': '1%', 'border': '1px solid #808080',
                                                                                                                                                                                                                                           'maxHeight': 'inherit'}
    elif value == "lifesciences":
        return create_box_plot("Life Sciences", *dynamic_percentages_groupation[0]['dynamic_percentages'][2]["lifeScience"]), create_df_and_fig_bar_dynamic_percentages(extract_number_of_domains(2, 'lifeScience'),  "Life Sciences"), {'height': '750px', 'margin': '1%', 'border': '1px solid #808080',
                                                                                                                                                                                                                                         'maxHeight': 'inherit'}
    elif value == "collections":
        return create_box_plot("Collections", *dynamic_percentages_groupation[0]['dynamic_percentages'][3]["collections"]), create_df_and_fig_bar_dynamic_percentages(extract_number_of_domains(3, 'collections'), "Collections"), {'height': '750px', 'margin': '1%', 'border': '1px solid #808080',
                                                                                                                                                                                                                                    'maxHeight': 'inherit'}
    elif value == "total":
        return create_box_plot(0), create_df_and_fig_bar_dynamic_percentages(percentages, "the total"), {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=True)
