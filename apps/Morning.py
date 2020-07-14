from datetime import date
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

reference='Morning shift'

def main_table(shift=reference+'.xlsx'):
        df=pd.read_excel(shift)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df=df.set_index('Name')
        df.loc['Total',:]=df.sum(axis=0)
        return df
def general_indicators():
        df=main_table()
        df2=df.iloc[:-1,:-1]
        temp=df2[df2>20]
        results=pd.DataFrame(index=np.arange(len(temp.count())))
        results['Hour']=temp.count().index
        results['Headcount']=temp.count().values
        results['Exp_Rate/person']=np.where((results['Hour']=='8:00-9:00') | (results['Hour']=='9:00-10:00'),75,100)
        results['Exp_Rate']=results['Exp_Rate/person']*results['Headcount']
        expected,real=results['Exp_Rate'].sum(axis=0),df2.sum(axis=0).sum()
        return (expected,real)
    
    #results table
m_results_table=pd.DataFrame(columns=['Expected Results','Net Results','Difference'],index=np.arange(1))
m_results_table['Expected Results']=general_indicators()[0]
m_results_table['Net Results']=general_indicators()[1]
m_results_table['Difference']=general_indicators()[1]-general_indicators()[0]
#this is only to show the table and the average part of the graph
m_main=main_table()
m_main.insert(loc=0,column='Reference', value=m_main.index)
m_main['Rate']['Total']=m_main.loc['Total'][1:-1][m_main.loc['Total'][1:-1]>0].mean()
m_main['Rate'] = m_main['Rate'].map('{:,.2f}'.format)
df=main_table()
df2=df.T.iloc[:-1,:]
df2=df2[df2['Total']>0]
df2['Hour']=df2.index
fig=px.line(df2, x='Hour', y='Total', title='Total Performance curve')
fig.add_trace(go.Scatter(x=df2.index, y=[float(m_main['Rate'].loc['Total']) for i in df2.index],
                    mode='lines',
                    name="Average {:,.2f} ilpns/hour".format(float(m_main['Rate'].loc['Total']))))

def time_():
    import datetime
    hour=int(time.ctime()[11:13])
    if hour>=4 and hour<=12:
        now = datetime.datetime.now()    
        return 'Last update '+now.strftime("%H:%M %m-%d")
    else:
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        return f'Last update 12:00 {str(yesterday)[5:]}'
       
layout =html.Div(
    [
        html.H1('Pulling Ambient '+reference,style={'float': 'center'}),
        html.H2(id=reference+'time_update',children=''),
        html.Div([dash_table.DataTable(
                                        id=reference+'main_table',
                                        columns=[{"name": i, "id": i} for i in m_main.columns],
                                        data=m_main.to_dict('records'),
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
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} >= 75'.format(x)},
                                                    'background_color': '#B3E577',
                                                } for x in df.columns

                                            ]
                                            +
                                            [
                                                {
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} > 35 && {{{0}}} <75'.format(x)},
                                                    'background_color': '#E0ED4B',
                                                } for x in df.columns
                                            ]
                                            +
                                            [
                                                {
                                                    'if': {'column_id': str(x), 'filter_query': '{{{0}}} <= 35'.format(x)},
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
                dash_table.DataTable(   id='results_table',
                                        columns=[{"name": i, "id": i} for i in m_results_table.columns],
                                        data=m_results_table.to_dict('records'),
                                        style_cell={'textAlign': 'center','whiteSpace': 'normal', 'textOverflow': 'ellipsis'}
                                        )
                    ],style={'width':'70%'}),
        html.Div(dcc.Dropdown(
                    id=reference+'name_list',
                    options=[{'label': i, 'value': i} for i in df.index],
                    value='Pull_Rates',
                    placeholder='Select Operator',
                    searchable=False,
                    multi=False
                ),style={'width': '28%', 'float': 'center', 'display': 'inline-block'}),
        html.Div(dcc.Graph(id=reference+'rates_graph',figure=fig,style={'width': '65%'})),
        html.Div(dcc.Interval(
            id=reference+'interval-main_table',
            interval=1000, # in milliseconds
            n_intervals=0)),
        html.Div(dcc.Interval(
            id=reference+'interval-results_table',
            interval=1000, # in milliseconds
            n_intervals=0)),
        html.Div(dcc.Interval(
            id=reference+'interval_graph',
            interval=1000, # in milliseconds
            n_intervals=0)),
    ])

@app.callback(
        Output(reference+'rates_graph', 'figure'),
        [Input(reference+'name_list', 'value'),Input(reference+'interval_graph', 'n_intervals')])

def update_graph(name_list,interval_graph):
        if name_list!='Pull_Rates' and name_list!='Total' and name_list:
            df=main_table()
            dff=df.T.iloc[:-1,:]
            dff=dff[dff['Total']>0]
            dff['Hour']=dff.index
            fig=px.line(dff, x='Hour', y=name_list, title=name_list+' Performance curve')
            fig.add_trace(go.Scatter(x=dff.index, y=[df['Rate'].loc[name_list] for i in dff.index],
                    mode='lines',
                    name="Average {:,.2f} ilpns/hour".format(df['Rate'].loc[name_list])))
            return fig
        else :
            df=main_table()
            dff=df.T.iloc[:-1,:]
            dff=dff[dff['Total']>0]
            dff['Hour']=dff.index
            fig=px.line(dff, x='Hour', y='Total', title='Total Performance curve')
            main=main_table()
            main.insert(loc=0,column='Reference', value=main.index)
            main['Rate']['Total']=main.loc['Total'][1:-1][main.loc['Total'][1:-1]>0].mean()
            main['Rate'] = main['Rate'].map('{:,.2f}'.format)
            fig.add_trace(go.Scatter(x=dff.index, y=[float(main['Rate'].loc['Total']) for i in dff.index],
                    mode='lines',
                    name="Average {:,.2f} ilpns/hour".format(float(main['Rate'].loc['Total']))))
            return fig
   
@app.callback(Output(reference+'main_table', 'data'),
              [Input(reference+'interval-main_table', reference+'n_intervals')])
    
def update_main_table(n_intervals):
        # hour=int(time.ctime()[11:13])
        # if hour>=4 and hour<=13:
        data=pd.read_excel('database.xlsx')
        date_=fx.date_reader()
        if date_:
            fx.get_rates(reference,morning,date_,data)
        else:
            fx.get_rates(reference,morning,date.today(),data)
        dff=main_table()
        dff.insert(loc=0,column='Reference', value=dff.index)
        dff['Rate']['Total']=dff.loc['Total'][1:-1][dff.loc['Total'][1:-1]>0].mean()
        dff['Rate'] = dff['Rate'].map('{:,.2f}'.format)
        dff.fillna(0)
        data=dff.to_dict('records')
        return data

@app.callback(Output(reference+'time_update', 'children'),
              [Input(reference+'interval-main_table', 'n_intervals')])
def update_time(n_intervals):
        return time_()

@app.callback(Output(reference+'results_table', 'data'),
              [Input(reference+'interval-results_table', reference+'n_intervals')])
    
def update_results_table(n_intervals):
        m_results_table['Expected_Results']=general_indicators()[0]
        m_results_table['Net Results']=general_indicators()[1]
        m_results_table['Difference']=general_indicators()[1]-general_indicators()[0]
        data=m_results_table.to_dict('records')
        return data



