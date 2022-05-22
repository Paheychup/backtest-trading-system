import pandas as pd
#------------------------------------------------------------------------------
def stat1(dict_str_all_deals):
    #create df names for df_stat1
    df_stat=pd.DataFrame(columns=['Str_id','Count','Count_plus','Count_minus',
                                   'Per_Count_plus','Per_Count_minus',
                                   'TP_vs_SL','Total','AVG_deal','Eff',
                                       'Max_TP','Max_SL',
                                       'DrDown','Eff2','DrDown2'])
    for key in dict_str_all_deals:
        df=dict_str_all_deals[key].copy()
        #df=dict_str_all_deals[15]
        Str_id=df.loc[0,'Str_id'] #Str_id
        df['Total']=df['TP']+df['SL']
        df['Cumsum']=df['Total'].cumsum()
        df['HighVal']=df['Cumsum'].cummax()
        df['DrDown']=df['Cumsum']-df['HighVal']
        df['LowVal']=df['Cumsum'].cummin()
        df['DrDown2']=df['Cumsum']-df['LowVal']
        DrDown=df['DrDown'].min()
        DrDown2=df['DrDown2'].max()
        #Max_TP
        df.loc[df['Total']<=0,'Sequence']=False
        df.loc[df['Total']>0,'Sequence']=True
        s=df['Sequence']
        Max_TP=(~s).cumsum()[s].value_counts().max()
        #Max_SL
        df.loc[df['Total']<=0,'Sequence']=True
        df.loc[df['Total']>0,'Sequence']=False
        s=df['Sequence']
        Max_SL=(~s).cumsum()[s].value_counts().max()
        Count=df.shape[0] #Count
        Count_plus=df[df['TP']>0].count()['TP']
        Count_minus=df[(df['SL']<=0) & (df['TP']==0)].count()['SL']
        Per_Count_plus=round(df[df['TP']>0].count()['TP']/df.shape[0],3)
        Per_Count_minus=round(df[(df['SL']<=0) & (df['TP']==0)].count()['SL']/df.shape[0],3)
        TP_vs_SL=round((df[df['TP']>0].count()['TP']/df.shape[0])/(df[(df['SL']<=0) & (df['TP']==0)].count()['SL']/df.shape[0]),3)
        Total=df['TP'].sum()+df['SL'].sum()
        AVG_deal=round((df['TP'].sum()+df['SL'].sum())/df.shape[0],2)
        Eff=round(abs(Total/DrDown),3)
        Eff2=round(abs(Total/DrDown2),3)
        values_df_stat={'Str_id':Str_id,'Count':Count,'Count_plus':Count_plus,'Count_minus':Count_minus,
                             'Per_Count_plus':Per_Count_plus,'Per_Count_minus':Per_Count_minus,
                             'TP_vs_SL':TP_vs_SL,'Total':Total,'AVG_deal':AVG_deal,'Eff':Eff,
                             'Max_TP':Max_TP,'Max_SL':Max_SL,
                             'DrDown':DrDown,'Eff2':Eff2,'DrDown2':DrDown2}
        df_stat=df_stat.append(values_df_stat,ignore_index=True)
    return df_stat