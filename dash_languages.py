import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
from graphs import create_pie_chart
import pandas as pd
import dash


def create_px_bar_animated_frame(df_final, x_value, y_value, title_given):
    fig_animation = px.bar(df_final, x=x_value, y=y_value, log_x=True, color=y_value, orientation='h', barmode="overlay",
                           height=850, width=900, animation_frame="Year", animation_group=y_value, template="simple_white",
                           hover_data={x_value: False,
                                       y_value: False, 'Year': False},
                           hover_name=x_value)
    fig_animation.update_layout(yaxis_categoryorder='total ascending', bargap=0.3,
                                # xaxis_autorange=False,
                                showlegend=False, title=f"{title_given} ({df_final['Count'].sum()})", title_x=0.5)
    fig_animation.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 550
    # fig_animation.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 500
    # fig_animation.layout.updatemenus[0].buttons[0].args[1]["frame"]["redraw"] = False
    return fig_animation

df_final_languages = pd.read_json(
    '../bbdd_jmf/final_df_languages.json')
df_final_domains = pd.read_json('../bbdd_jmf/final_df_domains.json')

# print(
#     fig_animation_languages.layout.updatemenus[0].buttons[0].args[1]["frame"])
# # for t in fig_animation_languages['layout']['sliders'][0]['steps']:
# #     t['args'][1]['frame']['redraw'] = True
# #     t['args'][1]['frame']['duration'] = 2000
# #     t['args'][1]['transition']['duration'] = 2000
# #     t['method'] = "animate"
# # fig_animation['layout']['sliders'][-1]['steps'][0]['args']['args'][1]['frame']['redraw'] = True

# print(fig_animation_languages['layout']['sliders'][-1]['steps'][0]['args'][1])
# pprint(vars())

# print(fig_animation['layout']['sliders'][-1]['steps'][0]['args'][1]['frame']['redraw'])


# # Dash HTML:
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
                html.Div(children=["Evolution of Research Software"]),
            ]),
        html.Div(
            style={'display': 'flex', 'flexDirection': 'row',  'textAlign': 'center',
                   'justifyContent': 'center', 'alignItems': 'center', },
            children=[
                html.Div(
                    style={"width": "30%"},
                    children=[
                        dcc.Graph(id="pie_chart_publications",
                                  className="little_plots",
                                  figure=create_pie_chart(
                                      [19559, 42711], ['Publications', 'No Publications'], "Publications in Bioinformatics Tools"),
                                  config={"displaylogo": False, 'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}),

                    ]),
                html.Div(
                    style={"width": "65%", 'display': 'flex', 'flexDirection': 'row',
                           'textAlign': 'center', 'justifyContent': 'center', 'alignItems': 'center', },
                    children=[
                        dcc.RadioItems(
                            id='radio_item_evolution',
                            options=[
                                {'label': 'Languages',
                                 'value': 'languages'},
                                {'label': 'Domains',
                                 'value': 'domains'},
                            ],
                            value='languages',
                            labelStyle={
                                'display': 'inline-block',  'margin': '5px'},
                            style={'height': 'auto', 'display': 'flex', 'flexWrap': 'wrap', 'textAlign': 'center', 'justifyContent': 'center', 'alignItems': 'center',
                                   'border': '1px solid #d6d6d6', 'width': '15vw',
                                   'backgroundColor': 'white', 'margin': '7px auto'
                                   }
                        ),

                        dcc.Graph(figure=create_px_bar_animated_frame(df_final_languages, "Cumulative_count", "Language", "Evolution of programming languages in Bioinformatics Research Software"),
                                  id="histogram_animation",
                                  style={
                                      "border": "1px solid #808080"},
                                  config={
                                      'displayModeBar': False,
                                      'displaylogo': False,
                                  },
                                  ),
                    ]
                )
            ]
        )
    ]
)

@app.callback(dash.dependencies.Output('histogram_animation', 'figure'),
              [dash.dependencies.Input('radio_item_evolution', 'value')])
def update_fig(value):
    if value == "languages":
        return create_px_bar_animated_frame(df_final_languages, "Cumulative_count", "Language", "Evolution of programming languages in Bioinformatics Research Software")
    elif value == "domains":
        return create_px_bar_animated_frame(df_final_domains, "Cumulative_count", "Domain", "Evolution of domains in Bioinformatics Research Software")

if __name__ == '__main__':
    app.run_server(debug=True)
