import pandas as pd
import numpy as np
#------------------------------------------------------------------------------
def stat2(dict_str_all_deals, df_ent_params):
    np_time=np.arange(10,19).astype(str) #create range with time
    df_stat=pd.DataFrame(columns=['Str_id','Hour','Count','Count_plus','Count_minus',
                                       'Per_Count_plus','Per_Count_minus',
                                       'TP_vs_SL','Total','AVG_deal','Eff',
                                       'Max_TP','Max_SL',
                                       'DrDown','Eff2','DrDown2'])
    for key in dict_str_all_deals:
        df=dict_str_all_deals[key].copy()
        #df=dict_str_all_deals[0].copy() 
        df['Hour']=df.Ent_time.apply(str)
        df['Hour']=df['Hour'].str[0:2]
        Str_id=int(df.loc[0,'Str_id']) #Str_id
        for time in np_time:
            #time=np_time[2]
            df_t=df[df['Hour']==str(time)].reset_index(drop=True)
            try:
                df_t.iloc[0,0]
            except:
                print('df_t has no data !!! next iteration')
            else:  
                df_t['Total']=df_t['TP']+df_t['SL']
                df_t['Cumsum']=df_t['Total'].cumsum()
                df_t['HighVal']=df_t['Cumsum'].cummax()
                df_t['DrDown']=df_t['Cumsum']-df_t['HighVal']
                df_t['LowVal']=df_t['Cumsum'].cummin()
                df_t['DrDown2']=df_t['Cumsum']-df_t['LowVal']
                DrDown=df_t['DrDown'].min()
                DrDown2=df_t['DrDown2'].max()
                #Max_TP
                df_t.loc[df_t['Total']<=0,'Sequence']=False
                df_t.loc[df_t['Total']>0,'Sequence']=True
                s=df_t['Sequence']
                Max_TP=(~s).cumsum()[s].value_counts().max()
                #Max_SL
                df_t.loc[df_t['Total']>0,'Sequence']=False
                df_t.loc[df_t['Total']<=0,'Sequence']=True
                s=df_t['Sequence']
                Max_SL=(~s).cumsum()[s].value_counts().max()
                Hour=df_t.loc[0,'Hour']
                Count=df_t.shape[0] #Count
                Count_plus=df_t[df_t['TP']>0].count()['TP']
                Count_minus=df_t[(df_t['SL']<=0) & (df_t['TP']==0)].count()['SL']
                Per_Count_plus=round(df_t[df_t['TP']>0].count()['TP']/df_t.shape[0],3)
                Per_Count_minus=round(df_t[(df_t['SL']<=0) & (df_t['TP']==0)].count()['SL']/df_t.shape[0],3)
                k_Ext=df_ent_params['k_Ext'][df_ent_params['Str_id']==Str_id].values[0]
                k_Sl=df_ent_params['k_Sl'][df_ent_params['Str_id']==Str_id].values[0]
                TP_vs_SL=round(k_Ext/k_Sl,2)
                Total=df_t['TP'].sum()+df_t['SL'].sum()
                AVG_deal=round((df_t['TP'].sum()+df_t['SL'].sum())/df_t.shape[0],1)
                Eff=round(abs(Total/DrDown),2)
                Eff2=round(abs(Total/DrDown2),2)
                values_df_stat={'Str_id':Str_id,'Hour':Hour,'Count':Count,'Count_plus':Count_plus,'Count_minus':Count_minus,
                                 'Per_Count_plus':Per_Count_plus,'Per_Count_minus':Per_Count_minus,
                                 'TP_vs_SL':TP_vs_SL,'Total':Total,'AVG_deal':AVG_deal,'Eff':Eff,
                                 'Max_TP':Max_TP,'Max_SL':Max_SL,
                                 'DrDown':DrDown,'Eff2':Eff2,'DrDown2':DrDown2}
                df_stat=df_stat.append(values_df_stat,ignore_index=True)
            del df_t
    return df_stat