import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#------------------------------------------------------------------------------
def group_by_stat2(df_all_deals,df_day_open,
                       CTr=0, CTr_In=0, column='AVG_deal',plt=plt,pd=pd):
    if CTr==0 and CTr_In==0:
        df_Total=df_all_deals.groupby(['Str_id','k_Ent','k_Ext'],as_index=False)['Total'].sum()
        df_AVG_deal=df_all_deals.groupby(['Str_id'],as_index=False)['Total'].mean().rename(columns={'Total':'AVG_deal'})
        df_Count=df_all_deals.groupby(['Str_id'],as_index=False)['Total'].count().rename(columns={'Total':'Count'})
        df_DrDown=df_all_deals.groupby(['Str_id'],as_index=False)['DrDown'].min()
        df_DrDown2=df_all_deals.groupby(['Str_id'],as_index=False)['DrDown2'].max()
        df_result=pd.concat([df_Total,df_AVG_deal,df_Count,df_DrDown,df_DrDown2],axis=1)
        df_result = df_result.loc[:,~df_result.columns.duplicated()]
    elif CTr!=0 and CTr_In==0:
        df_all_deals=df_all_deals[df_all_deals['CTr']==CTr].reset_index(drop=True)
        df_Total=df_all_deals.groupby(['Str_id','CTr','k_Ent','k_Ext'],as_index=False)['Total'].sum()
        df_AVG_deal=df_all_deals.groupby(['Str_id'],as_index=False)['Total'].mean().rename(columns={'Total':'AVG_deal'})
        df_Count=df_all_deals.groupby(['Str_id'],as_index=False)['Total'].count().rename(columns={'Total':'Count'})
        df_DrDown=df_all_deals.groupby(['Str_id'],as_index=False)['DrDown'].min()
        df_DrDown2=df_all_deals.groupby(['Str_id'],as_index=False)['DrDown2'].max()
        df_result=pd.concat([df_Total,df_AVG_deal,df_Count,df_DrDown,df_DrDown2],axis=1)
        df_result = df_result.loc[:,~df_result.columns.duplicated()]
    elif CTr==0 and CTr_In!=0:
        df_all_deals=df_all_deals[df_all_deals['CTr_In']==CTr_In].reset_index(drop=True)
        df_Total=df_all_deals.groupby(['Str_id','CTr_In','k_Ent','k_Ext'],as_index=False)['Total'].sum()
        df_AVG_deal=df_all_deals.groupby(['Str_id'],as_index=False)['Total'].mean().rename(columns={'Total':'AVG_deal'})
        df_Count=df_all_deals.groupby(['Str_id'],as_index=False)['Total'].count().rename(columns={'Total':'Count'})
        df_DrDown=df_all_deals.groupby(['Str_id'],as_index=False)['DrDown'].min()
        df_DrDown2=df_all_deals.groupby(['Str_id'],as_index=False)['DrDown2'].max()
        df_result=pd.concat([df_Total,df_AVG_deal,df_Count,df_DrDown,df_DrDown2],axis=1)
        df_result = df_result.loc[:,~df_result.columns.duplicated()]
    elif CTr!=0 and CTr_In!=0:
        df_all_deals=df_all_deals[(df_all_deals['CTr']==CTr) & (df_all_deals['CTr_In']==CTr_In)].reset_index(drop=True)
        df_Total=df_all_deals.groupby(['Str_id','CTr','CTr_In','k_Ent','k_Ext'],as_index=False)['Total'].sum()
        df_AVG_deal=df_all_deals.groupby(['Str_id'],as_index=False)['Total'].mean().rename(columns={'Total':'AVG_deal'})
        df_Count=df_all_deals.groupby(['Str_id'],as_index=False)['Total'].count().rename(columns={'Total':'Count'})
        df_DrDown=df_all_deals.groupby(['Str_id'],as_index=False)['DrDown'].min()
        df_DrDown2=df_all_deals.groupby(['Str_id'],as_index=False)['DrDown2'].max()
        df_result=pd.concat([df_Total,df_AVG_deal,df_Count,df_DrDown,df_DrDown2],axis=1)
        df_result = df_result.loc[:,~df_result.columns.duplicated()]
    print(df_result.iloc[:,:-1])   
    def data_barplot_k_func(df_result=df_result,column=column,CTr=CTr,CTr_In=CTr_In):
        df_k_Ext_unique=pd.DataFrame(pd.unique(df_result['k_Ext']))
        df_k_Ent_unique=pd.DataFrame(pd.unique(df_result['k_Ent']))
        names=tuple(list(round(df_k_Ent_unique[0],2)))
        barWidth = 1/(len(df_k_Ext_unique)+1)
        r=[]
        a=df_result.k_Ent.unique()
        b=np.arange(len(a))
        dict_r = {}
        for keys,values in zip(a,b):
            dict_r[keys]=values
        r_block=0
        plt.figure(figsize=(10, 8))
        for i in range(0,len(df_k_Ext_unique)):
            k_Ext=round(df_k_Ext_unique.iloc[i,0],2)
            df=df_result[(round(df_result['k_Ext'],2)==k_Ext)].loc[:,:].copy().reset_index(drop=True)
            bars=df[column]   
            r=[dict_r[x]+ barWidth*i for x in round(df['k_Ent'],2)]
            if r_block==0: r_tick=r; r_block=1
            rgb = np.random.rand(3,)
            plt.bar(r, bars, color=rgb, width=barWidth, edgecolor='white', label=str(k_Ext))
            plt.xlabel('k_Ent', fontweight='bold')
            plt.ylabel(column,fontweight='bold')
            title='Profit summary statistic with different coefficients'
            if CTr==0 and CTr_In==0:plt.title(title+'  CTr='+str(CTr)+'  CTr_In='+str(CTr_In),fontsize=12,pad=10,fontweight='bold')
            elif CTr!=0 and CTr_In==0:plt.title(title+'  CTr='+str(CTr)+'  CTr_In='+str(CTr_In),fontsize=12,pad=10,fontweight='bold')
            elif CTr==0 and CTr_In!=0:plt.title(title+'  CTr='+str(CTr)+'  CTr_In='+str(CTr_In),fontsize=12,pad=10,fontweight='bold')
            elif CTr!=0 and CTr_In!=0:plt.title(title+'  CTr='+str(CTr)+'  CTr_In='+str(CTr_In),fontsize=12,pad=10,fontweight='bold')
            plt.legend(title='k_Ext', fontsize ='medium',bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
        plt.xticks(r_tick,names)
        print(df_day_open['Date'])
        plt.show()
    data_barplot_k_func()
    return df_result