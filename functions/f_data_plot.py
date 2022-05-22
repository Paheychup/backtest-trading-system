import numpy as np
import matplotlib.pyplot as plt
#------------------------------------------------------------------------------   
def data_plot(Str_id, Date 
              ,df_ent_params
              ,dict_str_data, dict_str_deals
              ,deal_indx=0, count_deals=1):
    
    np_df_day=dict_str_data[Str_id][Date].copy()
    df_deals=dict_str_deals[Str_id][Date].copy()
    df_deals=df_deals[df_deals.loc[:,'Date']==int(Date)] #filter df_deals by date

    df_ent_params_indx=df_ent_params.index[df_ent_params['Str_id']==Str_id].tolist()[0]
    df_deals['Hour']=df_deals.Ent_time.apply(str)
    df_deals['Hour']=df_deals['Hour'].str[0:2]
    #--------------------------------------------------------------------------
    if count_deals>len(df_deals): count_deals=len(df_deals)
    if deal_indx>=len(df_deals):deal_indx=len(df_deals)-1
    if count_deals==0: count_deals=1
    if deal_indx>0: 
        if count_deals>len(df_deals)-deal_indx:count_deals=len(df_deals)-deal_indx
    #if deal_indx>=len(df_deals): deal_indx=len(df_deals)-1
    #if count_deals<deal_indx: count_deals=deal_indx+1
    start_time_value=df_deals.loc[deal_indx,'Ent_time']
    #stop_time_value=df_deals.loc[count_deals-1,'Ext_time']
    stop_time_value=df_deals.loc[count_deals-1+deal_indx,'Ext_time']
    time_start_indx=min(np.where(np_df_day[:,1]==start_time_value)[0])
    time_stop_indx=max(np.where(np_df_day[:,1]==stop_time_value)[0])
    #print(df_deals.loc[deal_indx:count_deals-1,['Ent_time','Ext_time','Ent_Lvl','Ext_Lvl','Sl_Lvl','TP','SL','CTr','CTr_In']])
    #count=str(len(df_deals.loc[deal_indx:count_deals-1,:]))
    print(df_deals.loc[deal_indx:count_deals-1+deal_indx,['Ent_time','Ext_time','Ent_Lvl','Ext_Lvl','Sl_Lvl','TP','SL','CTr','CTr_In','Tr']])
    count=str(len(df_deals.loc[deal_indx:count_deals-1+deal_indx,:]))

    #--------------------------------------------------------------------------
    plt.figure(figsize=(15, 8))
    plt.plot(np_df_day[time_start_indx:time_stop_indx,[2]],lw=.6)
    plt.plot(np_df_day[time_start_indx:time_stop_indx,[4,5]],lw=.5)
    plt.plot(np_df_day[time_start_indx:time_stop_indx,[6,7]],ls='--',lw=.5)
    plt.scatter(x=np.arange(0,time_stop_indx-time_start_indx),y=np_df_day[time_start_indx:time_stop_indx,8],c='black',lw=3,marker='_')
    plt.scatter(x=np.arange(0,time_stop_indx-time_start_indx),y=np_df_day[time_start_indx:time_stop_indx,9],c='r',lw=3,marker='_')
    plt.scatter(x=np.arange(0,time_stop_indx-time_start_indx),y=np_df_day[time_start_indx:time_stop_indx,10],c='m',lw=3,marker='_')
    plt.title('Str_id='+str(df_deals.Str_id[0])+'  '+'Date='+str(df_deals.Date[0])+'  '+
              'Count_All='+str(df_deals.shape[0])+
              '\nPer_Tr='+str(df_ent_params.Per_Tr[df_ent_params_indx])+'  '+
              'k_Ent='+str(round(df_ent_params.k_Ent[df_ent_params_indx],2))+'  '
              +'k_Ext='+str(df_ent_params.k_Ext[df_ent_params_indx])+'  '+'Time: '+str(start_time_value)+':'+str(stop_time_value)+
              '  Count='+count
              ,loc='left',fontsize=10,fontweight='bold')
    plt.show()
    return np_df_day,df_deals