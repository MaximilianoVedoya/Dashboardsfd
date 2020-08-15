#reads all the information form the database and stores the detail file into database.xslx
def get_data():
    import pandas as pd
    import numpy as np
    from datetime import date
    import pyodbc

    connection = pyodbc.connect('DRIVER={SQL Server};'

                                'SERVER=nj01prdbidb01.intranet.biz.freshdirect.com;'

                                'DATABASE=DASHBOARD;'

                                'UID=DASH_READONLY;'

                                'PWD=Mbers0nyon#123;'
                                
                                "autocommit = True")
    query="""
        Select 
        distinct
        pt.USER_ID as User_id,
        concat(us.USER_FIRST_NAME,',',us.USER_LAST_NAME) usr,
        pt.task_id,
        pt.CNTR_NBR ilpn,
        case when isNull(td.STAT_CODE,td2.STAT_CODE) = 40 then 'Pulled' 
        when isNull(td.STAT_CODE,td2.STAT_CODE) = 99 then 'Pulled then Ctrl-G'
        else 'Complete' end as status,
        concat(lh0.WORK_AREA,'/',lh0.WORK_GRP) 'WA/WG',
        pt.CREATE_DATE_TIME pulling_date_time,
        lh0.dsp_locn Pull_location,
        convert(date,pt.CREATE_DATE_TIME) pulling_date,

        case when th.INVN_NEED_TYPE = 1 then 'INT1' 
        when th.INVN_NEED_TYPE = 2 then 'INT2' 
        when th.INVN_NEED_TYPE = 90 then 'INT90' 
        end as INT_task,

        CASE
            WHEN Th.Task_Type = '11' THEN 'Chill Pallet'
            WHEN Th.Task_Type = '12' THEN 'Freezer Pallet Replen'
            WHEN Th.Task_Type = '13' THEN 'BTO Pallet Replen'
            WHEN Th.Task_Type = '14' THEN 'Kitchen Pallet Replen'
            WHEN Th.Task_Type = '15' THEN 'Ambient Pallet Replen'
            WHEN Th.Task_Type = '70' and  Th.START_CURR_WORK_AREA NOT like 'N%' 
                                THEN 'Ambient Case Replen'
            WHEN Th.Task_Type = '71' and Th.START_CURR_WORK_AREA NOT like 'B%' and Th.START_CURR_WORK_AREA NOT like 'N%'
                                    THEN 'Chill Case Replen' 
            WHEN Th.Task_Type = '72' THEN 'Freezer Case Replen'
            WHEN Th.Task_Type = '73' THEN 'BTO Case Replen'
            WHEN Th.Task_Type = '74' THEN 'Kitchen Case Replen'
            WHEN Th.Task_Type = '75' THEN 'Shuttle Case Replen'
            WHEN Th.Task_Type = '70' and  Th.START_CURR_WORK_AREA like 'N%' 
                                        THEN 'Supplies'
            WHEN Th.Task_Type = '71' and (Th.START_CURR_WORK_AREA like 'B%' or Th.START_CURR_WORK_AREA like 'P%')
                                    THEN 'Supplies'
            WHEN Th.Task_Type = '76' THEN 'Chill MTS Replen'
            WHEN Th.Task_Type in ('40','41') THEN 'Pick from reserve INT2'
            WHEN Th.Task_Type = '50' THEN 'Recall INT90'
        END AS "Task description",

        --concat(td.task_id,td.CNTR_NBR) id,

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end as Pull_hour,


        case 	when

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('04AM','05AM','06AM','07AM','08AM','09AM','10AM','11AM') then 'Morning shift'

            when
        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('12PM','01PM','02PM','03PM','04PM','05PM','06PM','07PM') then 'Afternoon shift'

            When 

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('08PM','09PM','10PM','11PM','12AM','01AM','02AM','03AM') then 'Night shift'

            end as Shft,

        case 	when

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('04AM','05AM','06AM','07AM','08AM','09AM','10AM','11AM') then convert(date,pt.CREATE_DATE_TIME)

            when
        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('12PM','01PM','02PM','03PM','04PM','05PM','06PM','07PM') then convert(date,pt.CREATE_DATE_TIME+1)

            When 

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('08PM','09PM','10PM','11PM') then convert(date,pt.CREATE_DATE_TIME+1)

            When 

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('12AM','01AM','02AM','03AM') then convert(date,pt.CREATE_DATE_TIME)

            end as Delivery
                        
        from PROD_TRKG_TRAN_WMS pt

        left outer join (select distinct th.task_id,th.Task_type,th.INVN_NEED_TYPE,Th.START_CURR_WORK_AREA from TASK_HDR_WMS th where th.INVN_NEED_TYPE in (1,2,90)
        and th.CREATE_DATE_TIME > cast(getdate()-6 as date)
        )th
        on th.TASK_ID = pt.TASK_ID

        left outer join (select distinct pt.CNTR_NBR,pt.task_id,concat(pt.from_locn,pt.CNTR_NBR)id,pt.CREATE_DATE_TIME from PROD_TRKG_TRAN_WMS pt
        inner join (
        select  distinct min(pt.CREATE_DATE_TIME)CREATE_DATE_TIME,concat(pt.from_locn,pt.CNTR_NBR)id from PROD_TRKG_TRAN_WMS pt where
        convert (date,pt.CREATE_DATE_TIME) > cast(getdate()-5 as date) 
        and pt.TRAN_TYPE = 300 and pt.TRAN_CODE = '005' and pt.TASK_ID is not null
        group by concat(pt.from_locn,pt.CNTR_NBR)
        )ptn on ptn.id = concat(pt.FROM_LOCN,pt.cntr_nbr) and ptn.CREATE_DATE_TIME = pt.CREATE_DATE_TIME
        where convert (date,pt.CREATE_DATE_TIME) > cast(getdate()-5 as date) and pt.TRAN_TYPE = 300 and pt.TASK_ID is not null 
        and pt.TRAN_CODE = '005'
        )ptn
        on ptn.id = concat(pt.FROM_LOCN,pt.cntr_nbr)
        and ptn.CREATE_DATE_TIME > pt.CREATE_DATE_TIME

        left outer join (select CONCAT(td.task_id,td.CNTR_NBR)id, td.TASK_ID, td.STAT_CODE from TASK_DTL_WMS td where td.MOD_DATE_TIME > cast(getdate()-6 as date))td
        on td.id = concat(ptn.TASK_ID,ptn.cntr_nbr)

        left outer join (select CONCAT(td.task_id,td.CNTR_NBR)id, td.TASK_ID, td.STAT_CODE from TASK_DTL_WMS td where td.MOD_DATE_TIME > cast(getdate()-6 as date))td2
        on td2.id = concat(pt.TASK_ID,pt.cntr_nbr)

        left outer join LOCN_HDR_WMS lh0
        on lh0.LOCN_ID = pt.FROM_LOCN

        left outer join ITEM_MASTER_WMS im
        on im.ITEM_ID = pt.ITEM_ID


        left outer join ucl_user_wms us
        on us.USER_NAME = pt.USER_ID

        where 
        convert (date,pt.CREATE_DATE_TIME) > cast(getdate()-6 as date)
        and pt.TRAN_TYPE = 300 and pt.TRAN_CODE = '006' and pt.TASK_ID is not null
        and th.Task_type not in (00,01,02,03,04,05,06,07,08)
        and (lh0.ZONE in ('A1','A2','A3','A4','A5','A6','A7'))
    """
    # Setting up a cursor.
    cursor = connection.cursor()
    # fetch data function.
    data = cursor.execute(query).fetchall()
    connection.close()                           

    reference=['User_id','usr','task_id','ilpn','status','WA/WG','pulling_date_time','Pull_location','pulling_date','INT_task','Task description','Pull_hour','Shft','Delivery']
    df=pd.DataFrame(columns=reference,index=np.arange(len(data)))
    for item in range(len(reference)):
        for row in range(len(data)):
            df[reference[item]][row]=data[row][item]

    out_path='archive\Pulling\database.xlsx'
    writer = pd.ExcelWriter(out_path , engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    return df

#recibes the name of the shift, definitiion of shifts, 
# date(YYYY-MM-DD) as string and raw data(from the function get_data()
def get_rates(shift,period,date_,data):
    from datetime import date
    import datetime
    import pandas as pd
    import numpy as np
    def get_users(shift,date_):
        temp=data[data['Shft']==shift]
        temp=temp.sort_values(by='pulling_date_time')
        temp=temp.set_index('pulling_date_time')
        g=temp.groupby(temp.index.floor('d'))
        my_day = pd.Timestamp(date_)
        df_slice = g.get_group(my_day)   
        return list(df_slice.usr.unique())

    def get_list(start,finish,shift,date_):
        morning=data[data['Shft']==shift]
        morning=morning.sort_values(by='pulling_date_time')
        morning=morning.set_index('pulling_date_time')
        g=morning.groupby(morning.index.floor('d'))
        my_day = pd.Timestamp(date_)
        df_slice = g.get_group(my_day)      
        first_hour=df_slice.between_time(start,finish)
        operators=first_hour['usr'].unique()
        dic={employee: first_hour[first_hour['usr']==employee]['ilpn'].size for employee in operators}
        return dic

    def built_dataframe(shift,period,date_):
        list_=[s+'-'+e for s,e in period]
        list_.insert(0,'Name')
        users=get_users(shift,date_)
        df=pd.DataFrame(columns=list_, index=pd.Series(users))
        starting=[s for s,e in period]
        ending=[e for s,e in period]
        def dataframe(s,e,shift):
            for name,rate in get_list(s,e,shift,date_).items():
                df[s+'-'+e][name]=rate
        for s,e in period:
            dataframe(s,e,shift)
        return df 
    
    def new_dataframe(shift,date_,data):
        today=str(date_)[:10]
        today_data=data[(data['pulling_date']==today)
                        &(data['Shft']==shift)
                        &(data['status']!='Pulled then Ctrl-G')]
        top50_data=today_data[ (today_data['WA/WG']=='RL1/AMRV')|
                       (today_data['WA/WG']=='RL2/AMRV')|
                       (today_data['WA/WG']=='RL3/AMRV')|
                       (today_data['WA/WG']=='RL4/AMRV')|
                       (today_data['WA/WG']=='SHR/SHRE')]

        top100_data=today_data[(today_data['WA/WG']=='001/AMMS')|
                            (today_data['WA/WG']=='07S/A07S')|
                            (today_data['WA/WG']=='07N/A07N')|
                            (today_data['WA/WG']=='08N/A08N')|
                            (today_data['WA/WG']=='08S/A08S')|
                            (today_data['WA/WG']=='09B/A09B')|
                            (today_data['WA/WG']=='09S/A09S')|
                            (today_data['WA/WG']=='09N/A09N')|
                            (today_data['WA/WG']=='EL1/AFLO')]
        
        location_50=top50_data.groupby(['Pull_hour','usr','WA/WG']).count()['ilpn'].unstack(level=0).fillna(0)
        location_100=top100_data.groupby(['Pull_hour','usr','WA/WG']).count()['ilpn'].unstack(level=0).fillna(0)
        def table_builder(raw_table):
            raw_table.set_index=range(len(raw_table.index))
            raw_table.reset_index(inplace=True)  
            raw_table.index.rename='index'
            def get_user_working_hours(user,location,database=today_data):
                user_data=database[(database['usr']==user)&(database['WA/WG']==location)].sort_values('pulling_date_time')
                time=list()
                for hour in user_data['Pull_hour'].unique():
                        temp=user_data[user_data['Pull_hour']==hour]
                        first_pull=temp.iloc[0]['pulling_date_time']
                        last_pull=temp.iloc[-1]['pulling_date_time']
                        delta_time=(last_pull-first_pull).seconds/3600
                        time.append(delta_time)
                return sum(time)
            raw_table['Working Hours']=raw_table.apply(lambda x: get_user_working_hours(x['usr'],x['WA/WG']),axis=1)
            raw_table['Total']=raw_table.T[2:-1].sum(axis=0)
            raw_table['Rate']=np.where(raw_table['Working Hours']>0.5,raw_table['Total']/raw_table['Working Hours'],0)
            return raw_table.sort_values('Rate', ascending=False)
        ranking_100=table_builder(location_100)
        ranking_50=table_builder(location_50)
        return(ranking_100,ranking_50)

    try:  
        df=built_dataframe(shift,period,date_)
        df['Name']=df.index
        df=df.fillna(0)
        df2=df.T.drop(['Name'])
        df['Rate']=df2[df2>20].mean(axis=0)
        df=df.sort_values('Rate',ascending=False)
        df['Rate'] = df['Rate'].map('{:,.2f}'.format)
        #adds the last location detected. 
        data=data.sort_values('pulling_date_time', ascending=False)
        Last_location=list()
        for user in df.index:
                Last_location.append(data[(data['usr']==user)]['WA/WG'].iloc[0])
        df.insert(1,'Last Location',Last_location)  
            
        ranking_100,ranking_50=new_dataframe(shift,date_,data)
                    
        file_name='archive/Pulling/'+str(date_)[5:10]+shift+'.xlsx'
        with pd.ExcelWriter(file_name) as writer:
                df.to_excel(writer, sheet_name='Sheet1')
                ranking_100.to_excel(writer, sheet_name='ranking_100')
                ranking_50.to_excel(writer, sheet_name='ranking_50')
        writer.save()
    except:
        pass
#small function to reads the date from the users (i might not need this, maybe I can read it from the input itself)

def pulling_get_tables(shift,date_):
    from datetime import date
    import datetime
    import pandas as pd
    import numpy as np
    data=pd.read_excel('archive/Pulling/database.xlsx')
    def dataframes(shift,date_,data):
        today=str(date_)[:10]
        today_data=data[(data['pulling_date']==today)
                        &(data['Shft']==shift)
                        &(data['status']!='Pulled then Ctrl-G')]
        top50_data=today_data[ 
                       (today_data['WA/WG']=='RL1/AMRV')|
                       (today_data['WA/WG']=='RL2/AMRV')|
                       (today_data['WA/WG']=='RL3/AMRV')|
                       (today_data['WA/WG']=='RL4/AMRV')|
                       (today_data['WA/WG']=='SHR/SHRE')]
        top100_data=today_data[ 
                       (today_data['WA/WG']!='RL1/AMRV')&
                       (today_data['WA/WG']!='RL2/AMRV')&
                       (today_data['WA/WG']!='RL3/AMRV')&
                       (today_data['WA/WG']!='RL4/AMRV')&
                       (today_data['WA/WG']!='SHR/SHRE')]
        
        location_50=top50_data.groupby(['Pull_hour','usr','WA/WG']).count()['ilpn'].unstack(level=0).fillna(0)
        location_100=top100_data.groupby(['Pull_hour','usr','WA/WG']).count()['ilpn'].unstack(level=0).fillna(0)
        
        def table_builder(raw_table,database):
            raw_table.set_index=range(len(raw_table.index))
            raw_table.reset_index(inplace=True)  
            raw_table.index.rename='index'
            def get_user_working_hours(user,location,database=database):
                maximum_time_between_pulls=0.1
                user_data=database[(database['usr']==user)&(database['WA/WG']==location)].sort_values('pulling_date_time')
                time=list()
                for hour in user_data['Pull_hour'].unique():
                        user_data_byhour=user_data[user_data['Pull_hour']==hour]
                        for pull in range(len(user_data_byhour.index)-1):
                            first=user_data_byhour.iloc[pull]['pulling_date_time']
                            second=user_data_byhour.iloc[pull+1]['pulling_date_time']
                            delta_time=(second-first).seconds/3600
                            if delta_time<=maximum_time_between_pulls:
                                time.append(delta_time)
                            else:
                                time.append(maximum_time_between_pulls)
                return sum(time)
            raw_table['Working Hours']=raw_table.apply(lambda x: get_user_working_hours(x['usr'],x['WA/WG']),axis=1)
            raw_table['Total']=raw_table.T[2:-1].sum(axis=0)
            
            raw_table.reset_index(drop=True, inplace=True)
            def get_last_position(user,database=database):
                position=database[(database['usr']==user)].sort_values('pulling_date_time').iloc[-1]['WA/WG']
                return position
            raw_table['Last Position']=raw_table.apply(lambda x:get_last_position(x['usr']),axis=1)
            return raw_table
    
        #table is either top50_data or top100_data
        def get_time_table(table,database=data):
            maximum_time_between_pulls=0.1
            temp=table.groupby(['Pull_hour','usr','WA/WG']).count()['ilpn'].unstack(level=0).fillna(0).index
            dic={user+' '+location: 0 for user,location in temp}
            for user,location in temp:
                user_data=database[(database['usr']==user)&(database['WA/WG']==location)].sort_values('pulling_date_time')
                time=list()
                times=list()
                for hour in user_data['Pull_hour'].unique():
                        user_data_byhour=user_data[user_data['Pull_hour']==hour]
                        for pull in range(len(user_data_byhour.index)-1):
                            first=user_data_byhour.iloc[pull]['pulling_date_time']
                            second=user_data_byhour.iloc[pull+1]['pulling_date_time']
                            delta_time=(second-first).seconds/3600
                            if delta_time<=maximum_time_between_pulls:
                                time.append(delta_time)
                            else:
                                time.append(maximum_time_between_pulls)
                        times.append(sum(time))
                dic[user+' '+location]=times
            max_=max([len(v) for v in dic.values()])
            for name in dic.keys():
                current_lenght=len (dic[name])
                temp=list(dic[name])
                if current_lenght<max_:
                    temp.extend([0 for i in range(max_-current_lenght)]) 
                    dic[name]=temp
            time_table=pd.DataFrame(dic)
            time_table=time_table.T
            temp=time_table.index
            location=[name.split(' ')[-1] for name in temp]
            names=[name[:-9] for name in temp]
            time_table.insert(0,'usr',names)
            time_table.insert(1,'WA/WG',location)
            time_table.index=time_table['usr']
            time_table.reset_index(drop=True, inplace=True)
            return ( time_table)
     
        #this section completes the table with all the hours (including those where nowbody worked)
        #it also solves the problem when in a particular shift nobody work in either 100 or 50 sectors, autocompleting the respective empty table in each case 
        def autocomplete(main):
            if shift=='Morning shift':
                hours=['usr','Last Position','04AM', '05AM', '06AM', '07AM', '08AM', '09AM','10AM', '11AM'
                    ,'Working Hours','Total','Rate']
            elif shift=='Afternoon shift':
                hours=['usr','Last Position','12PM', '01PM', '02PM', '03PM', '04PM', '05PM','06PM', '07PM'
                    ,'Working Hours','Total','Rate']
            elif shift=='Night shift':
                hours=['usr','Last Position','08PM', '09PM', '10PM', '11PM', '12AM', '01AM','02AM', '03AM'
                    ,'Working Hours','Total','Rate']
            if len(main):
                for position in range(len(hours)):
                    if hours[position] in main.columns:
                        continue
                    else:
                        list_=[0 for item in main.index]
                        main.insert(position,hours[position],list_)
                return main
            else:
                hours.append('WA/WG')
                fake=pd.DataFrame(columns=hours, index=range(3))
                fake=fake.fillna(0)
                fake['usr']=['fulano','mengano','sultano']
                return fake
             
        if len(top100_data):
            ranking_100=table_builder(location_100,top100_data)
            ranking_100=autocomplete(ranking_100)
            ranking_100_t=get_time_table(top100_data)
        else:
            ranking_100=autocomplete(top100_data)
            ranking_100_t=autocomplete(top100_data)
            
        if len(top50_data):
            ranking_50=table_builder(location_50,top50_data)
            ranking_50=autocomplete(ranking_50)
            ranking_50_t=get_time_table(top50_data)
        else:
            ranking_50=autocomplete(top50_data)
            ranking_50_t=autocomplete(top50_data)

        return (ranking_100,ranking_100_t,ranking_50,ranking_50_t)
    try:
        ranking_100=dataframes(shift,date_,data)[0]
        times_100=dataframes(shift,date_,data)[1]
        ranking_50=dataframes(shift,date_,data)[2]
        times_50=dataframes(shift,date_,data)[3]
                        
        file_name='archive/Pulling/'+str(date_)[5:10]+shift+'.xlsx'
        with pd.ExcelWriter(file_name) as writer:
                ranking_100.to_excel(writer, sheet_name='ranking_100')
                times_100.to_excel(writer, sheet_name='times_100')
                ranking_50.to_excel(writer, sheet_name='ranking_50')
                times_50.to_excel(writer, sheet_name='times_50')
        writer.save()
    except:
        pass
    
def pulling_get_mains(file_name,sheet_n):
    import pandas as pd 
    import numpy as np
    factor=1 #factor used to fix the computation of working hours.
    data=pd.read_excel('archive/Pulling/'+file_name,sheet_name=sheet_n).T[1:].T
    main=data.groupby(['usr','Last Position']).sum()
    main.drop('WA/WG', 1,inplace=True)
    main.reset_index(drop=False, inplace=True)
    main['Rate']=np.where(main['Working Hours']>0,main['Total']/(main['Working Hours']*factor),0)
    main['Rate']=main['Rate'].astype(float)
    main['Ranking']= 0.4*main['Rate']/max(main['Rate'])+0.6*main['Total']/max(main['Total'])
    main.sort_values('Ranking', ascending=False, inplace=True)
    main['Rate']=main['Rate'].map('{:,.2f}'.format)
    main['Working Hours']=main['Working Hours'].map('{:,.2f}'.format)
    main['Ranking']=main['Ranking'].map('{:,.2f}'.format)
    return main.T[:-1].T

def pulling_get_total(file_name):
    import pandas as pd
    from apps import functions as fx
    import numpy as np
    ranking_50=fx.pulling_get_mains(file_name,'ranking_50')
    ranking_100=fx.pulling_get_mains(file_name,'ranking_100')
    ranking_50['Rate']=ranking_50['Rate'].astype(float)
    ranking_100['Rate']=ranking_100['Rate'].astype(float)
    ranking_50['Working Hours']=ranking_50['Working Hours'].astype(float)
    ranking_100['Working Hours']=ranking_100['Working Hours'].astype(float)
    total=pd.concat([ranking_100.T,ranking_50.T],axis=1).sum(axis=1)
    total.usr='TOTAL'
    total['Last Position']=0
    if total['Working Hours']:
        aux=total.T[2:-3]
        aux=list(aux[aux>100])
        if len(aux):
            total['Rate']=sum(aux)/len(aux)
        else:
            total['Rate']=0
    else:
        total['Rate']=0
    total['Last Position']='---/----'
    df=pd.DataFrame(columns=[0], index=total.index)
    df[0]=total
    df=df.T
    df['Working Hours']=round(df['Working Hours'][0],2)
    df['Rate']=round(df['Rate'][0],2)
    return df

def pulling_get_result_table(file_name):
    import pandas as pd
    factor=1#this factor is to adjust the computation of working hours. 
    directory='archive/Pulling/'
    times_50=pd.read_excel(directory+file_name,'ranking_50')['Working Hours']
    times_100=pd.read_excel(directory+file_name,'ranking_100')['Working Hours']
    expected_result=int(times_50.sum()*50+times_100.sum()*100)*factor
    net_result=pd.read_excel(directory+file_name,'ranking_50')['Total'].sum()+pd.read_excel(directory+file_name,'ranking_100')['Total'].sum()
    result_table=pd.DataFrame(columns=['Expected Results','Net Results', 'Difference'], index=range(1))
    result_table['Expected Results']=expected_result
    result_table['Net Results']=net_result
    result_table['Difference']=net_result-expected_result
    return result_table.round(0)

def pulling_get_performance_fig(file_name,name='Total'):
    import pandas as pd 
    import plotly.graph_objs as go
    import plotly.express as px
    from apps import functions as fx
    ranking_100=fx.pulling_get_mains(file_name,'ranking_100')
    ranking_50=fx.pulling_get_mains(file_name,'ranking_50')
    total=pd.concat([ranking_100.T,ranking_50.T],axis=1)
    total=total.T.drop(['Last Position','Working Hours'],axis=1)
    total['Rate']=total['Rate'].astype('float')
    new_row=total.sum(axis=0)
    new_row['usr']='Total'
    total=total.append(new_row,ignore_index=True)
    
    aux=pd.DataFrame(columns=['Hour','Rate'],index=range(len(total.columns[1:-2])))
    aux['Hour']=total.columns[1:-2]
    aux['Total']=list(total.sum(axis=0)[1:-2])
    aux=total[total['usr']==name]
    aux.reset_index(drop=True,inplace=True)
    aux=aux.T[1:]
    effective_rate=aux.loc['Rate'][0]
    aux=aux[:-2]
    aux['Hour']=aux.index
    aux['Total']=aux[0]
    average_rate=aux[aux['Total']>20]['Total'].mean()

    fig=px.line(aux, x='Hour', y='Total', title=name+' Performance curve')

    fig.add_trace(go.Scatter(x=aux['Hour'], y=[average_rate for i in range(len(aux.index))],
                            mode='lines',
                            name="Effective rate {:,.2f} ilpns/hour".format(float(average_rate))))
    if name!='Total':
        fig.add_trace(go.Scatter(x=aux['Hour'], y=[effective_rate for i in range(len(aux.index))],
                            mode='lines',
                            name="Theorical rate {:,.2f} ilpns/hour".format(float(effective_rate))))
    return fig,total

def pulling_get_load_distribution_fig(file_name):
    import plotly.express as px
    import pandas as pd
    directory='archive/Pulling/'
    ranking_100=pd.read_excel(directory+file_name,'ranking_100')
    ranking_50=pd.read_excel(directory+file_name,'ranking_50')
    ranking_100=ranking_100[['WA/WG','Total']].groupby('WA/WG').sum()
    ranking_50=ranking_50[['WA/WG','Total']].groupby('WA/WG').sum()
    total=pd.concat([ranking_100.T,ranking_50.T],axis=1).T
    total['Location']=total.index
    fig=px.bar(total, x='Location', y='Total',
               color='Total',text='Total',title='Load distribution',
               color_continuous_scale=['#060000','#EC9C08','#F71802'])
    return fig

def pulling_initializer(finish,start,decrement=-1):
    import pandas as pd
    import datetime
    from apps import functions as fx
    shifts=['Morning shift','Afternoon shift','Night shift']
    for i in range(finish,start,decrement):
        for shift in shifts:
            date=datetime.datetime.today()-datetime.timedelta(i)
            fx.pulling_get_tables(shift,date)

    for i in range(finish,start,decrement):
            for shift in shifts: 
                try:
                    date_=datetime.datetime.today()-datetime.timedelta(days=i)
                    string=str(date_)[5:10]+shift+'.xlsx'
                    pd.read_excel('archive/Pulling/'+string)
                except:
                    yesterday=date_-datetime.timedelta(days=1)
                    file_name=str(yesterday)[5:10]+shift+'.xlsx'
                    fake_ranking_100=pd.read_excel('archive/Pulling/'+file_name,sheet_name='ranking_100')
                    fake_times_100=pd.read_excel('archive/Pulling/'+file_name,sheet_name='times_100')
                    fake_ranking_50=pd.read_excel('archive/Pulling/'+file_name,sheet_name='ranking_50')
                    fake_times_50=pd.read_excel('archive/Pulling/'+file_name,sheet_name='times_50')
                    def create_empty_df(df):
                        # df=df.drop('Unnamed: 0',axis=1)
                        aux=pd.DataFrame(columns=df.columns,index=df.index)
                        aux['usr']=df['usr']
                        return aux.fillna(0)
                    file_name='archive/Pulling/'+str(date_)[5:10]+shift+'.xlsx'
                    
                    with pd.ExcelWriter(file_name) as writer:
                        create_empty_df(fake_ranking_100).to_excel(writer, sheet_name='ranking_100')
                        create_empty_df(fake_times_100).to_excel(writer, sheet_name='times_100')
                        create_empty_df(fake_ranking_50).to_excel(writer, sheet_name='ranking_50')
                        create_empty_df(fake_times_50).to_excel(writer, sheet_name='times_50')
                    writer.save()

def date_reader():
    import pandas as pd
    import pickle
    f = open('date.pckl', 'rb')
    obj = pickle.load(f)
    f.close()
    return pd.Timestamp(obj)

#it should let you know when was the last time the table was updated 
def update_time(start,finish,date):
    import datetime
    import time
    from apps import functions as fx
    hour=int(time.ctime()[11:13])
    today=time.ctime()[8:10]
    user_input=str(date)[8:10]
    
    if int(today)==int(user_input):
        if hour>=20 or hour<=4:
            now = datetime.datetime.now()  
            return 'Last update '+now.strftime("%H:%M %m-%d")
        else:
            if hour>=start and hour<=finish:
                now = datetime.datetime.now()    
                return 'Last update '+now.strftime("%H:%M %m-%d")
            elif start==12 and finish==20:
                yesterday = datetime.date.today()-datetime.timedelta(days=1)
                return f'Last update {finish}:00 {str(yesterday)[5:]}'
            else:
                today = datetime.date.today()
                return f'Last update {finish}:00 {str(today)[5:]}'
    else:
        return f'Last update {finish}:00 {str(date)[5:10]}'

    # import pandas as pd
    # from apps import functions as fx
    # main=fx.main_table(file_name)
    # main.insert(loc=0,column='Reference', value=main.index)
    # main['Rate']['Total']=main.loc['Total'][2:-1][main.loc['Total'][2:-1]>0].mean()
    # main['Rate'] = main['Rate'].map('{:,.2f}'.format)
    # df=main_table(file_name)
    # aux=df.T.iloc[:-1,:]
    # aux=aux[1:]
    # aux=aux[aux['Total']>0]
    # aux['Hour']=aux.index
    # return (main,aux)
 
def summary(n_shift,m_shift,a_shift,date):
    import time 
    import pandas as pd 
    hour=int(time.ctime()[11:13])
    u_input_day=str(date)[8:10]
    today_=time.ctime()[8:10]
    
    def get_summary(sum_):
        total=pd.DataFrame(columns=['Expected Results','Net Results','Difference'], index=pd.Series(range(4)))
        total.iloc[0]=n_shift.iloc[0]
        total.iloc[1]=m_shift.iloc[0]
        total.iloc[2]=a_shift.iloc[0]
        reference=['Night shift','Morning shift','Afternoon shift','Total']
        total.insert(0,'Reference',reference)
        temp_=['Total']
        for column in ['Expected Results','Net Results','Difference']:
            temp_.append(sum_.iloc[0][column])
        total.iloc[3]=temp_
        return total

    if today_==u_input_day:
        if hour<=4:
            sum_=n_shift
            total=get_summary(sum_)
        if hour<=13:
            sum_=n_shift+m_shift
            total=get_summary(sum_)
        else:
            sum_=n_shift+m_shift+a_shift
            total=get_summary(sum_)
        return total
    else:
        sum_=n_shift+m_shift+a_shift
        total=get_summary(sum_)
        return total

#it ensure the existence of the 3 previous days, and the current day. 
#reads the database for the sorting 
def sorting_get_data():
    import pandas as pd
    import numpy as np
    from datetime import date
    import pyodbc

    connection = pyodbc.connect('DRIVER={SQL Server};'

                                'SERVER=nj01prdbidb01.intranet.biz.freshdirect.com;'

                                'DATABASE=DASHBOARD;'

                                'UID=DASH_READONLY;'

                                'PWD=Mbers0nyon#123;'
                                
                                "autocommit = True")
    query="""
        select distinct pt.CNTR_NBR lpn,pt.CREATE_DATE_TIME Sort_date_time, convert(date,pt.CREATE_DATE_TIME) Sort_Date,substring(TO_LOC.LVL,1,1) Lvl,pt.USER_ID, us.USER_FIRST_NAME+','+us.USER_LAST_NAME Usr, to_loc.DSP_LOCN To_loc,

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end as Sort_hour,


        case 	when

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('04AM','05AM','06AM','07AM','08AM','09AM','10AM','11AM') then 'Morning shift'

            when
        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('12PM','01PM','02PM','03PM','04PM','05PM','06PM','07PM') then 'Afternoon shift'

            When 

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('08PM','09PM','10PM','11PM','12AM','01AM','02AM','03AM') then 'Night shift'

            end as Shft

        from PROD_TRKG_TRAN_WMS pt 
        left outer join LOCN_HDR_WMS fr on fr.LOCN_ID = pt.FROM_LOCN
        left outer join LOCN_HDR_WMS to_loc on to_loc.LOCN_ID = pt.TO_LOCN
        join UCL_USER_WMS us on us.USER_NAME = pt.USER_ID
        where  1=1
        and ( to_loc.AISLE = 'AM' and substring(TO_LOC.LVL,2,1) = 'F' )
    """
    # Setting up a cursor.
    cursor = connection.cursor()
    # fetch data function.
    data = cursor.execute(query).fetchall()
    connection.close()                           

    reference=['lpn','Sort_date_time','Sort_Date','Lvl','USER_ID','Usr','To_loc','Sort_hour','Shft']
    df=pd.DataFrame(columns=reference,index=np.arange(len(data)))
    for item in range(len(reference)):
        for row in range(len(data)):
            df[reference[item]][row]=data[row][item]

    out_path='archive\Sorting\sorting_database.xlsx'
    writer = pd.ExcelWriter(out_path , engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    return df

#returns 2 tables main and aux to be used in the views of sorting and putaway.
def sorting_tables(shift,day,schedule):
        import datetime as dt
        import pandas as pd
        from apps import functions as fx
        factor=1.2 #this is the general efficiency use to adjust the computation of rates and expected values 
    #this create the main table and aux table used to show the rates of each operator
        data=pd.read_excel('archive/Sorting/sorting_database.xlsx')
        def putaway_rate(user,hour,day): 
            rate=len(data[(data['Usr']==user)&(data['Sort_hour']==hour)&(data['Sort_Date']==str(day)[:10])]['lpn'].unique())
            return rate
        data=data.sort_values('Sort_date_time',ascending=False)
        users=data[(data['Sort_Date']==str(day)[:10]) & (data['Shft']==shift)]['Usr'].unique()
        df=pd.DataFrame(columns=schedule, index=users)
        for name in users:
            for hour in schedule:
                df[hour][name]= putaway_rate(name,hour,day)
        rates=df[df[df.columns]>20].mean(axis=1)
        df['Rates']=rates
        df=df.sort_values('Rates',ascending=False)
        temp=df.sum(axis=0)
        df=df.T
        df['Total']=temp
        df=df.T
        df['Rates']['Total']=df.loc['Total'][1:-1].mean()
        df.insert(0,'Name',df.index)
        aux=df[df.columns[1:]].T
        aux['hours']=aux.index
        aux=aux[:-1]
      
    #this is a patch to add working hour and total and fix the rate
        df=df.fillna(0)
        maximum_time_between_pulls=0.05
        def get_user_working_hours(user,database=data,shift=shift):
                user_data=database[(database['Usr']==user) & (database['Shft']==shift) & (database['Sort_Date']==str(day)[:10])].sort_values('Sort_date_time',ascending=False)
                time=list()
                for hour in user_data['Sort_hour'].unique():
                        user_data_byhour=user_data[user_data['Sort_hour']==hour]
                        
                        for pull in range(len(user_data_byhour.index)-1):
                            first=user_data_byhour.iloc[pull]['Sort_date_time']
                            second=user_data_byhour.iloc[pull+1]['Sort_date_time']
                            delta_time=(first-second).seconds/3600
                            
                            if delta_time<=maximum_time_between_pulls:
                                time.append(delta_time)
                            else:
                                time.append(maximum_time_between_pulls)
                        
                return sum(time)
        df['Working Hours']=df.apply(lambda x:get_user_working_hours(x['Name']),axis=1)
        df['Total']=df[schedule].sum(axis=1)
        df['Rates']=df['Total']/(df['Working Hours']*factor)
        df['Ranking']=0.5*df['Total']/max(df['Total'])+0.5*df['Rates']/max(df['Rates'])
        
        columns_order=['Name']
        columns_order.extend(schedule)
        columns_order.extend(['Working Hours', 'Total','Rates','Ranking'])
        df=df[columns_order]
        df=df[df.index!='Total'].sort_values('Ranking',ascending=False)
        total=df.sum(axis=0)
        total['Name']='Total'
        total['Rates']=total[schedule].mean()
        df=df.append(total,ignore_index=True)
        
    #This is to create the floors table (it indicates how many ilpns is going to each floor)
        data=pd.read_excel('archive/Sorting/sorting_database.xlsx')
        shifts_=['Night shift','Morning shift','Afternoon shift']
        floors_table=pd.DataFrame(columns=shifts_, index=range(1,5))
        for shift_ in shifts_:
            content=list(data[(data['Sort_Date']==str(day)[:10]) & (data['Shft']==shift_)].groupby('Lvl').count()['lpn'])
            if content:
                floors_table[shift_]=content
            else:
                floors_table[shift_]=[0,0,0,0]

        floors_table.insert(0,'level',['A1','A2','A3','A4'])
        floors_table['Total']=floors_table[shifts_].sum(axis=1)

    #this is to create the resutls table
        #alternative method 
            # temp=df[schedule]
            # temp=temp[:-1]
            # headcount=temp[temp>20].count(axis=0)
            # expected_results=headcount*100
            # expected_results.sum()
            # result_table=pd.DataFrame(columns=['Expected Results','Net Results','Difference'],index=range(1))
            # result_table['Expected Results']=expected_results.sum()
            # result_table['Net Results']=df[schedule].sum(axis=1)[:-1].sum()
            # result_table['Difference']=result_table['Net Results']-result_table['Expected Results']
        result_table=pd.DataFrame(columns=['Expected Results','Net Results','Difference'],index=range(1))
        result_table['Net Results']=int(df['Total'].iloc[-1])
        result_table['Expected Results']=int(df[:-1]['Working Hours'].sum()*100*factor)
        result_table['Difference']=result_table['Net Results']-result_table['Expected Results']
        
    #here everything is sorted into different sheets of the same excel file (1 per shift per day)
        name='archive/Sorting/'+str(day)[5:10]+'Sorting '+shift+'.xlsx'   
        with pd.ExcelWriter(name) as writer:
            df.to_excel(writer, sheet_name='main')
            aux.to_excel(writer, sheet_name='aux')
            floors_table.to_excel(writer, sheet_name='floors_table')
            result_table.to_excel(writer, sheet_name='results_table')
        writer.save()

def initializer_Sorting(finish,start,decrement=-1):
    import pandas as pd
    import datetime as dt
    from apps import functions as fx
    night=['01AM', '02AM', '03AM', '08PM', '09PM', '10PM', '11PM', '12AM']
    morning=['04AM','05AM','06AM','07AM','08AM','09AM','10AM','11AM']
    afternoon=['12PM','01PM', '02PM', '03PM', '04PM', '05PM', '06PM', '07PM']
    shifts=[('Night shift',night),('Morning shift',morning),('Afternoon shift',afternoon)]
    today=dt.date.today()
    for i in range(finish,start,decrement):
        day=today-dt.timedelta(days=i)
        for shift in shifts:
            fx.sorting_tables(shift[0],day,shift[1])

def graphs(date_):
    import pandas as pd
    from apps import Afternoon, Morning,Night, functions as fx
    import plotly.graph_objects as go
    def get_bargraph(total,title,date_):
        total.columns[1:]
        total.loc[0][1:]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=total.columns[1:],
            y=total.loc[0][1:],
            name=total.loc[0][0],
            marker_color='#055050',
            text=total.loc[0][1:],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=total.columns[1:],
            y=total.loc[1][1:],
            name=total.loc[1][0],
            marker_color='#099292',
            text=total.loc[1][1:],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=total.columns[1:],
            y=total.loc[2][1:],
            name=total.loc[2][0],
            marker_color='#68bdef',
            text=total.loc[2][1:],
            textposition='auto'
        ))
        fig.add_trace(go.Bar(
            x=total.columns[1:],
            y=total.loc[3][1:],
            name=total.loc[3][0],
            marker_color='#4c6df1',
            text=total.loc[3][1:],
            textposition='auto'
        ))
        
        fig.update_layout(barmode='group', xaxis_tickangle=0,
        title=title+' '+str(date_)[5:10],
        titlefont=dict(size=20),
        xaxis=dict(titlefont_size=20,tickfont_size=20),
        yaxis=dict(title='Number of ilpns', titlefont_size=20,tickfont_size=20)
        )
        
        return fig 

 #Summary of pulling activities
    def results_table(date_, shift):
        file_name=str(date_)[5:10]+shift+'.xlsx'
        df=fx.main_table(file_name)
        result=fx.get_results_table(file_name,df)
        return result
    m_shift= results_table(date_,'Morning shift')
    n_shift= results_table(date_,'Night shift')
    a_shift= results_table(date_,'Afternoon shift')
    total= fx.summary(n_shift,m_shift,a_shift,date_)
    pulling_fig=get_bargraph(total,'Summary of Pulling Activities',date_)

 #Summary of Sorting activities
    day=str(date_)[5:10]
    total= fx.summary(n_shift,m_shift,a_shift,date_)
    night=pd.read_excel('archive/Sorting/'+day+'Sorting Night shift.xlsx',sheet_name='results_table').loc[0][1:]
    afternoon=pd.read_excel('archive/Sorting/'+day+'Sorting Afternoon shift.xlsx',sheet_name='results_table').loc[0][1:]
    morning=pd.read_excel('archive/Sorting/'+day+'Sorting Morning shift.xlsx',sheet_name='results_table').loc[0][1:]
    sorting_total=pd.DataFrame(columns=morning.index, index=range(4))
    sorting_total.loc[0]=night
    sorting_total.loc[1]=morning
    sorting_total.loc[2]=afternoon
    sorting_total.sum(axis=0)
    sorting_total.loc[3]=sorting_total.sum(axis=0)
    sorting_total.insert(0,'Shift',['Night shift','Morning shift','Afternoon shift','Total'])
    sorting_fig=get_bargraph(sorting_total,'Summary of Sorting Activities',date_)

    return(pulling_fig,sorting_fig)

