import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


counter_authors_each_tool_1= {0: 46516, 1: 12148, 3: 228, 2: 1517, 4: 35, 7: 1, 5: 15, 12: 1}
df_authors = pd.DataFrame(counter_authors_each_tool_1.items(), columns=["Number of authors", "Count"]).sort_values(by="Number of authors").reset_index(drop=True)

fig = px.scatter(df_authors, x="Number of authors", y="Count", log_y=True, width=600, height=600, template="simple_white", title="Authors per tool").update_traces(mode="lines+markers")

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])


app.layout = html.Div(

            children=[
                dcc.Graph(

                    figure=fig,
                    config={"displaylogo": False, "displayModeBar" : False, "showTips": False,
                            'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                )])
if __name__ == '__main__':
    app.run_server(debug=True) 