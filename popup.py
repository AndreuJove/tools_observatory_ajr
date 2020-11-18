import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

def modal():
    return html.Div(
        children=[
            html.Div([
                html.Div(
                    className='modal-text',
                    children=[
                        dcc.Markdown(dedent('''
                        # This is the text that will be in the modal
                        '''))
                    ]
                ),
        ],
        id='modal',
        className='modal',
        style={"display": "none"},
    )
# hide/show modal
@app.callback(Output('modal', 'style'),
              [Input('instructions-button', 'n_clicks')])
def show_modal(n):
    if n > 0:
        return {"display": "block"}
    return {"display": "none"}

# Close modal by resetting info_button click to 0
@app.callback(Output('instructions-button', 'n_clicks'),
              [Input('modal-close-button', 'n_clicks')])
def close_modal(n):
    return 0


if __name__ == '__main__':
    app.run_server(debug=True)