import pandas as pd
#create dataframe with enter parameters
#------------------------------------------------------------------------------
def df_ent_params_func_All(k_Ent_Step,
                           k_Ent_min,k_Ent_max,
                           k_Ext_Step,
                           k_Ext_min, k_Ext_max, 
                           Per_Tr):
    df_ent_params=pd.DataFrame(columns=['Str_id','Per_Tr','k_Ent','k_Ext','k_Sl'])
    count_ent=int(round(((k_Ent_max-k_Ent_min)+k_Ent_Step)/k_Ent_Step))
    count_ext=int(round(((k_Ext_max-k_Ext_min)+k_Ext_Step)/k_Ext_Step))
    Str_id=0
    for j_str in range(0,count_ent):
        #k_Ent_min=k_Ent_Step*j_str
        k_Ext=k_Ext_min
        for i_str in range(0,count_ext):
            Str_id=Str_id+1
            k_Sl=round(Per_Tr-k_Ent_min,2)
            values_ent_params={'Str_id':int(Str_id),'Per_Tr':Per_Tr,'k_Ent':round(k_Ent_min,2),'k_Ext':round(k_Ext,2),'k_Sl':k_Sl}
            df_ent_params=df_ent_params.append(values_ent_params,ignore_index=True)
            k_Ext=k_Ext+k_Ext_Step
        i_str=0
        count_ext=count_ext+1
        k_Ent_min=k_Ent_min+k_Ent_Step
    return df_ent_params
#------------------------------------------------------------------------------