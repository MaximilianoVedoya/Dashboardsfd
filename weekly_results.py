def weekly_results(shift):
    import pandas as pd 
    import datetime
    names=list()
    for i in range(1,8):
        day=datetime.date.today()-datetime.timedelta(days=i)
        file_name=str(day)[5:10]+shift+'.xlsx'
        df=pd.read_excel('archive/'+file_name)
        names.extend(list(df.Name))
    names=list(pd.Series(names).unique())
    dic={name:0 for name in names}
    for name in names:
        temp=list()
        for i in range(1,8):
            day=datetime.date.today()-datetime.timedelta(days=i)
            file_name=str(day)[5:10]+shift+'.xlsx'
            df=pd.read_excel('archive/'+file_name)
            df=df.dropna()
            x=list(df[df['Name']==name]['Rate'])
            if x:
                 temp.append(float(x[0]))
        if len(temp):
            dic[name]=[sum(temp)/len(temp),len(temp)]
        else:
            dic[name]=[sum(temp),len(temp)]
    df=pd.DataFrame(dic).T
    df.columns=['Rate','Days']
    df['Total ilpns']=df['Rate']*8*df['Days']
    df=df.sort_values('Rate',ascending=False)
    return df
with pd.ExcelWriter('results.xlsx') as writer:
        weekly_results('Morning shift').to_excel(writer, sheet_name='Morning shift')
        weekly_results('Afternoon shift').to_excel(writer, sheet_name='Afternoon shift')
        weekly_results('Night shift').to_excel(writer, sheet_name='Night shift')