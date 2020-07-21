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
import plotly.express as px
from app import app
from apps import functions as fx


#shifts definition
morning=[('4:00','5:00'),('5:00','6:00'),('6:00','7:00'),('7:00','8:00'),
                ('8:00','9:00'),('9:00','10:00'),('10:00','11:00'),('11:00','12:00')]
afternoon=[('12:00','13:00'),('13:00','14:00'),('14:00','15:00'),('15:00','16:00'),
                ('16:00','17:00'),('17:00','18:00'),('18:00','19:00'),('19:00','20:00')]
night=[('20:00','21:00'),('21:00','22:00'),('22:00','23:00'),('23:00','0:00'),
                ('0:00','1:00'),('1:00','2:00'),('2:00','3:00'),('3:00','4:00')]


#reference is used infront of every single id of each one of the elements of the layout, to avoid duplicate callbacks
reference='Morning shift'
#refreshing time establishes the amount of time by each callback
refreshing_time=1*60*1000 #millisecods


input_day=str(fx.date_reader())[5:10]
data=pd.read_excel('archive/database.xlsx')
fx.get_rates(reference,morning,fx.date_reader(),data)
file_name=str(fx.date_reader())[5:10]+reference+'.xlsx'


main,aux=fx.get_main_aux(file_name)
df=fx.main_table(file_name)
results_table=fx.get_results_table(file_name,df)

fig=px.line(aux, x='Hour', y='Total', title='Total Performance curve')
fig.add_trace(go.Scatter(x=aux.index, y=[float(main['Rate'].loc['Total']) for i in aux.index],
                        mode='lines',
                        name="Average {:,.2f} ilpns/hour".format(float(main['Rate'].loc['Total']))))
 

layout =html.Div(
    [   html.H1('Pulling Ambient '+reference,style={'float': 'center'}),
        html.H2(id=reference+'time_update',children=''),
        html.Div([dash_table.DataTable( id=reference+'main_table',
                                        columns=[{"name": i, "id": i} for i in main.columns],
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
                                                    'if': {'column_id': 'Rate'},'fontWeight': 'bold',
                                                } 
                                            ]
                                        ),
                dash_table.DataTable(   id=reference+'results_table',
                                        columns=[{"name": i, "id": i} for i in results_table.columns],
                                        data=results_table.to_dict('records'),
                                        style_cell={'textAlign': 'center','whiteSpace': 'normal', 'textOverflow': 'ellipsis'}
                                        )
                    ],style={'width':'70%'}),
        html.Div(dcc.Dropdown(id=reference+'name_list',
                            options=[{'label': i, 'value': i} for i in df.index],
                            value='Pull_Rates',
                            placeholder='Select Operator',
                            searchable=False,
                            multi=False),style={'width': '28%', 'float': 'center', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id=reference+'rates_graph',figure=fig,style={'width': '65%'})),
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
                ])

@app.callback(
        Output(reference+'rates_graph', 'figure'),
        [Input(reference+'name_list', 'value'),Input(reference+'interval_graph', 'n_intervals')])

def update_graph(name_list,interval_graph):
        file_name=str(fx.date_reader())[5:10]+reference+'.xlsx'
        main,aux=fx.get_main_aux(file_name)
        df=fx.main_table(file_name)
        if name_list!='Pull_Rates' and name_list!='Total' and name_list:
            fig=px.line(aux, x='Hour', y=name_list, title=name_list+' Performance curve')
            fig.add_trace(go.Scatter(x=aux.index, y=[df['Rate'].loc[name_list] for i in aux.index],
                    mode='lines',
                    name="Average {:,.2f} ilpns/hour".format(df['Rate'].loc[name_list])))
            return fig
        else :
            fig=px.line(aux, x='Hour', y='Total', title='Total Performance curve')
            fig.add_trace(go.Scatter(x=aux.index, y=[float(main['Rate'].loc['Total']) for i in aux.index],
                        mode='lines',
                        name="Average {:,.2f} ilpns/hour".format(float(main['Rate'].loc['Total']))))
            return fig
            
   
@app.callback(Output(reference+'main_table', 'data'),
              [Input(reference+'interval-main_table', 'n_intervals')])
    
def update_main_table(n_intervals):
        file_name=str(fx.date_reader())[5:10]+reference+'.xlsx'
        main=fx.get_main_aux(file_name)[0]
        data=main.to_dict('records')
        return data

@app.callback(Output(reference+'time_update', 'children'),
              [Input(reference+'interval-main_table', 'n_intervals')])
def update_time(n_intervals):
        return fx.update_time(4,12)

@app.callback(Output(reference+'results_table', 'data'),
              [Input(reference+'interval-results_table', 'n_intervals')])
    
def update_results_table(n_intervals):
    file_name=str(fx.date_reader())[5:10]+reference+'.xlsx'
    df=fx.main_table(file_name)
    results_table=fx.get_results_table(file_name,df)
    data=results_table.to_dict('records')
    return data