#The following functions are exclusive for Fill Active
def fill_get_data():
    import pandas as pd
    import numpy as np
    from datetime import date
    import pyodbc

    connection = pyodbc.connect('DRIVER={SQL Server};'

                                'SERVER=nj01prdbidb01.intranet.biz.freshdirect.com;'

                                'DATABASE=DASHBOARD;'

                                'UID=DASH_READONLY;'

                                'PWD=Mbers0nyon#123;'
                                
                                "autocommit = True")
    query="""
  
        select distinct pt.CNTR_NBR lpn,pt.CREATE_DATE_TIME Fill_date_time, convert(date,pt.CREATE_DATE_TIME) Fill_Date,TO_LOC.ZONE Fill_Zone,pt.USER_ID, us.USER_FIRST_NAME+','+us.USER_LAST_NAME Usr, to_loc.DSP_LOCN To_loc,

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end as Fill_hour,


        case 	when

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('04AM','05AM','06AM','07AM','08AM','09AM','10AM','11AM') then 'Morning shift'

            when
        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('12PM','01PM','02PM','03PM','04PM','05PM','06PM','07PM') then 'Afternoon shift'

            When 

        CASE DATEPART(HOUR, pt.CREATE_DATE_TIME)
            WHEN 0 THEN  '12AM'
            WHEN 1 THEN   '01AM'
            WHEN 2 THEN   '02AM'
            WHEN 3 THEN   '03AM'
            WHEN 4 THEN   '04AM'
            WHEN 5 THEN   '05AM'
            WHEN 6 THEN   '06AM'
            WHEN 7 THEN   '07AM'
            WHEN 8 THEN   '08AM'
            WHEN 9 THEN   '09AM'
            WHEN 10 THEN '10AM'
            WHEN 11 THEN '11AM'
            WHEN 12 THEN '12PM'
            ELSE Format(DATEPART(HOUR, pt.CREATE_DATE_TIME)-12,'00') + 'PM'end

            in ('08PM','09PM','10PM','11PM','12AM','01AM','02AM','03AM') then 'Night shift'

            end as Shft

        from PROD_TRKG_TRAN_WMS pt 
        inner join (select distinct lp.TC_LPN_ID from LPN_WMS lp where lp.LPN_FACILITY_STATUS = 96 and lp.LAST_UPDATED_DTTM > cast(getdate()-6 as date))lp on lp.TC_LPN_ID = pt.CNTR_NBR
        left outer join LOCN_HDR_WMS fr on fr.LOCN_ID = pt.FROM_LOCN
        left outer join LOCN_HDR_WMS to_loc on to_loc.LOCN_ID = pt.TO_LOCN
        join UCL_USER_WMS us on us.USER_NAME = pt.USER_ID
        left outer join (select emp.personnum,emp.SUPERVISORID from EMPLOYEEV42_KRONO emp)emp on emp.personnum = pt.USER_ID
        where  1=1
        and to_loc.LOCN_CLASS = 'A'
        and pt.TRAN_TYPE = 300
        and substring(pt.MENU_OPTN_NAME,1,4) = 'Fill'
        and SUBSTRING(to_loc.zone,1,1) = 'A'
        and (emp.SUPERVISORID not in ('21187','44') or emp.SUPERVISORID is null)
  
  
  """
    
    # Setting up a cursor.
    cursor = connection.cursor()
    # fetch data function.
    data = cursor.execute(query).fetchall()
    connection.close()                           

    reference=['lpn','Sort_date_time','Sort_Date','Lvl','USER_ID','Usr','To_loc','Sort_hour','Shft']
    df=pd.DataFrame(columns=reference,index=np.arange(len(data)))
    for item in range(len(reference)):
        for row in range(len(data)):
            df[reference[item]][row]=data[row][item]

    out_path='archive\Fill_Active\Fill_database.xlsx'
    writer = pd.ExcelWriter(out_path , engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()

def fill_get_table(shift,schedule,day):
    import pandas as pd
    import datetime 
    data=pd.read_excel('archive/Fill_Active/fill_database.xlsx')
    data=data[(data['Sort_Date']==str(day)[:10])&(data['Shft']==shift)].sort_values('Sort_date_time',ascending=False)

    def fill_rate(user,hour,day): 
        rate=len(data[(data['Usr']==user)&(data['Sort_hour']==hour)]['lpn'].unique())
        return rate
    users=data['Usr'].unique()
    fill_table=pd.DataFrame(columns=schedule, index=users)
    for name in users:
        for hour in schedule:
            fill_table[hour][name]= fill_rate(name,hour,day)
    rates=fill_table[fill_table[fill_table.columns]>20].mean(axis=1)
    fill_table['Rates']=rates
    fill_table=fill_table.sort_values('Rates',ascending=False)
    temp=fill_table.sum(axis=0)
    fill_table=fill_table.T
    fill_table['Total']=temp
    fill_table=fill_table.T

    last_floor=list()
    last_time=list()
    for name in fill_table.index:
        if name!='Total':
            user_last_record=data[data['Usr']==name].iloc[0]
            last_floor.append(user_last_record['Lvl'])
            last_time.append(user_last_record['Sort_date_time'])
        else:
            last_floor.append(0)
            last_time.append(0)

    fill_table.insert(0,'Floor',last_floor)
    fill_table.insert(0,'Last Record',last_time)
    fill_table['Rates']['Total']=fill_table.loc['Total'][1:-1].mean()
    fill_table.insert(0,'Name',fill_table.index)
    fill_table=fill_table.reset_index(drop=True)
    fill_table=fill_table.fillna(0)[:-1]


    # this is in hours, so 0.05*60 min its 3 minutes
    maximum_time_between_pulls=0.05
    def get_user_working_hours(user,database=data):
            user_data=database[(database['Usr']==user)].sort_values('Sort_date_time',ascending=False)
            time=list()
            for hour in user_data['Sort_hour'].unique():
                    user_data_byhour=user_data[user_data['Sort_hour']==hour]
                    for pull in range(len(user_data_byhour.index)-1):
                        first=user_data_byhour.iloc[pull]['Sort_date_time']
                        second=user_data_byhour.iloc[pull+1]['Sort_date_time']
                        delta_time=(first-second).seconds/3600
                        
                        if delta_time<=maximum_time_between_pulls:
                            time.append(delta_time)
                        else:
                            time.append(maximum_time_between_pulls)
            return sum(time)
    fill_table['Working Hours']=fill_table.apply(lambda x:get_user_working_hours(x['Name']),axis=1)
    fill_table['Total']=fill_table[schedule].sum(axis=1)

    fill_table['Ranking']=0.3*fill_table['Working Hours']/max(fill_table['Working Hours'])+0.3*fill_table['Total']/max(fill_table['Total'])+0.4*fill_table['Rates']/max(fill_table['Rates'])
    columns_order=['Name','Floor']
    columns_order.extend(schedule)
    columns_order.extend(['Working Hours', 'Total','Rates','Ranking','Last Record'])
    fill_table=fill_table[columns_order]
    fill_table=fill_table[fill_table.index!='Total'].sort_values('Ranking',ascending=False)
    total=fill_table.sum(axis=0)
    total['Name']='Total'
    total['Floor']='All'
    fill_table=fill_table.append(total,ignore_index=True)

    def time_since_last_pull(last_record):
        import datetime
        last_record=pd.Timestamp(last_record)
        return (datetime.datetime.now()-last_record).seconds/60
    fill_table['T_since_Pull']=fill_table.apply(lambda x: time_since_last_pull(x['Last Record']),axis=1)
    
    file_name='archive/Fill_Active/'+str(day)[5:10]+'Fill '+shift+'.xlsx'
    fill_table.to_excel(file_name)

def fill_result_table(file_name):
    import pandas as pd
    factor=1.2
    main=pd.read_excel(file_name).round(2)
    expected_result=main['Working Hours'].sum()*100*factor
    net_result=main['Total'].sum()
    difference=net_result-expected_result
    result_table=pd.DataFrame(columns=['Expected Results','Net Results', 'Difference'], index=range(1))
    result_table['Expected Results']=expected_result
    result_table['Net Results']=net_result
    result_table['Difference']=difference
    return result_table.round(0)

def fill_get_rates_fig(file_name,name='Total'):
    import plotly.graph_objs as go
    import plotly.express as px
    import pandas as pd
    main=pd.read_excel(file_name).round(2)
    no_show=['Unnamed: 0','Ranking','Last Record','T_since_Pull']
    no_show.extend(['Floor','Working Hours'])
    aux=main.drop(no_show,axis=1)
    aux=aux.set_index('Name').T
    aux['hour']=aux.index
    rate=float(main[main['Name']=='Total'].T[3:-6].mean())
    aux2=aux[:-2] 
    if name=='Total':
        fig=px.line(aux2, x='hour', y='Total', title='Total Performance curve')
        fig.add_trace(go.Scatter(x=aux2.hour, y=[rate for i in aux.index],
                                mode='lines',
                                name="Average {:,.2f} ilpns/hour".format(rate)))
        return fig
    else:
        fig=px.line(aux2, x='hour', y=name, title=name+' Performance curve')
        fig.add_trace(go.Scatter(x=aux2.hour, y=[aux[name].loc['Rates'] for i in aux.index],
                                mode='lines',
                                name="Average {:,.2f} ilpns/hour".format(aux[name].loc['Rates'])))

        return fig

def fill_get_load_fig(file_name):
    import plotly.graph_objs as go
    import plotly.express as px
    import pandas as pd
    main=pd.read_excel(file_name).round(2)
    aux=main.groupby(['Floor']).sum()
    aux['Floor']=aux.index
    aux=aux[['Floor','Total']][:-1]
    fig = px.bar(aux, x='Floor', y='Total',color='Total',text='Total',color_continuous_scale=['#060000','#EC9C08','#F71802'])
    return fig

def fill_initializer(finish,start,decrement=-1):
    import pandas as pd
    import datetime as dt
    from apps import functions as fx
    night=['01AM', '02AM', '03AM', '08PM', '09PM', '10PM', '11PM', '12AM']
    morning=['04AM','05AM','06AM','07AM','08AM','09AM','10AM','11AM']
    afternoon=['12PM','01PM', '02PM', '03PM', '04PM', '05PM', '06PM', '07PM']
    shifts=[('Night shift',night),('Morning shift',morning),('Afternoon shift',afternoon)]
    today=dt.date.today()
    for i in range(finish,start,decrement):
        day=today-dt.timedelta(days=i)
        for shift in shifts:
            try:
                fx.fill_get_table(shift[0],shift[1],day)
            except:
                pass
    shifts=['Morning shift','Afternoon shift','Night shift']
 #to complete the missing shift with a fake daraframe(so the website can show 0)
    for i in range(finish,start,decrement):
            for shift in shifts: 
                try:
                    date_=dt.datetime.today()-dt.timedelta(days=i)
                    string=str(date_)[5:10]+'Fill '+shift+'.xlsx'
                    pd.read_excel('archive/Fill_Active/'+string)
                except:
                    yesterday=dt.datetime.today()-dt.timedelta(days=1)
                    file_name=str(yesterday)[5:10]+'Fill '+shift+'.xlsx'
                    fake_file_active=pd.read_excel('archive/Fill_Active/'+file_name)
                    def create_empty_df(df):
                        aux=pd.DataFrame(columns=df.columns,index=df.index)
                        aux['Name']=df['Name']
                        return aux.T[1:].T
                    file_name='archive/Fill_Active/'+str(day)[5:10]+'Fill '+shift+'.xlsx'
                    
                    with pd.ExcelWriter(file_name) as writer:
                        create_empty_df(fake_file_active).to_excel(writer)
                    writer.save()

def summary_get_main(date):
    from apps import functions as fx
    import pandas as pd
    fill=list()
    pull=list()
    sort=list()
    shifts=['Morning shift', 'Afternoon shift','Night shift']
    for shift in shifts: 
        file_name=str(date)[5:10]+shift+'.xlsx'
        pull.append(fx.pulling_get_result_table(file_name))
        file_name='archive/Fill_Active/'+str(date)[5:10]+'Fill '+shift+'.xlsx'
        fill.append(fx.fill_result_table(file_name))
        file_name='archive/Sorting/'+str(date)[5:10]+'Sorting '+shift+'.xlsx'
        sort.append(pd.read_excel(file_name,sheet_name='results_table').T[1:].T)
    pull=pd.concat(pull,axis=0).sum()
    fill=fill[0]+fill[1]+fill[2]
    sort=sort[0]+sort[1]+sort[2]
    summary=pd.DataFrame(columns=['Pulling','Sorting','Fill Active'],index=['Expected Results','Net Results','Difference'])
    summary['Pulling']=list(pull)
    summary['Sorting']=list(sort.iloc[0])
    summary['Fill Active']=list(fill.iloc[0])
    summary=summary.T
    summary.insert(0,'Reference',['Pulling','Sorting','Fill Active'])
    return summary

#this is for shuttle
def shuttle_get_table():
  #gets data from database
    import pandas as pd
    import numpy as np
    from datetime import date
    import pyodbc

    connection = pyodbc.connect('DRIVER={SQL Server};'

                                'SERVER=nj01prdbidb01.intranet.biz.freshdirect.com;'

                                'DATABASE=DASHBOARD;'

                                'UID=DASH_READONLY;'

                                'PWD=Mbers0nyon#123;'
                                
                                "autocommit = True")
    query="""
        select case when replen.RDate is not null then Replen.RDate when trans.TDate is not null then trans.TDate else cycle.Date end [Date], case when replen.DisplayName is not null then replen.DisplayName when trans.DisplayName is not null then trans.DisplayName else cycle.DisplayName end [Name], replen.iLPNs,replen.Replen, trans.Transfer, cycle.Totes [CC_Totes], cycle.Compartments [CC_Quads]  
        from (
        select convert(varchar(8),td.CompletedDateTime,1) [RDate], auser.displayname,count(distinct slpn.Lpn) iLPNs,count(td.id) [Replen] 
        from TaskDetail_WES td 
        join ContainerLpn_WES slpn on slpn.Container_Id = td.SourceContainer_Id
        join ContainerLpn_WES dlpn on dlpn.Container_Id = td.DestinationContainer_Id
        join AuthUser_WES auser on auser.userid = td.ActualUser
        where TaskType_Id = 440 /* and TaskPlannerId = 103 */ and td.Status  = 'COMPLETED' and holdstatus is null
        group by convert(varchar(8),td.CompletedDateTime,1),auser.displayname
        ) replen
        full join (select convert(varchar(8),td.CompletedDateTime,1) [TDate],auser.DisplayName,count(td.id) [Transfer]  
        from TaskDetail_WES td  
        join AuthUser_WES auser on auser.UserId = td.ActualUser
        where TaskType_Id = 420
        and HoldStatus is null  and td.Status  = 'COMPLETED' and ReasonCode_Id is null 
        group by convert(varchar(8),td.CompletedDateTime,1),auser.DisplayName ) trans on trans.DisplayName = replen.DisplayName and trans.TDate = replen.RDate
        full join (select  convert(varchar,td.completeddatetime,1) Date,auser.DisplayName, count(distinct substring(lpn,1,7)) [Totes],count(Lpn) [Compartments]
        from TaskDetail_WES td 
        join AuthUser_WES auser on auser.userid = td.ActualUser
        join ContainerLpn_WES lpn on lpn.Container_Id = td.SourceContainer_Id 
        where td.TaskType_Id in (439,442,443,444) and ReasonCode_Id = 34 and td.Status  = 'COMPLETED' and Lpn.Lpn like 'S%' and holdstatus is null
        group by convert(varchar,completeddatetime,1) ,auser.DisplayName
        ) cycle on case when replen.RDate is not null then Replen.RDate when trans.TDate is not null then trans.TDate end =  cycle.Date and case when replen.DisplayName is not null then replen.DisplayName when trans.DisplayName is not null then trans.DisplayName end = cycle.DisplayName
        order by convert(datetime, [Date], 1) desc, name

    """

    # Setting up a cursor.
    cursor = connection.cursor()
    # fetch data function.
    data = cursor.execute(query).fetchall()
    connection.close()                           
  #organizes data into a dataframe and save the information by day
    import datetime
    hoy=datetime.date.today()
    hoy=str(hoy.strftime('%m/%d/%Y'))[:6]+str(hoy.strftime('%m/%d/%Y'))[-2:]
    date=hoy
    temp=list()
    for element in data:
        temp.append([element[0],element[1],element[2]])
    df=pd.DataFrame(columns=range(len(data)),index=['Date','Name','ilpns'])
    for item in range(len(temp)):
        df[item]=temp[item]
    df=df.T.sort_values('Date',ascending=False)
    df=df[df['Date']==date]
    df=df.dropna()
    df.to_excel('archive/Shuttle/'+date.replace('/','_')+'.xlsx')

def shuttle_read(date):
    import pandas as pd
    import plotly.express as px
    import datetime
    try:
        day=date.replace('/','_')
        df=pd.read_excel('archive/Shuttle/'+day+'.xlsx')
        fig=px.bar(df, x='Name', y='ilpns',color='ilpns',text='ilpns',title=date)
        return (df,fig)
    except:
        yesterday=pd.Timestamp(date)-datetime.timedelta(days=1)
        yesterday=str(yesterday.strftime('%m/%d/%Y'))[:6]+str(yesterday.strftime('%m/%d/%Y'))[-2:]
        day=str(yesterday).replace('/','_')
        print(day)
        df=pd.read_excel('archive/Shuttle/'+day+'.xlsx')
        fig=px.bar(df, x='Name', y='ilpns',color='ilpns',text='ilpns',title=date)
        return (df,fig)