import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#------------------------------------------------------------------------------
def group_by_stat_CTr(  df_all_deals
                           , dict_str_all_deals
                           , df_ent_params
                           , df_day_open
                           , Str_id
                           , CTr_In=0,column='Total'):
    df=dict_str_all_deals[Str_id].copy()
    df=pd.merge(df, df_ent_params, how='inner',on='Str_id')
    if CTr_In!=0:
        df=df[df['CTr_In']==CTr_In].reset_index(drop=True)
        if len(df)==0:print('\nFilter with CTr_In='+str(CTr_In)+' returns 0 rows');return None
        color='tomato'
    else:color='limegreen'
    df['Total']=df['SL']+df['TP']
    df['Cumsum']=df['Total'].cumsum()
    df['HighVal']=df['Cumsum'].cummax()
    df['DrDown']=df['Cumsum']-df['HighVal']
    df['LowVal']=df['Cumsum'].cummin()
    df['DrDown2']=df['Cumsum']-df['LowVal']
    df_Total=df.groupby(['CTr'],as_index=False)['Total'].sum()
    df_AVG_deal=df.groupby(['CTr'],as_index=False)['Total'].mean().rename(columns={'Total':'AVG_deal'})
    df_Count=df.groupby(['CTr'],as_index=False)['Total'].count().rename(columns={'Total':'Count'})
    df_DrDown=df.groupby(['CTr'],as_index=False)['DrDown'].min()
    df_DrDown2=df.groupby(['CTr'],as_index=False)['DrDown2'].max()
    df_result=pd.concat([df_Total,df_AVG_deal,df_Count,df_DrDown,df_DrDown2],axis=1)
    df_result = df_result.loc[:,~df_result.columns.duplicated()]

    k_Ent=df['k_Ent'][0];k_Ext=df['k_Ext'][0]
    barWidth=0.75; y_pos=np.arange(len(df_result)); height=df_result[column] #must be a series
    names=tuple(list(df_result['CTr'])) #names must be tuples
    plt.bar(y_pos,height,width = barWidth,color=color)
    plt.xticks(y_pos,names,rotation=0)
    plt.xlabel('CTr', fontweight='bold'); plt.ylabel(column, fontweight='bold')
    plt.title('CTr summary statistic Str_id='+str(df['Str_id'][0])+'  CTr_In='+str(CTr_In)+'\nk_Ent='+str(round(k_Ent,2))+'  k_Ext='+str(k_Ext)+
              '\nDate: ' + str(df_day_open['Date'].min()) +'-' + str(df_day_open['Date'].max())
              ,loc='left',fontsize=12,pad=10,fontweight='bold')
    plt.subplots_adjust(top=1.7,bottom=0.8); plt.subplots_adjust(bottom=0.4)
    plt.plot()
    #print('\n'+str(df_result.loc[:,['CTr','Total','AVG_deal','DrDown','DrDown2','Count']]))
    print('\n'+str(df_result.loc[:,['CTr','Total','AVG_deal','DrDown','Count']]))