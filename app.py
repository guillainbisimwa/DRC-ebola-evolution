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
    dataframe = df[df.health_zone.str.match("Beni")]

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), len(dataframe)))]
    )
def gen(selected_datte):
    # filtered_df = df[df.report_date.str.match(selected_datte)]
    dataframe = df[df.report_date.str.contains(selected_datte)]
    
    #print(selected_datte)
    print(" Hello :{}",dataframe['report_date'][dataframe.index[0]])
    return dataframe['report_date'][dataframe.index[0]]
    

#load df ordered by month
def load_by_mounth():
    df_m = []
    for m in df['report_date'].unique():
        df_m.append(m[:7])
    output = []
    for x in df_m:
        if x not in output:
            output.append(x)
    return output

def test():
    return html.Div([
        html.H6("Hypothetical growth of $10,000",
                className="gs-header gs-table-header padded"),
        dcc.Graph(
            id="grpah-2",
            figure={
                'data': [
                    go.Bar(
                        x = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"],
                        y = ["10000", "7500", "9000", "10000", "10500", "11000", "14000", "18000", "19000", "20500", "24000"],
                        marker = {
                            "color": "rgb(53, 83, 255)",
                            "line": {
                            "color": "rgb(255, 255, 255)",
                            "width": 2
                            }
                                    },
                        name = "500 Index Fund Inv"
                    ),
                    go.Scatter(
                        x = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"],
                        y = ["1000", "1500", "8000", "10800", "10200", "11000", "1000", "8000", "12000", "20000", "4000"],
                        line = {"color": "rgb(255, 83, 0)"},
                        mode = "lines",
                        name = "5Ala jjjjjj"
                    )
                ],
                'layout': go.Layout(
                    autosize = True,
                    title = "",
                    
                    showlegend = True,
                    xaxis = {
                        "autorange": True,
                        "linecolor": "rgb(0, 0, 0)",
                        "linewidth": 1,
                        "range": [2008, 2018],
                        "showgrid": False,
                        "showline": True,
                        "title": "",
                        "type": "linear"
                    },
                    yaxis = {
                        "autorange": False,
                        "gridcolor": "rgba(127, 127, 127, 0.2)",
                        "mirror": False,
                        "nticks": 4,
                        "range": [0, 30000],
                        "showgrid": True,
                        "showline": True,
                        "ticklen": 10,
                        "ticks": "outside",
                        "title": "$",
                        "type": "linear",
                        "zeroline": False,
                        "zerolinewidth": 4
                    }
                )
            },
            config={
                'displayModeBar': False
            }
        )
    ])
    
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

    #generate_table(df),
    # gen("2018-11"),
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
            # html.Label('Selectionner la datte',
            # className="mdl-cell mdl-cell--6-col"),
            dcc.Dropdown(
                id='datte-id-2',
                options=[{'label': report_mounth, 'value': report_mounth} for report_mounth in load_by_mounth()],
                value='2019-02',
                className="mdl-my-input"
            ),
            html.Div(id='datte-div-2'),
            html.P("\
                COmment ebola a evoluer eau mois de janvier 2048\
                blalllaa\
                blaaaa.",
                    className="mdl-my-input"
                ),
            ],
            className="mdl-card mdl-cell mdl-cell--12-col"
        ),
        ],
        className="section--center mdl-grid mdl-grid--no-spacing mdl-shadow--2dp my_section"
    ),

    # html.Section([
    #     html.Div([
    #         result_over_time(),
    #         ],
    #         className="mdl-card mdl-cell mdl-cell--12-col"
    #     ),
    #     ],
    #     className="section--center mdl-grid mdl-grid--no-spacing mdl-shadow--2dp my_section"
    # ),
    html.Section([
        html.Div([
            test(),
            ],
            className="mdl-card mdl-cell mdl-cell--12-col"
        ),
        ],
        className="section--center mdl-grid mdl-grid--no-spacing mdl-shadow--2dp my_section"
    ),
],
className="mdl-color--grey-100")

@app.callback(
    Output(component_id='datte-div', component_property='children'),
    [Input(component_id='datte-id', component_property='value')]
)
def selected_datte_output_div(selected_datte):
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

# second question
@app.callback(
    Output(component_id='datte-div-2', component_property='children'),
    [Input(component_id='datte-id-2', component_property='value')]
)
def suspected_over_confirmed(selected_datte):
    filtered_df = df[df.report_date.str.match(gen(selected_datte))]
    return (
        dcc.Graph(
            id='s-c-by-cd-graph',
            figure={
                'data': [
                    {
                        'x': [health_zone for health_zone in filtered_df["health_zone"]],
                        'y': [cc for cc in filtered_df["total_suspected_cases"]],
                        'type': 'lines', 'name': 'total_suspected_cases'
                    },
                    {
                        'x': [health_zone for health_zone in filtered_df["health_zone"]],
                        'y': [cc for cc in filtered_df["confirmed_cases"]],
                        'type': 'lines', 'name': 'confirmed_cases'
                    }
                ],
                'layout': {
                    'title': 'DRC Ebola Outbreak, North Kivu and Ituri - MOH-By-Health-Zone on {} mounth'.format(selected_datte)
                }
            }
        )
    )
 

if __name__ == '__main__':
    app.run_server(debug=True)