import json
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import graphs

app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

path_metrics = "new_input_data/countries.json"
with open(path_metrics, "r") as l:
    countries = json.load(l)

df = pd.DataFrame(eval(countries['df_countries']))

#Create figure:
fig = go.Figure(data=go.Choropleth(
                locations=df['CODE'],
                z=df['Count'],
                text=df['Country'],
                colorscale='Blues',
                autocolorscale=True,
                reversescale=True,
                marker_line_color='darkgray',
                marker_line_width=0.5,
                colorbar_title='Number of Tools',
                ))

fig.update_layout(
                    title=f"<b>Tools ({df['Count'].sum():,}) on countries ({len(df):,})</b>",
                    title_x=0.5,
                    legend_orientation="h",
                    title_font_family="Arial",
                    title_font_color="#383838",
                    title_font_size=30,
                    geo=dict(
                        showframe=True,
                        showcoastlines=False,
                        projection_type='equirectangular'
                    ),
)

app.layout = html.Div(
    style={'width': '100%', "alignItems" : "center" },
    children=[
        html.Div(
                className="section-title ",
                children=[
                    html.Div(children=["Tools procedence"])
                        ]
                ),
        html.Div(
                id="div_top_dynamic_websites",
                children=[
                            dcc.Graph(
                                        id='pie_dynamic_not_dynamic',
                                        figure=graphs.create_pie_chart([df['Count'].sum(),
                                                                        countries['total_len_tools']-df['Count'].sum()],
                                                                        ['Tools found procedence', 'Tools not found procedence'],
                                                                        "Total Tools")),
                            dcc.Markdown(
                                        children= '''
                                            *The procedence of the tools*
                                        
                                            *has been tracked using*

                                            *the Institution documented*
                                        
                                            *of the tool and the*
                                        
                                            *domain of the emails*

                                            *of the Authors.*
                                                    '''
                                        )
                    ]),
        html.Div(style={"margin" : "4em"}),
        html.Div(
            children=[
                        dcc.Graph(figure=fig,
                                style={'height': '850px',
                                        "width" : "90%", "margin" : "0 auto"},
                                config={"displaylogo": False,
                                        'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                                ),
                  ]),
        html.Div(style={"margin" : "4em"})
                ])

if __name__ == '__main__':
    app.run_server(debug=True)
