from datetime import date
import datetime
import time 
import pandas as pd
import numpy as np 
import dash
import dash_table
import dash_core_components as dcc
import plotly.graph_objs as go
import plotly.express as px
import dash_html_components as html
from dash.dependencies import Input, Output
from app import app
from apps import functions as fx
from app import dbc


#shifts definition
schedule=['12PM','01PM', '02PM', '03PM', '04PM', '05PM', '06PM', '07PM']

#reference is used infront of every single id of each one of the elements of the layout, to avoid duplicate callbacks
reference='Sorting Afternoon shift'
#refreshing time establishes the amount of time by each callback
refreshing_time=1*60*1000 #millisecods


input_day=str(datetime.date.today())[5:10]
file_name='archive/Sorting/'+input_day+reference+'.xlsx'

main=pd.read_excel(file_name,sheet_name='main').round(2).T[:-1].T
aux=pd.read_excel(file_name,sheet_name='aux')
temp=schedule
temp.append('Rates')
df=pd.read_excel(file_name,sheet_name='main')[temp]
results_table=pd.read_excel(file_name,sheet_name='results_table').iloc[:,1:]
floors_table=pd.read_excel(file_name,sheet_name='floors_table')

fig2 = px.bar(floors_table, x='level', y=reference[8:],color=reference[8:],text=reference[8:],color_continuous_scale=['#060000','#EC9C08','#F71802'])
fig=px.line(aux, x='hours', y='Total', title='Total Performance curve')
fig.add_trace(go.Scatter(x=aux.hours, y=[float(main[main['Name']=='Total']['Rates']) for i in aux.index],
                        mode='lines',
                        name="Average {:,.2f} ilpns/hour".format(float(main[main['Name']=='Total']['Rates']))))

def layout():
    return(
        html.Div(
            [   
                html.H1('Sorting '+reference[8:],style={'text-align':'center'}),
                html.H2(id=reference+'time_update',children='',style={'text-align':'center'}),
                html.Div([
                    html.Div(dcc.DatePickerSingle(id=reference+'my-date-picker-single',
                                                    min_date_allowed=datetime.datetime(2020,8,1),
                                                    max_date_allowed=datetime.date.today(),
                                                    initial_visible_month=datetime.date.today(),
                                                    date=str(datetime.date.today())
                                                    )),
                    dash_table.DataTable(   id=reference+'results_table',
                                                columns=[{"name": i, "id": i} for i in results_table.columns],
                                                data=results_table.to_dict('records'),
                                                style_cell={'textAlign': 'center','whiteSpace': 'normal', 'textOverflow': 'ellipsis','font_size': '22px','fontWeight': 'bold'},
                                                style_data_conditional=
                                                        [
                                                            {
                                                                'if': 
                                                                {
                                                                    'filter_query': '{Difference} < 0',
                                                                    'column_id': ['Difference','Net Results','Expected Results']
                                                                },
                                                                'backgroundColor': 'tomato',
                                                                'color': 'white'
                                                            }
                                                        ]
                                                        +
                                                        [
                                                            {
                                                                'if': 
                                                                {
                                                                    'filter_query': '{Difference} >= 0',
                                                                    'column_id': ['Difference','Net Results','Expected Results']
                                                                },
                                                                'backgroundColor': 'green',
                                                                'color': 'white'
                                                            }
                                                        ]
                                            ),
                html.Br(),
                dash_table.DataTable( id=reference+'main_table',
                                                columns=[{"name": i, "id": i} for i in main.columns[1:]],
                                                data=main.to_dict('records'),
                                                editable=False,
                                                sort_action="native",
                                                column_selectable="single",
                                                selected_columns=[],
                                                selected_rows=[],
                                                page_action="native",
                                                page_current= 0,
                                                page_size= 100,
                                                style_cell={'textAlign': 'center','whiteSpace': 'normal', 'textOverflow': 'ellipsis'},
                                                style_data_conditional=
                                                    [ 
                                                        {
                                                            'if': {'column_id': str(x), 'filter_query': '{{{0}}} >= 80'.format(x)},
                                                            'background_color': '#B3E577',
                                                        } for x in df.columns

                                                    ]
                                                    +
                                                    [
                                                        {
                                                            'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 60 && {{{0}}} <80'.format(x)},
                                                            'background_color': '#E0ED4B',
                                                        } for x in df.columns
                                                    ]
                                                    +
                                                    [
                                                        {
                                                            'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 60'.format(x)},
                                                            'background_color': '#F78B54',
                                                        } for x in df.columns
                                                    ]
                                                    +
                                                    [
                                                        {
                                                            'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 0'.format(x)},
                                                            'background_color': '#fafcfa',
                                                        } for x in df.columns
                                                    ]
                                                    +
                                                    
                                                    [
                                                        {
                                                            'if': {'column_id': 'Rates'},'fontWeight': 'bold',
                                                        } 
                                                    ]
                                                ),
                            ]),
                html.Div(dcc.Dropdown(id=reference+'name_list',
                                    options=[{'label': i, 'value': i} for i in main.Name],
                                    value='Select Sorter',
                                    placeholder='Select Sorter',
                                    searchable=False,
                                    multi=False),style={'width': '20%'}),
                dbc.Row([
                        dbc.Col(dcc.Graph(id=reference+'rates_graph',figure=fig),className="one columns"),
                        dbc.Col(dcc.Graph(id=reference+'level_graph',figure=fig2),className="one columns")
                        ]),
                html.Div(dcc.Interval(
                    id=reference+'interval-main_table',
                    interval=refreshing_time, # in milliseconds
                    n_intervals=0)),
                html.Div(dcc.Interval(
                    id=reference+'interval-results_table',
                    interval=refreshing_time, # in milliseconds
                    n_intervals=0)),
                html.Div(dcc.Interval(
                    id=reference+'interval_graph',
                    interval=refreshing_time, # in milliseconds
                    n_intervals=0)),
            ],style={'margin-left':'10%','margin-right':'10%'})
    )

