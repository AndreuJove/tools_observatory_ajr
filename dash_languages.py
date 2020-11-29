import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from graphs import create_pie_chart
import pandas as pd
import dash
import collections
import json


def create_px_bar_animated_frame(df_final, x_value, y_value, title_given):
    fig_animation = px.bar(df_final, x=x_value, y=y_value, 
                            log_x=True, color=y_value, 
                            orientation='h', barmode="overlay",
                            height=850, width=900, animation_frame="Year", 
                            animation_group=y_value, template="simple_white",
                            hover_data={x_value: False,
                                       y_value: False, 
                                       'Year': False},
                            labels={"Cumulative_count" : "Cumulative Count"},
                            hover_name=x_value)
    fig_animation.update_layout(yaxis_categoryorder='total ascending', bargap=0.3,
                                showlegend=False, 
                                title=f"<b>{title_given} ({df_final['Count'].sum():,})<b>", 
                                title_x=0.5)
    fig_animation.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 550
    return fig_animation



path_metrics = "new_input_data/publications.json"
with open(path_metrics, "r") as l:
    publications_json = json.load(l)

df_final_languages = pd.DataFrame(publications_json['df_languages'])

df_publications = pd.DataFrame(publications_json['df_publications'])


def create_scatter_plot_years(series, column_name_1, column_name_2):
    dict_counter = dict(collections.Counter(series.dropna().to_list()))
    df = pd.DataFrame([(int(float(t[0])), t[1]) for t in dict_counter.items()],columns = [column_name_1,column_name_2])
    df = df.sort_values(by=column_name_1).reset_index(drop=True)
    fig = px.line(df, x=column_name_1, 
                        y=column_name_2, 
                        template="simple_white",
                        log_y=True    
                    )
    fig.update_layout(bargap=0.4,
                        title=f"<b>Tools ({df[column_name_2].sum():,}) per {column_name_1}</b>",  
                        title_font_family="Arial", 
                        title_x=0.5)
    fig.update_xaxes(
                        dtick="M5",
                        tickangle=45,
                        tickvals = list(range(int(series.min()), int(series.max()), 5)) + [int(series.max())]
                        )
    return fig

fig_year = create_scatter_plot_years(df_publications['Year'], "Year", "Tools")

def create_scatter_plot_authors(series, column_name_1, column_name_2):
    dict_counter = dict(collections.Counter(series.dropna().to_list()))
    df = pd.DataFrame([(int(float(t[0])), t[1]) for t in dict_counter.items()],columns = [column_name_1,column_name_2])
    df = df.sort_values(by=column_name_1).reset_index(drop=True)
    fig = px.scatter(df, x=column_name_1, 
                        y=column_name_2, 
                        template="simple_white",
                        log_y=True    
                    )
    fig.update_layout(bargap=0.4,
                        title=f"<b>{column_name_1} ({int(series.sum()):,}) per {column_name_2} ({df[column_name_2].sum():,}) </b>",  
                        title_font_family="Arial", 
                        title_x=0.5)
    fig.update_traces(mode='lines+markers')
    return fig

fig_authors = create_scatter_plot_authors(df_publications['Authors'], "Number of Authors", "Tools")


def create_scatter_citations_references(series, column_name_1, column_name_2):
    dict_counter = dict(collections.Counter(series.dropna().to_list()))
    df = pd.DataFrame([(int(float(t[0])), t[1]) for t in dict_counter.items()],columns = [column_name_1, column_name_2])
    df = df.sort_values(by=column_name_1).reset_index(drop=True)
    fig = px.histogram(df, x=column_name_1, 
                        y=column_name_2, 
                        template="simple_white",
                        log_y = True  
                    )
    fig.update_layout(bargap=0.4,
                        title=f"<b>{column_name_1} ({int(series.sum()):,}) per Tool ({df[column_name_2].sum():,}) </b>",  
                        title_font_family="Arial", 
                        title_x=0.5)
    return fig



fig_citations = create_scatter_citations_references(df_publications['Citations'], "Number of Citations", "Tools")

