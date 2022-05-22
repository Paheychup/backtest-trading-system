import pandas as pd
# 1 group by all Str_id
#------------------------------------------------------------------------------
def df_all_deals(dict_str_deals,df_ent_params):
    for key in dict_str_deals:
        for key2 in dict_str_deals[key]:
            df=dict_str_deals[key][key2].copy()
            df['Total']=df['SL']+df['TP']
            df['Hour']=df.Ent_time.apply(str)
            df['Hour']=df['Hour'].str[0:2].astype('category')
            df['Cumsum']=df['Total'].cumsum()
            df['HighVal']=df['Cumsum'].cummax()
            df['DrDown']=df['Cumsum']-df['HighVal']
            df['LowVal']=df['Cumsum'].cummin()
            df['DrDown2']=df['Cumsum']-df['LowVal']
            df=pd.merge(df, df_ent_params, how='inner',on='Str_id')
            try:
                df_all_deals=df_all_deals.append(df,ignore_index=True)
            except:
                df_all_deals=df.copy()
    return df_all_deals          
#------------------------------------------------------------------------------ 