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
morning=[('4:00','5:00'),('5:00','6:00'),('6:00','7:00'),('7:00','8:00'),
                ('8:00','9:00'),('9:00','10:00'),('10:00','11:00'),('11:00','12:00')]
afternoon=[('12:00','13:00'),('13:00','14:00'),('14:00','15:00'),('15:00','16:00'),
                ('16:00','17:00'),('17:00','18:00'),('18:00','19:00'),('19:00','20:00')]
night=[('20:00','21:00'),('21:00','22:00'),('22:00','23:00'),('23:00','0:00'),
                ('0:00','1:00'),('1:00','2:00'),('2:00','3:00'),('3:00','4:00')]


#reference is used infront of every single id of each one of the elements of the layout, to avoid duplicate callbacks
reference='Afternoon shift'
#refreshing time establishes the amount of time by each callback
refreshing_time=1*60*1000 #millisecods


input_day=str(fx.date_reader())[5:10]
data=pd.read_excel('archive/Pulling/database.xlsx')
fx.get_rates(reference,afternoon,fx.date_reader(),data)
file_name=str(fx.date_reader())[5:10]+reference+'.xlsx'


main,aux=fx.get_main_aux(file_name)
df=fx.main_table(file_name)
results_table=fx.get_results_table(file_name,df)


#The following is to split the main table into 3 different sections 
top_100=['001/AMMS','08N/A08N', '08N/A08N', '08S/A08S', '09B/A09B','09S/A09S','09S/A09S',0]
top_50=['RL1/AMRV','RL2/AMRV','RL3/AMRV','RL4/AMRV','SHR/SHRE']
total=['---']
temp=[main[main['Last Location']==location] for location in top_100]
main_table_1=pd.concat(temp,axis=0).drop_duplicates().replace('nan',' ').sort_values('Rate',ascending=False)
temp=[main[main['Last Location']==location] for location in top_50]
main_table_2=pd.concat(temp,axis=0).drop_duplicates().replace('nan',' ').sort_values('Rate',ascending=False)
main_table_total=main[main['Last Location']=='---']

fig=px.line(aux, x='Hour', y='Total', title='Total Performance curve')
fig.add_trace(go.Scatter(x=aux.index, y=[float(main['Rate'].loc['Total']) for i in aux.index],
                        mode='lines',
                        name="Average {:,.2f} ilpns/hour".format(float(main['Rate'].loc['Total']))))
fig2=fx.pulling_load_distribution(reference)

layout =html.Div(
    [   
        html.H1('Pulling Ambient '+reference,style={'text-align':'center'}),
        html.H2(id=reference+'time_update',children='',style={'text-align':'center'}),
        html.Div(
            [

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
                dash_table.DataTable( id=reference+'main_table_1',
                                        columns=[{"name": i, "id": i} for i in main_table_1.columns],
                                        data=main_table_1.to_dict('records'),
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
                                            +
                                            [
                                                {
                                                    'if': {'column_id': 'Reference'},'width':'20%',
                                                } 
                                            ]
                                            +
                                                                                        [
                                                {
                                                    'if': {'column_id': 'Last Location'},'width':'10%',
                                                } 
                                            ]

                                    ),
                html.Br(),
                dash_table.DataTable( id=reference+'main_table_2',
                                        columns=[{"name": i, "id": i} for i in main_table_2.columns],
                                        data=main_table_2.to_dict('records'),
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
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} >= 50'.format(x)},
                                                    'background_color': '#B3E577',
                                                } for x in df.columns

                                            ]
                                            +
                                            [
                                                {
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 40 && {{{0}}} <50'.format(x)},
                                                    'background_color': '#E0ED4B',
                                                } for x in df.columns
                                            ]
                                            +
                                            [
                                                {
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 40'.format(x)},
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
                                            +
                                            [
                                                {
                                                    'if': {'column_id': 'Reference'},'width':'20%',
                                                } 
                                            ]
                                            +
                                                                                        [
                                                {
                                                    'if': {'column_id': 'Last Location'},'width':'10%',
                                                } 
                                            ]
                                        ),
                html.Br(),
                dash_table.DataTable( id=reference+'main_table_total',
                                        columns=[{"name": i, "id": i} for i in main_table_total.columns],
                                        data=main_table_total.to_dict('records'),
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
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} >= 500'.format(x)},
                                                    'background_color': '#B3E577',
                                                } for x in df.columns

                                            ]
                                            +
                                            [
                                                {
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 400 && {{{0}}} <500'.format(x)},
                                                    'background_color': '#E0ED4B',
                                                } for x in df.columns
                                            ]
                                            +
                                            [
                                                {
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 400'.format(x)},
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
                                            +
                                            [
                                                {
                                                    'if': {'column_id': 'Reference'},'width':'20%',
                                                } 
                                            ]
                                            +
                                                                                        [
                                                {
                                                    'if': {'column_id': 'Last Location'},'width':'10%',
                                                } 
                                            ]
                                        ),
                html.Br(),
            ]),
        
        html.Div([
            dcc.Dropdown(id=reference+'name_list',
                            options=[{'label': i, 'value': i} for i in df.index],
                            value=df.index[0],
                            placeholder='Select Operator',
                            searchable=False,
                            multi=False)],style={'width':'20%'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id=reference+'rates_graph',figure=fig)),
            dbc.Col(dcc.Graph(id=reference+'load_graph',figure=fig2)),
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
            n_intervals=0))

    ],style={'margin-left':'10%','margin-right':'10%'})

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
            
