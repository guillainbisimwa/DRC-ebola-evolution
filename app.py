import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import math

df2 = pd.read_csv(
    'Data_ DRC.1.csv')

df = pd.read_csv(
    'Data_ DRC Ebola Outbreak, North Kivu and Ituri - MOH-By-Health-Zone.csv')


def generate_table(dataframe): #max_rows=5
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), len(dataframe)))]
    )

def result_over_time():
    return (
        dcc.Graph(
            id='rot-graph',
            figure={
                'data': [
                     go.Scatter(
                                    x = [ report_date for report_date in df["report_date"].unique() ],
                                    y = [cc for cc in df["confirmed_deaths"]],
                                    line = {"color": "rgb(53, 83, 255)"},
                                    mode = "lines",
                                    name = "confirmed_deaths"
                                ),
                    # {
                    #     'x': [ report_date for report_date in df["report_date"].unique() ],
                    #     'y': [cc for cc in df["confirmed_deaths"]],
                    #     'type': 'bar', 'name': 'confirmed_deaths'
                    # },
                   
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        )
    )

external_scripts = [
    'assets/material.min.js'
]

# external CSS stylesheets
external_stylesheets = [
    'assets/material.min.css',
    'assets/bWLwgP.css'
]

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[

    # header
    html.Div([
        html.H3("The epidemiological situation of the Ebola Virus (DRC) from 2018-08-04 to 2019-02-21", 
        className='mdl-layout--large-screen-only mdl-pad-to-bottom-50'),
        ],
        className="m-botm-20 mdl-layout__header mdl-color--pink-800"
    ),

    # generate_table(df),
    html.Section([
        html.Div([
            # html.Label('Selectionner la datte',
            # className="mdl-cell mdl-cell--6-col"),
            dcc.Dropdown(
                id='datte-id',
                options=[{'label': report_date, 'value': report_date} for report_date in df['report_date'].unique()],
                value='2019-02-20',
                className="mdl-my-input"
            ),
            html.Div(id='datte-div'),
            html.P("\
                The first graph allows you to see the situation at a desired date. \
                And to understand which health zone is most affected in terms of confirmed cases \
                and cases of death confirms.",
                    className="mdl-my-input"
                ),
            ],
            className="mdl-card mdl-cell mdl-cell--12-col"
        ),
        ],
        className="section--center mdl-grid mdl-grid--no-spacing mdl-shadow--2dp my_section"
    ),

    html.Section([
        html.Div([
            result_over_time(),
            ],
            className="mdl-card mdl-cell mdl-cell--12-col"
        ),
        ],
        className="section--center mdl-grid mdl-grid--no-spacing mdl-shadow--2dp my_section"
    ),

    # html.H2(children='''First question.'''),
    # html.Div(children="(10 zones de sante les plus touchees depuis l'epidemie d'ebola)"),
    #result_over_time()
],
className="mdl-color--grey-100")

@app.callback(
    Output(component_id='datte-div', component_property='children'),
    [Input(component_id='datte-id', component_property='value')]
)
def selected_datte_output_div(selected_datte):
    #   return 'You\'ve entered "{}"'.format(selected_datte)
    filtered_df = df[df.report_date == selected_datte]
    return (
        dcc.Graph(
            id='cc-by-cd-graph',
            figure={
                'data': [
                    {
                        'x': [health_zone for health_zone in filtered_df["health_zone"]],
                        'y': [cc for cc in filtered_df["confirmed_cases"]],
                        'type': 'bar', 'name': 'Confirmed cases'
                    },
                    {
                        'x': [health_zone for health_zone in filtered_df["health_zone"]],
                        'y': [cc for cc in filtered_df["confirmed_deaths"]],
                        'type': 'bar', 'name': 'Confirmed deaths'
                    }
                ],
                'layout': {
                    'title': 'DRC Ebola Outbreak, North Kivu and Ituri - MOH-By-Health-Zone on {}'.format(selected_datte)
                }
            }
        )
    )

if __name__ == '__main__':
    app.run_server(debug=True)