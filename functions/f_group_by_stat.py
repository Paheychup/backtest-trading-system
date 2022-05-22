import pandas as pd
import matplotlib.pyplot as plt
#------------------------------------------------------------------------------
def group_by_stat(df_all_deals,df_day_open,
                       CTr=0, CTr_In=0, column='AVG_deal'):
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
    def data_barplot_func(df_result=df_result,column=column,CTr=CTr,CTr_In=CTr_In):# build the graphic
        y_pos=df_result['Str_id']#names must be tuples
        names=tuple(list(df_result.sort_values(column)['Str_id']))
        plt.figure(figsize=(9, 12))
        plt.barh(y=df_result['Str_id'], width = df_result[column].sort_values(), height=0.75)
        plt.yticks(y_pos,names,rotation=0)
        plt.tick_params(axis='y', labelsize = 8, direction='out',length=3,  colors='black',
                        right=True,labelright=True,)
        plt.xlabel(column, fontweight='bold',labelpad=5); 
        plt.ylabel('Str_id', fontweight='bold',labelpad=5)
        plt.grid(True, color='grey', linestyle='--', linewidth=.3)
        title='Profit summary statistic'
        if CTr==0 and CTr_In==0:plt.title(title,fontsize=12,pad=10,fontweight='bold')
        elif CTr!=0 and CTr_In==0: plt.title(title+'\nCTr='+str(CTr),fontsize=12,pad=10,fontweight='bold')
        elif CTr==0 and CTr_In!=0: plt.title(title+'\nCTr='+str(CTr)+'\nCTr_In='+str(CTr_In),fontsize=12,pad=10,fontweight='bold')
        elif CTr!=0 and CTr_In!=0: plt.title(title+'\nCTr='+str(CTr)+'\nCTr_In='+str(CTr_In),fontsize=12,pad=10,fontweight='bold')
        print(df_day_open['Date'])
        plt.show()
    data_barplot_func()