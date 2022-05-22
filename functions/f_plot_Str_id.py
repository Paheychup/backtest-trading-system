import pandas as pd
import matplotlib.pyplot as plt

def plot_Str_id(Str_id
            ,df_ent_params
            ,dict_str_all_deals
            ,CTr=0
            ,CTr_In=0
            ,CTr_Range=False):
    df_temp=dict_str_all_deals[Str_id]
    if CTr_Range==False:
        if CTr_In==0 and CTr==0:
            df_temp=df_temp.reset_index(drop=True)
            df_temp['Total']=df_temp['TP']+df_temp['SL']
            df_temp['Cumsum']=df_temp['Total'].cumsum()
            df_temp['HighVal']=df_temp['Cumsum'].cummax()
            df_temp['DrDown']=df_temp['Cumsum']-df_temp['HighVal']

            df_Total=df_temp.groupby(['Str_id'],as_index=False)['Total'].sum()
            df_AVG_deal=df_temp.groupby(['Str_id'],as_index=False)['Total'].mean().rename(columns={'Total':'AVG_deal'})
            df_Count=df_temp.groupby(['Str_id'],as_index=False)['Total'].count().rename(columns={'Total':'Count'})
            df_DrDown=df_temp.groupby(['Str_id'],as_index=False)['DrDown'].min()
            df_result=pd.concat([df_Total,df_AVG_deal,df_Count,df_DrDown],axis=1)
            df_result = df_result.loc[:,~df_result.columns.duplicated()]
        elif CTr!=0 and CTr_In==0:
            df_temp=df_temp[(df_temp['CTr']==CTr)]

            if len(df_temp)==0:
                max_CTr=df_temp['CTr'].max()
                print('\nTFilter with CTr='+str(CTr)+'n\Choose another value'+'\nMax data CTr='+str(max_CTr))

            df_temp=df_temp.reset_index(drop=True)
            df_temp['Total']=df_temp['TP']+df_temp['SL']
            df_temp['Cumsum']=df_temp['Total'].cumsum()
            df_temp['HighVal']=df_temp['Cumsum'].cummax()
            df_temp['DrDown']=df_temp['Cumsum']-df_temp['HighVal']

            df_Total=df_temp.groupby(['Str_id'],as_index=False)['Total'].sum()
            df_AVG_deal=df_temp.groupby(['Str_id'],as_index=False)['Total'].mean().rename(columns={'Total':'AVG_deal'})
            df_Count=df_temp.groupby(['Str_id'],as_index=False)['Total'].count().rename(columns={'Total':'Count'})
            df_DrDown=df_temp.groupby(['Str_id'],as_index=False)['DrDown'].min()
            df_result=pd.concat([df_Total,df_AVG_deal,df_Count,df_DrDown],axis=1)
            df_result = df_result.loc[:,~df_result.columns.duplicated()]
            
        elif CTr!=0 and CTr_In!=0:
            df_temp=df_temp[(df_temp['CTr']==CTr) & (df_temp['CTr_In']==CTr_In)]

            if len(df_temp)==0:
                max_CTr=df_temp['CTr'].max()
                max_CTr_In=df_temp['CTr_In'].max()
                print('\nTFilter with CTr='+str(CTr)+' and CTr_In='+str(CTr_In)+'n\Choose another value'+'\nMax data CTr='+str(max_CTr)+'\nMax data CTr_In value='+str(max(CTr_In)))

            df_temp=df_temp.reset_index(drop=True)
            df_temp['Total']=df_temp['TP']+df_temp['SL']
            df_temp['Cumsum']=df_temp['Total'].cumsum()
            df_temp['HighVal']=df_temp['Cumsum'].cummax()
            df_temp['DrDown']=df_temp['Cumsum']-df_temp['HighVal']

            df_Total=df_temp.groupby(['Str_id'],as_index=False)['Total'].sum()
            df_AVG_deal=df_temp.groupby(['Str_id'],as_index=False)['Total'].mean().rename(columns={'Total':'AVG_deal'})
            df_Count=df_temp.groupby(['Str_id'],as_index=False)['Total'].count().rename(columns={'Total':'Count'})
            df_DrDown=df_temp.groupby(['Str_id'],as_index=False)['DrDown'].min()
            df_result=pd.concat([df_Total,df_AVG_deal,df_Count,df_DrDown],axis=1)
            df_result = df_result.loc[:,~df_result.columns.duplicated()]
    elif CTr_Range==True:
        df_temp=df_temp[(df_temp['CTr']>=CTr)]

        if len(df_temp)==0:
            max_CTr=df_temp['CTr'].max()
            print('\nTFilter with CTr='+str(CTr)+'n\Choose another value'+'\nMax data CTr='+str(max_CTr))

        df_temp=df_temp.reset_index(drop=True)
        df_temp['Total']=df_temp['TP']+df_temp['SL']
        df_temp['Cumsum']=df_temp['Total'].cumsum()
        df_temp['HighVal']=df_temp['Cumsum'].cummax()
        df_temp['DrDown']=df_temp['Cumsum']-df_temp['HighVal']

        df_Total=df_temp.groupby(['Str_id'],as_index=False)['Total'].sum()
        df_AVG_deal=df_temp.groupby(['Str_id'],as_index=False)['Total'].mean().rename(columns={'Total':'AVG_deal'})
        df_Count=df_temp.groupby(['Str_id'],as_index=False)['Total'].count().rename(columns={'Total':'Count'})
        df_DrDown=df_temp.groupby(['Str_id'],as_index=False)['DrDown'].min()
        df_result=pd.concat([df_Total,df_AVG_deal,df_Count,df_DrDown],axis=1)
        df_result = df_result.loc[:,~df_result.columns.duplicated()]
    
    print(pd.concat( [df_ent_params[df_ent_params['Str_id']==Str_id].reset_index(drop=True),df_result], axis=1 ))    

    plt.plot(df_temp['Cumsum'])
    #plt.title('Backtest-trading-system result  Str_id='+str(df_temp['Str_id'][0]))
    plt.title('Backtest-trading-system result  Str_id='+str(df_temp['Str_id'][0])+'\nCTr='+
            str(CTr)+'\nCTr_In='+str(CTr_In),loc='left',fontweight='bold')
    plt.ylabel('Total', fontweight='bold')
    plt.xlabel('Trades', fontweight='bold')
    plt.show()