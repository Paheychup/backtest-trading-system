#------------------------------------------------------------------------------
def dict_str_all_deals(dict_str_deals):
    dict_str_all_deals={}
    for key in dict_str_deals:
        for key2 in dict_str_deals[key]:
            try:
                df_deals_all_days=df_deals_all_days.append(dict_str_deals[key][key2],ignore_index=True)
            except:
                df_deals_all_days=dict_str_deals[key][key2].copy()
        dict_str_all_deals[key]=df_deals_all_days.reset_index(drop=True)
        del df_deals_all_days
    return dict_str_all_deals
#------------------------------------------------------------------------------