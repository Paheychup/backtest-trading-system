import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#------------------------------------------------------------------------------
def group_by_stat_CTr_CTr_In(Str_id, df_all_deals, df_ent_params, dict_str_all_deals, column='Total'):   
    df=dict_str_all_deals[Str_id].copy()
    df=pd.merge(df, df_ent_params, how='inner',on='Str_id')
    df['Total']=df['SL']+df['TP']
    df['Cumsum']=df['Total'].cumsum()
    df['HighVal']=df['Cumsum'].cummax()
    df['DrDown']=df['Cumsum']-df['HighVal']
    df['LowVal']=df['Cumsum'].cummin()
    df['DrDown2']=df['Cumsum']-df['LowVal']
    df_Total=df.groupby(['CTr','CTr_In'],as_index=False)['Total'].sum()
    df_AVG_deal=df.groupby(['CTr','CTr_In'],as_index=False)['Total'].mean().rename(columns={'Total':'AVG_deal'})
    df_Count=df.groupby(['CTr','CTr_In'],as_index=False)['Total'].count().rename(columns={'Total':'Count'})
    df_DrDown=df.groupby(['CTr','CTr_In'],as_index=False)['DrDown'].min()
    df_DrDown2=df.groupby(['CTr','CTr_In'],as_index=False)['DrDown2'].max()
    df_result=pd.concat([df_Total,df_AVG_deal,df_Count,df_DrDown,df_DrDown2],axis=1)
    df_result = df_result.loc[:,~df_result.columns.duplicated()]
    
    df_CTr_unique=pd.DataFrame(pd.unique(df_result['CTr']))
    df=df_result.copy().reset_index(drop=True)
    df_CTr_In_unique=pd.DataFrame(pd.unique(df['CTr_In']))
    names=tuple(list(round(df_CTr_unique[0],2)))
    r=[]
    dict_r={}
    keys=range(1,len(df_CTr_unique)+1)
    values=list(range(0,len(df_CTr_unique)))
    for i in keys:
        dict_r[i]=values[i-1]
    plt.figure(figsize=(12, 9))
    for i in range(0,len(df_CTr_In_unique)):
        CTr_In=round(df_CTr_In_unique.iloc[i,0],2)
        df_in=df[(df['CTr_In']==CTr_In)].loc[:,:].copy().reset_index(drop=True)
        barWidth = 1/(len(df_CTr_In_unique)+1)
        bars=df_in[column]
        r=[dict_r[x]+ barWidth*i for x in round(df_in['CTr'],2)]
        rgb = np.random.rand(3,)
        plt.bar(r, bars, color=rgb, width=barWidth, edgecolor='white', label=str(CTr_In))
        plt.xlabel('CTr', fontweight='bold')
        plt.ylabel(column, fontweight='bold')
        plt.xticks([r + (len(df_CTr_In_unique)/20) for r in range(len(names))], names)
        plt.title('CTr and CTr_In summary statistic  Str_id='+str(Str_id),fontsize=12,pad=10,fontweight='bold')
        plt.legend(title='CTr_In', fontsize ='large',bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.show()
#group_by_stat_CTr_CTr_In_func(Str_id=Str_id)