import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output

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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H3(children='The epidemiological situation of the Ebola Virus Disease from 2018-08-04 to 2019-02-21'),
    # generate_table(df),
    html.Label('Selectionner la datte'),
    dcc.Dropdown(
        id='datte-id',
        options=[{'label': report_date, 'value': report_date} for report_date in df['report_date'].unique()],
        value='2019-02-20'
    ),
    html.Div(id='datte-div'),
    html.H2(children='''First question.'''),
    html.Div(children="(10 zones de sante les plus touchees depuis l'epidemie d'ebola)"),
    # dcc.Graph(
    #     id='example-graph',
    #     figure={
    #         'data': [
    #             {
    #                 'x': [health_zone for health_zone in df["health_zone"]],
    #                 'y': [cc for cc in df["confirmed_cases"]],
    #                 'type': 'bar', 'name': 'Confirmed cases'
    #              },
    #              {
    #                 'x': [health_zone for health_zone in df["health_zone"]],
    #                 'y': [cc for cc in df["confirmed_deaths"]],
    #                 'type': 'bar', 'name': 'Confirmed deaths'
    #              }
                
                
    #         ],
    #         'layout': {
    #             'title': 'Dash Data Visualization'
    #         }
    #     }
    # )
])

@app.callback(
    Output(component_id='datte-div', component_property='children'),
    [Input(component_id='datte-id', component_property='value')]
)
def update_output_div(selected_datte):
    #return 'You\'ve entered "{}"'.format(selected_datte)
    filtered_df = df[df.report_date == selected_datte]

    return (
        dcc.Graph(
            id='example-graph',
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
                    'title': 'Dash Data Visualization on "{}" '.format(selected_datte)
                }
            }
        )
    )


if __name__ == '__main__':
    app.run_server(debug=True)