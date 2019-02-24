import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output


df = pd.read_csv(
    'Data_ DRC Ebola Outbreak, North Kivu and Ituri - MOH-By-Health-Zone.csv')

def generate_table(dataframe, max_rows=5):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def generate_table2(dataframe, max_rows=5):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[


    html.Label('Dropdown'),
    dcc.Dropdown(
        options=[{'label': report_date, 'value': report_date} for report_date in df['report_date'].unique()],
        value='2019-02-20'
    ),
   
    dcc.Input(id='my-id', value='initial value', type='text'),
    html.Div(id='my-div'),
    html.H4(children='The epidemiological situation of the Ebola Virus Disease from 2018-08-04 to 2019-02-21'),
    generate_table2(df),
    # html.H4(children='The epidemiological situation of the Ebola Virus Disease'),
    # generate_table(df)
])

@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)