@app.callback(Output(reference+'rates_graph', 'figure'),
        [Input(reference+'name_list', 'value'),Input(reference+'interval_graph', 'n_intervals'),Input(reference+'my-date-picker-single', 'date')])

def update_graph(value,interval_graph,date):
        input_day=str(date)[5:10]
        file_name='archive/Sorting/'+input_day+reference+'.xlsx'
        main=pd.read_excel(file_name,sheet_name='main')
        aux=pd.read_excel(file_name,sheet_name='aux')
        if value!='Select Sorter' and value!='Total' and value:
            fig=px.line(aux, x='hours', y=value, title=value+' Performance curve')
            fig.add_trace(go.Scatter(x=aux.hours, y=[float(main[main['Name']== value]['Rates']) for i in aux.index],
                        mode='lines',
                        name="Average {:,.2f} ilpns/hour".format(float(main[main['Name']==value]['Rates']))))
            return fig
        else :
            fig=px.line(aux, x='hours', y='Total', title='Total Performance curve')
            fig.add_trace(go.Scatter(x=aux.hours, y=[float(main[main['Name']=='Total']['Rates']) for i in aux.index],
                        mode='lines',
                        name="Average {:,.2f} ilpns/hour".format(float(main[main['Name']=='Total']['Rates']))))
           
            return fig


@app.callback(Output(reference+'main_table', 'data'),
              [Input(reference+'interval-main_table', 'n_intervals'),Input(reference+'my-date-picker-single', 'date')])
def update_main_table(n_intervals,date):
        input_day=str(date)[5:10]
        file_name='archive/Sorting/'+input_day+reference+'.xlsx'
        main=pd.read_excel(file_name,sheet_name='main').round(2)
        data=main.to_dict('records')
        return data

@app.callback(Output(reference+'results_table', 'data'),
              [Input(reference+'interval-results_table', 'n_intervals'),Input(reference+'my-date-picker-single', 'date')])
def update_results_table(n_intervals,data):
    input_day=str(data)[5:10]
    file_name='archive/Sorting/'+input_day+reference+'.xlsx'
    results_table=pd.read_excel(file_name,sheet_name='results_table').iloc[:,1:]
    data=results_table.to_dict('records')
    return data

@app.callback(Output(reference+'name_list', 'options'),
              [Input(reference+'interval-main_table', 'n_intervals'),Input(reference+'my-date-picker-single', 'date')])
def update_dropbox(n_intervals,date):
        input_day=str(date)[5:10]
        file_name='archive/Sorting/'+input_day+reference+'.xlsx'
        main=pd.read_excel(file_name,sheet_name='main').round(2)
        options=[{'label': i, 'value': i} for i in main.Name]
        return options

@app.callback(Output(reference+'level_graph', 'figure'),
        [Input(reference+'interval-main_table', 'n_intervals'),Input(reference+'my-date-picker-single', 'date')])
def update_graph(n_intervals,date):
    input_day=str(date)[5:10]
    file_name='archive/Sorting/'+input_day+reference+'.xlsx'
    floors_table=pd.read_excel(file_name,sheet_name='floors_table')
    fig2 = px.bar(floors_table, x='level', y=reference[8:],color=reference[8:],text=reference[8:],color_continuous_scale=['#060000','#EC9C08','#F71802'])
    return fig2


@app.callback(Output(reference+'time_update', 'children'),
              [Input(reference+'my-date-picker-single', 'date'),Input(reference+'interval-main_table', 'n_intervals')])
def update_time(date,n_intervals):
    input_day=str(date)
    return fx.update_time(12,20,input_day)