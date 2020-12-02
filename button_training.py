


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
    style={"width" : "400px", "border" : "1px solid #808080", "margin" : "10px auto"},
    
    children=[
        dbc.CardBody(
            
            [
                html.Div(
                    style={"height" : "27px", "backgroundColor" : "white"},
                    children=[html.Img(
                                        id="popover-bottom-target",
                                        src="assets/boton-de-informacion.svg",
                                        n_clicks=0,
                                        className="info-icon",
                                        style={"margin": "5px"},
                                    )
                    ]
                ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("HTTP vs HTTPS"),
                        dbc.PopoverBody(
                            children=[
                                html.P("HTTP: unsecured Hypertext Transfer Protocol. Does not require domain validation. No encryption."),
                                html.P("HTTPS: secure Hypertext Transfer Protocol. Requires domain validation. Encryption."),
                            
                            ],
                            style={"padding" : "15px"}
                            ),
                    ],
                    id="popover",
                    target="popover-bottom-target",  # needs to be the same as dbc.Button id
                    placement="bottom",
                    is_open=False,
                    style={"backgroundColor" : "white"}
                ),
                dcc.Graph(id='line_chart', 
                            
                            figure=create_pie_chart_button(
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