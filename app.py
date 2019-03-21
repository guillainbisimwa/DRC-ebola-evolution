import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objs as go

df2 = pd.read_csv(
    'Data_ DRC.1.csv')

df = pd.read_csv(
    'Data_ DRC Ebola Outbreak, North Kivu and Ituri - MOH-By-Health-Zone.csv')

df_clean = df.drop(columns=['publication_date', 'report_date','country', 'province','health_zone', 'confirmed_cases_change',
'probable_cases_change', 'total_cases_change','confirmed_deaths_change', 'total_deaths_change','total_suspected_cases_change', 'source'])

def generate_table(dataframe):

    dataframe = df[df.report_date.str.contains("2019-03-19")]
    dataframe = dataframe.astype({"confirmed_cases": int,"probable_cases": int})

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), len(dataframe)))]
    )
def gen(selected_datte):
    dataframe = df[df.report_date.str.contains(selected_datte)]
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
def result_all_in_one():
    filtered_df = df[df.report_date == "2019-03-19"]
    return (
        dcc.Graph(
            id='life-exp-vs-gdp',
            figure={
                'data': [
                    go.Scatter(
                        x=filtered_df[filtered_df['province'] == i]['total_cases'],
                        y=filtered_df[filtered_df['province'] == i]['confirmed_deaths'],
                        text=filtered_df[filtered_df['province'] == i]['health_zone'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 15,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df.province.unique()
                ],
                'layout': go.Layout(
                    xaxis={'type': 'log', 'title': 'GDP Per Capita'},
                    yaxis={'title': 'Life Expectancy'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            }
        )
    )

def final_stat():
    # filter df by province
    #take the last day
    filtered_df = df[df.report_date == df['report_date'][df.index[1]]]
    filtered_df_nk = filtered_df[filtered_df.province == "North Kivu"]

    filtered_df_it = filtered_df[filtered_df.province == "Ituri"]
    # sum all confirmed case
    filtered_df_nk = filtered_df_nk.astype({"confirmed_cases": int,"probable_cases": int
        ,"confirmed_deaths":int,"total_suspected_cases":int})

    filtered_df_it = filtered_df_it.astype({"confirmed_cases": int,"probable_cases": int
        ,"confirmed_deaths":int,"total_suspected_cases":int})
        # sum all suspected cases
    get_sum_nk = filtered_df_nk.sum(axis = 0, skipna = True)
    get_sum_it = filtered_df_it.sum(axis = 0, skipna = True)
    # the same to sc

    data_nk= [
        {
            'values': [get_sum_nk["confirmed_cases"], get_sum_nk["confirmed_deaths"]],
            'type': 'pie',
            'labels': ['N-K Confirmed cases ','N-K Confirmed deaths'],
            'textfont': {'size': 20}
        },
    ]

    data_it = [
        {
            'values': [get_sum_it["confirmed_cases"], get_sum_it["confirmed_deaths"]],
            'type': 'pie',
            'labels': ['Ituri Confirmed cases','Ituri Confirmed deaths'],
            'textfont': {'size': 20}
     
        },
    ]

    return html.Div([
        html.Div([
            dcc.Graph(
                id='graph1',
                figure={
                    'data': data_nk,
                    'layout': {
                        'margin': {
                            'l': 30,
                            'r': 0,
                            'b': 30,
                            't': 0
                        },
                        'legend': {'x': 0, 'y': 1}
                    }
                },
                className="fleft mdl-cell--6-col"
            ),
        ]),
        html.Div([
            dcc.Graph(
                id='graph2',
                figure={
                    'data': data_it,
                    'layout': {
                        'margin': {
                            'l': 30,
                            'r': 0,
                            'b': 30,
                            't': 0
                        },
                        'legend': {'x': 0, 'y': 1}
                    }
                },
                className="fleft mdl-cell--6-col"
            )
        ])
    ])

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
server = app.server

app.layout = html.Div(children=[

    # header
    html.Div([
        html.H3("The outbreak situation of the Ebola Virus (DRC) from 2018-08-04 to 2019-03-19", 
        className='mdl-layout--large-screen-only mdl-pad-to-bottom-50'),
        ],
        className="m-botm-20 mdl-layout__header mdl-color--pink-800"
    ),

    # generate_table(df),

    html.Section([
        html.Div([
            dcc.Dropdown(
                id='datte-id',
                options=[{'label': report_date, 'value': report_date} for report_date in df['report_date'].unique()],
                value='2019-03-19',
                className="mdl-my-input"
            ),
            html.Div(id='datte-div'),
            html.P("\
                Do you want to see what were the daily situation of health areas\
                in terms of confirmed cases and confirmed death?",
                    className="mdl-my-input qst"
                ),
            html.P("\
                The first graph allows you to see the situation at a selected date. \
                And to understand which health zone is most affected in terms of confirmed cases \
                and death confirms cases.",
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
            dcc.Dropdown(
                id='province-id-2',
                options=[{'label': prvc, 'value': prvc} for prvc in df['province'].unique()],
                value='North Kivu',
                className="mdl-my-input"
            ),
            html.Div(id='datte-div-2'),
            html.P("\
                Do you want to see the number of people with Ebola per provinve per month,\
                confirmed by the laboratory?",
                    className="mdl-my-input qst"
                ),
            html.P("\
                Here we see the cumulative confirmed cases,\
                the monthly cumulative confirmed deaths,and\
                the monthly cumulative suspected cases.",
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
            final_stat(),
            html.P("\
                What is the proportion of confirmed deaths compared to confirmed cases?",
                    className="mdl-my-input qst"
                ),
            html.P("\
                On the left I show you the report of confirmed deaths compared to confirmed cases\
                of the North Kivu province.\
                On the right I show you the report of confirmed deaths compared to confirmed \
                cases of the Ituri province.\
                Only you can see in which province has there been much more deaths \
                compared to the confirmed cases.",
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
            html.Div([
                html.Div([
                    html.Label('Select one or more provinces'),
                    dcc.Dropdown(
                        id='province-column',
                        options=[{'label': i, 'value': i} for i in df["province"].unique()[1:]],
                        value= [i for i in df["province"].unique()[1:]],
                        multi=True
                    )
                ],
                style={'width': '28%', 'float': 'left', 'display': 'inline-block','margin':'2%'}),

                html.Div([
                    html.Label('Chose the first case'),
                    dcc.Dropdown(
                        id='1axis-column',
                        options=[{'label': column, 'value': column} for column in df_clean.columns],
                        value='confirmed_cases'
                    )
                ],style={'width': '28%', 'float': 'left', 'display': 'inline-block','margin':'2%'}),

                html.Div([
                    html.Label('Chose the second case'),
                    dcc.Dropdown(
                        id='2axis-column',
                        options=[{'label': column, 'value': column} for column in df_clean.columns],
                        value='confirmed_deaths'
                    )
                ],style={'width': '28%', 'float': 'left', 'display': 'inline-block','margin':'2%'})
            ]),

            html.Div(id='indicator-graphic'),
            
            dcc.Slider(
                id='month-slider',
                min=0,
                max=len(load_by_mounth())-2,
                marks=[load_by_mounth_ for load_by_mounth_ in reversed(load_by_mounth())],
                value=len(load_by_mounth())-2,
                className='mdl-pad-to-bottom-30'
            ),
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
    [Input(component_id='province-id-2', component_property='value')]
)
def suspected_over_confirmed(province):
    filtered_df = df[df.province.str.match(province)]
    #filtered_df = df
    tab_sc = [] #suspected
    tab_cc = [] # confirmed case
    tab_cd = [] # death confirmed
    for m in load_by_mounth():
        # transform m to the last day of the month form
        m_ = gen(m)
        # filter result by the last day of the month
        df_filtered_b_m = filtered_df[filtered_df.report_date.str.contains(m_)]
        df_filtered_b_m = df_filtered_b_m.astype({"confirmed_cases": int,"probable_cases": int
        ,"confirmed_deaths":int,"total_suspected_cases":int})

        # sum all suspected cases
        get_sum = df_filtered_b_m.sum(axis = 0, skipna = True)
       
        tab_cc.append(df_filtered_b_m.sum(axis = 0, skipna = True)["confirmed_cases"])
        tab_sc.append(df_filtered_b_m.sum(axis = 0, skipna = True)["total_suspected_cases"])
        tab_cd.append(df_filtered_b_m.sum(axis = 0, skipna = True)["confirmed_deaths"])


        # sum all confirmed cases
    return (
        dcc.Graph(
            id='s-c-by-cd-graph',
            figure={
                'data': [
                    {
                        'x': [load_by_mounth_ for load_by_mounth_ in load_by_mounth()],
                        'y': [cc for cc in tab_cc],
                        'type': 'lines', 'name': 'Confirmed cases'
                    },
                    {
                        'x': [load_by_mounth_ for load_by_mounth_ in load_by_mounth()],
                        'y': [cd for cd in tab_cd],
                        'type': 'lines', 'name': 'Confirmed deaths'
                    },
                     {
                        'x': [load_by_mounth_ for load_by_mounth_ in load_by_mounth()],
                        'y': [sc for sc in tab_sc],
                        'type': 'area', 'name': 'Suspected cases'
                    }
                ],
                'layout': {
                    'title': 'DRC Ebola Outbreak, {} province'.format(province)
                }
            }
        )
    )

@app.callback(
    Output(component_id='indicator-graphic', component_property='children'),
    [
        Input(component_id='province-column', component_property='value'),
        Input(component_id='1axis-column', component_property='value'),
        Input(component_id='2axis-column', component_property='value'),
        Input(component_id='month-slider', component_property='value')
    ]
)
def update_graph(province_clbk,axis_column1,axis_column2,month_slider):
    filtered_df = df[df['province'].isin(province_clbk)]
   
    # transform m to the last day of the month form
    m_ = gen(load_by_mounth()[len(load_by_mounth()) - month_slider - 1])
    # filter result by the last day of the month
    filtered_df = filtered_df[filtered_df.report_date.str.contains(m_)]
    return (
        dcc.Graph(
            id='cc-by-cd-graph1',
            figure={
                'data': [
                    {
                        'x': [health_zone for health_zone in filtered_df["health_zone"]],
                        'y': [cc for cc in filtered_df[""+axis_column1]],
                        'type': 'bar', 'name': ''+axis_column1
                    },
                    {
                        'x': [health_zone for health_zone in filtered_df["health_zone"]],
                        'y': [cc for cc in filtered_df[""+axis_column2]],
                        'type': 'bar', 'name': ''+axis_column2
                    }
                ],
                'layout': {
                    'title': 'DRC Ebola Outbreak, North Kivu and Ituri - MOH-By-Health-Zone on {}'.format(province_clbk)
                }
            }
        )
    )
 

if __name__ == '__main__':
    app.run_server(debug=True)