@app.callback(Output(reference+'main_table_1', 'data'),
              [Input(reference+'interval-main_table', 'n_intervals')])
   
def update_main_table_1(n_intervals):
        file_name=str(fx.date_reader())[5:10]+reference+'.xlsx'
        main=fx.get_main_aux(file_name)[0]
        temp=[main[main['Last Location']==location] for location in top_100]
        main_table_1=pd.concat(temp,axis=0).drop_duplicates().replace('nan',' ').sort_values('Rate',ascending=False)
        data=main_table_1.to_dict('records')
        return data

@app.callback(Output(reference+'main_table_2', 'data'),
              [Input(reference+'interval-main_table', 'n_intervals')])
   
def update_main_table_2(n_intervals):
        file_name=str(fx.date_reader())[5:10]+reference+'.xlsx'
        main=fx.get_main_aux(file_name)[0]
        temp=[main[main['Last Location']==location] for location in top_50]
        main_table_2=pd.concat(temp,axis=0).drop_duplicates().replace('nan',' ').sort_values('Rate',ascending=False)
        data=main_table_2.to_dict('records')
        return data

@app.callback(Output(reference+'main_table_total', 'data'),
              [Input(reference+'interval-main_table', 'n_intervals')])
   
def update_main_table_total(n_intervals):
        file_name=str(fx.date_reader())[5:10]+reference+'.xlsx'
        main=fx.get_main_aux(file_name)[0]
        main_table_total=main[main['Last Location']=='---']
        data=main_table_total.to_dict('records')
        return data


@app.callback(Output(reference+'time_update', 'children'),
              [Input(reference+'interval-main_table', 'n_intervals')])
def update_time(n_intervals):
        return fx.update_time(12,20)

@app.callback(Output(reference+'results_table', 'data'),
              [Input(reference+'interval-results_table', 'n_intervals')])
    
def update_results_table(n_intervals):
    file_name=str(fx.date_reader())[5:10]+reference+'.xlsx'
    df=fx.main_table(file_name)
    results_table=fx.get_results_table(file_name,df)
    data=results_table.to_dict('records')
    return data


@app.callback(Output(reference+'name_list', 'options'),
              [Input(reference+'interval-main_table', 'n_intervals')])
def update_dropbox(n_intervals):
        file_name=str(fx.date_reader())[5:10]+reference+'.xlsx'
        df=fx.main_table(file_name)
        options=[{'label': i, 'value': i} for i in df.index]
        return options

@app.callback(
        Output(reference+'load_graph', 'figure'),
        [Input(reference+'interval_graph', 'n_intervals')])
def update_load_graph(n_intervals):
    return fx.pulling_load_distribution(reference)