fig_references = create_scatter_citations_references(df_publications['References'], "Number of References", "Tools")

# Dash HTML:
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

app.layout = html.Div(
    id='container_father',
    style={'display': 'flex', 'flex-direction': 'column'},
    children=[
        html.Div(
            className="section-title ",
            children=[
                html.Div(children=["Bioinformatics Tools with registered publication"]),
            ]),
        html.Div(
        id="div_top_dynamic_websites",
        children=[
                    dcc.Graph(
                    id='pie_dynamic_not_dynamic',
                    figure=create_pie_chart(
                                      publications_json['all_tools_vs_tools_publications'], ['Publications', 'No Publications'], "Publications in Bioinformatics Tools"),
                                      config={"displaylogo": False, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),
                    dcc.Markdown(
                            children= '''
                                *We understand for *
                            
                                *tools with a publication*

                                *the ones that has an *
                            
                                *academic article *
                            
                                *published about the tool.*

                            ''')  

                ]),
        html.Hr(style={"margin": "2em"}),
        html.Div(
            style={'textAlign': 'center', "margin" : "2em"},
            children=[
                dcc.Markdown(
                    children=[f'''
                                        *The following plots have being calculated from the **{(publications_json['all_tools_vs_tools_publications'][0]):,}** tools with publication* 
                                        
                                        *from an amount of **{sum((publications_json['all_tools_vs_tools_publications'])):,}** bioinformatics tools.*

                                        '''],  style={"fontSize": "23px"})
            ]
        ),
        html.Div(
            style={'display': 'flex', 'flexDirection': 'row', "width" : "60%", "margin" : "0 auto",
                   'justifyContent': 'space-evenly', 'alignItems': 'center' },
            children=[

                        dcc.Graph(figure=create_px_bar_animated_frame(df_final_languages, 
                                                                    "Cumulative_count", 
                                                                    "Language", 
                                                                    "Evolution of programming languages in Bioinformatics Research Software"),
                                  id="histogram_animation",
                                  style={
                                      "border": "1px solid #808080"},
                                  config={
                                      'displayModeBar': False,
                                      'displaylogo': False,
                                  },
                                  ),
                        dcc.Markdown(
                                        children= '''
                                        *This plot pretends*
                                        
                                        *to find the evolution*

                                        *of the programming*

                                        *languages of the*
                                        
                                        *tools with publication.*
                                        
                                        ''',                                             
                                        )   
                    ]
                ),
        html.Hr(style={"margin": "3em"}),
        html.Div(
            className= "div_markdown",
            children=[
                dcc.Markdown(
                    children=[f'''
                                        Stadistics obtained from the tools with publication.

                                        ''']
                            )               
            ]
        ),
        html.Div(
            style={'display': 'flex'},
            
            children=[
                dcc.Graph(id='line_authors',
                                    figure=fig_authors,
                                  style={'height': '750px', "width" : "950px",'margin': '1% auto', 'border': '1px solid #808080',
                                         'maxHeight': 'inherit'},
                                  config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                                          ),
                dcc.Graph(id='line_years',
                                figure=fig_year,
                                style={'height': '750px', "width" : "950px",'margin': '1% auto', 'border': '1px solid #808080',
                                        'maxHeight': 'inherit'},
                                config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                        'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                                        ),
            ]
        ),

                html.Div(
            style={'display': 'flex'},
            
            children=[
                dcc.Graph(id='px_line_citations',
                                    figure=fig_citations,
                                  style={'height': '750px', "width" : "950px",'margin': '1% auto', 'border': '1px solid #808080',
                                         'maxHeight': 'inherit'},
                                  config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                                          ),
                dcc.Graph(id='px_line_references',
                                figure=fig_references,
                                style={'height': '750px', "width" : "950px",'margin': '1% auto', 'border': '1px solid #808080',
                                        'maxHeight': 'inherit'},
                                config={"displaylogo": False, "displayModeBar": False, "showTips": False,
                                        'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                                        ),
            ]
        ),


            ]
        )
    



if __name__ == '__main__':
    app.run_server(debug=True)
