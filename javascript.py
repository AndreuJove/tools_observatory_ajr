import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import graphs

"""
imports to change
"""

path_metrics = "new_input_data/extracted_metrics.json"
with open(path_metrics, "r") as l:
    metrics = json.load(l)

df_total_percentages = pd.read_json("new_input_data/df_years_percentages.json")

# Get external CSS:
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
app.title = "JavaScript"
app.css.append_css(
    {'external_url': 'assets/styles.css'})
app.css.config.serve_locally = False
app.config['suppress_callback_exceptions'] = True
app.prevent_initial_callbacks = True


# Calculate the dynamic static websites.
df_static = df_total_percentages[df_total_percentages['percentage_of_change']<4]
df_javaScript = df_total_percentages[df_total_percentages['percentage_of_change']>4]

df_color_procedence = graphs.fill_df_color_procedence(df_total_percentages)
df_only_years = df_color_procedence[df_color_procedence['year']!= ""]

app.layout = html.Div(
    id='container_father_access_websites',
    style={'display': 'flex', 'flex-direction': 'column', 'backgroundColor': '#f6f6f6'},
    children=[
        html.Div(
            className="section-title ",
            children=[
                html.Div(children=["JavaScript in Websites"])
            ]
        ),
        html.Div(
            id="div_top_dynamic_websites",
            children=[
                        dcc.Graph(
                        id='pie_dynamic_not_dynamic',
                        figure=graphs.create_pie_chart([len(df_static), len(df_total_percentages)-len(df_static)], ['Static', 'Dynamic'], "HTML format websites without errors")),
                        dcc.Markdown(
                                children= '''
                                    **Dynamic websites**
                                
                                    *are considered the*

                                    *ones that JavaScript*
                                
                                    *displays content*
                                
                                    *of the website.*

                                    **Percentage of change**

                                    *is obtained by comparing*

                                    *HTML with and without*
                                
                                    *JavaScript rendered.*  

                                    *The next following plots*

                                    *are being obtained from*

                                    *the dynamic websites.*


                                ''')  

                    ]),
        html.Hr(style={"margin": "3em"}),
        html.Div(
            style={'textAlign': 'center'},
            children=[
                dcc.Markdown(
                    children=[f'''
                                        *The following plots have being calculated from the **{len(df_javaScript)}** dynamic websites.* 

                                        '''],  style={"fontSize": "23px"})
            ]
        ),
        html.Div(style={"margin" : "1em"}),
        
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
                                  style={'margin': '1%', 'border': '1px solid #808080',
                                         'maxHeight': 'inherit'},
                                  config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                        dcc.Graph(id='boxplot_plot',
                                  className='six columns',
                                  style={'margin': '1%', 'border': '1px solid #808080',
                                         'maxHeight': 'inherit'},
                                  config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                    ]),

                        # html.Div(
                        #     id="div_scatter_plot_markdown",
                        #     children=[
                        #         dcc.Graph(id='scatter_plot',
                        #             figure=graphs.create_scatter_plot(df_only_years),
                        #           style={'height': '750px', "width" : "950px",'margin': '1% auto', 'border': '1px solid #808080',
                        #                  'maxHeight': 'inherit'},
                        #           config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                        #                   'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                        #                   ),

                        #         dcc.Markdown(
                        #                     children= '''
                        #                     *This plot pretends*
                                            
                        #                     *to find correlationship*

                        #                     *between the Year of*

                        #                     *publication of the*
                                            
                        #                     *tool and the percentage*

                        #                     *of change of the*

                        #                     *website of the tool.*''',                                             
                        #                     )     
                        #             ]
                        # )
                    ]
                )]
        )


"""
Callback for tab JavaScript:
"""

@app.callback([ Output('boxplot_plot', 'figure'), 
                Output('histogram_dynamic_percentages', 'figure'), 
                Output('boxplot_plot', 'style')
                ],
              [Input('data_view_javascript', 'value')])
def update_histogram_box_plot(value):
    if value == "generic":
        return graphs.crate_box_plot_from_df("Generic Repositories", df_javaScript[df_javaScript['domain'].isin(metrics['domains_classification'][4]['generic'])]), graphs.create_fig_bar_percentage_of_change(df_javaScript[df_javaScript['domain'].isin(metrics['domains_classification'][4]['generic'])], "Generic Repositories"), {'height': '750px', 'margin': '1%', 'border': '1px solid #808080','maxHeight': 'inherit'}
    elif value == "universities":
        return graphs.crate_box_plot_from_df("Universities", df_javaScript[df_javaScript['domain'].isin(metrics['domains_classification'][0]['university'])]), graphs.create_fig_bar_percentage_of_change(df_javaScript[df_javaScript['domain'].isin(metrics['domains_classification'][0]['university'])], "Universities"), {'height': '750px', 'margin': '1%', 'border': '1px solid #808080', 'maxHeight': 'inherit'}                                                                                                                                                                                                                              
    elif value == "institutions":
        return graphs.crate_box_plot_from_df("Institutions", 
                                        df_javaScript[df_javaScript['domain'].isin(metrics['domains_classification'][1]['institucional'])]), graphs.create_fig_bar_percentage_of_change(df_javaScript[df_javaScript['domain'].isin(metrics['domains_classification'][1]['institucional'])],  "Institutions"), {'height': '750px', 'margin': '1%', 'border': '1px solid #808080', 'maxHeight': 'inherit'}                                                                                                                                                                                                                                 
    elif value == "lifesciences":
        return graphs.crate_box_plot_from_df("Life Sciences", 
                                        df_javaScript[df_javaScript['domain'].isin(metrics['domains_classification'][2]['lifeScience'])]), graphs.create_fig_bar_percentage_of_change(df_javaScript[df_javaScript['domain'].isin(metrics['domains_classification'][2]['lifeScience'])],  "Life Sciences"), {'height': '750px', 'margin': '1%', 'border': '1px solid #808080', 'maxHeight': 'inherit'}                                                                                                                                                                                                                                    
    elif value == "collections":
        return graphs.crate_box_plot_from_df("Collections", 
                                        df_javaScript[df_javaScript['domain'].isin(metrics['domains_classification'][3]['collections'])]), graphs.create_fig_bar_percentage_of_change(df_javaScript[df_javaScript['domain'].isin(metrics['domains_classification'][3]['collections'])], "Collections"), {'height': '750px', 'margin': '1%', 'border': '1px solid #808080', 'maxHeight': 'inherit'}                                                                                                                                                                                                                            
    elif value == "total":
        return graphs.crate_box_plot_from_df("Collections", 
                                        df_javaScript[df_javaScript['domain'].isin(metrics['domains_classification'][3]['collections'])]), graphs.create_fig_bar_percentage_of_change(df_javaScript, "the total"), {'display': 'none'}

if __name__ == '__main__':
    app.run_server(debug=True)
