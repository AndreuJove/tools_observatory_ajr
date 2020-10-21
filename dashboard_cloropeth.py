import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

app = dash.Dash(__name__,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])

df = pd.read_json(
    'input_data/df_countries_code.json')

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
    colorbar_title='Number of authors',
))

fig.update_layout(
    title_text='TOOLS AUTHORS PROCEDENCES',
    title_font_size=30,
    geo=dict(
        showframe=True,
        showcoastlines=False,
        projection_type='equirectangular'
    ),

)

app.layout = html.Div(
    style={'width': '90%', 'backgroundColor': '#f6f6f6', },
    children=[
        dcc.Graph(figure=fig,
                  style={'height': '850px',
                         'backgroundColor': '#f6f6f6'},
                  config={"displaylogo": False,
                          'modeBarButtonsToRemove': ['pan2d', 'lasso2d']}
                  )])


if __name__ == '__main__':
    app.run_server(debug=True)



