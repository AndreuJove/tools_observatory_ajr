


import json
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import graphs
import plotly.graph_objects as go



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


# Colors for all pies chart:
colors = ['#1976d3', '#64b5f6']

def create_pie_chart_button(values_list, labels_list, title_pie):
    # Function create pie_chart in:
    pie = go.Figure(
        data=[go.Pie(labels=labels_list, values=values_list, hole=0.55)])
    pie.update_traces(hoverinfo='value', marker=dict(colors=colors))
    pie.update_layout(title=f"<b>{title_pie} ({int(sum(values_list)):,})</b>", title_x=0.5,
                      legend_orientation="h", title_font_family="Arial", title_font_color="#383838")


    return pie




app.layout = dbc.Card(
    
    children=[
        dbc.CardBody(
            
            [
                html.H4("Graffiti in Berlin 2012-2019", className="card-title", style={"text-align": "center"}),
                html.Div(
                    children=[html.Img(
                                        id="popover-bottom-target",
                                        src="images/question-circle-solid.svg",
                                        n_clicks=0,
                                        className="info-icon",
                                        style={"margin": 0},
                                    )
                    ]
                ),
                # dbc.Button(
                #     "About Berlin", id="popover-bottom", color="danger"
                # ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("All About Berlin:"),
                        dbc.PopoverBody(
                            "Berlin (/bɜːrˈlɪn/; German: [bɛʁˈliːn] is the capital and largest city of Germany by both area and population. Its 3,769,495 (2019) inhabitants make it the most populous city proper of the European Union. The city is one of Germany's 16 federal states. It is surrounded by the state of Brandenburg, and contiguous with Potsdam, Brandenburg's capital. The two cities are at the center of the Berlin-Brandenburg capital region, which is, with about six million inhabitants and an area of more than 30,000 km2, Germany's third-largest metropolitan region after the Rhine-Ruhr and Rhine-Main regions. (Wikipedia)"),
                    ],
                    id="popover",
                    target="popover-bottom-target",  # needs to be the same as dbc.Button id
                    placement="bottom",
                    is_open=False,
                ),
                dcc.Graph(id='line_chart', figure=create_pie_chart_button(
                                        graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["https"], ['HTTPS', 'HTTP'], "HTTP vs HTTPS")),

            ]
        ),
    ],
    color="light",
)



@app.callback(
    Output("popover", "is_open"),
    [Input("popover-bottom-target", "n_clicks")],
    [State("popover", "is_open")],
)
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open

# app.layout = html.Div(
#                     children=[
#                         dcc.Graph(id="pie_chart_1",
#                                     className="little_plots",
#                                     figure=create_pie_chart_button(
#                                         graphs.metrics["bioschemas_ssl_https_license"][-1]["total"]["https"], ['HTTPS', 'HTTP'], "HTTP vs HTTPS"),
#                                     config={"displaylogo": False, "displayModeBar": False, "showTips": False,
#                                           'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
#                         )
#                     ])

if __name__ == '__main__':
    app.run_server(debug=True)