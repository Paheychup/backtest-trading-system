# start backtest with different parameters:
#-----------------------------------------------------------------------------
for i_Str_id in range(0,len(df_ent_params)):
    print("Str_id: "+str(int(df_ent_params.Str_id[i_Str_id]))+"   "\
        "Per_Tr: "+str(df_ent_params.Per_Tr[i_Str_id])+"   "\
        "k_Ent="+str(df_ent_params.k_Ent[i_Str_id])+"   "\
        "k_Ext="+str(df_ent_params.k_Ext[i_Str_id])+"   "\
        "k_Sl="+str(df_ent_params.k_Sl[i_Str_id])
        )
    #--------------------------------------------------------------------------
    for i_txt in range(0,len(txtfiles)):
        #print(txtfiles[i_txt])
        df=pd.read_csv(txtfiles[i_txt],sep=','
                           ,names=['date','time','last','vol','id','oper'],header=0)
        df=df.iloc[:,:-2]
        
        g=df['last'].ne(df['last'].shift()).cumsum()
        df=df.groupby(['date','time','last',g],
                      as_index=False,sort=False)['vol'].sum()
        df=df.astype({'last':'int64'})
        np_df_day=np.array(df[(df['time']<190000)])
        #------------------------------------------------------------------------------
        a=np.empty((np_df_day.shape[0],np_df_day.shape[1]+7))
        a[:]=np.NAN
        a[:,:-7]=np_df_day
        np_df_day=a
        #------------------------------------------------------------------------------
        np_df_ev=np.array(df[df['time']>=190000])
        del a,g,df
        #------------------------------------------------------------------------------
        #create table for orders - Deals
        np_Deals_table_names=['Status','Date','Ent_time','Ent_Lvl','Ext_time','Ext_Lvl','Sl_Lvl','Tr','Str_id',
                              'CTr_In','CTr','New_Max','New_Min','In_Tr_Max','In_Tr_Min','Tr_Ch_Lvl','TP','SL','Tr_Ch_Max_Lvl','Tr_Ch_Min_Lvl']
        np_Deals_table=np.zeros((100000,len(np_Deals_table_names)),dtype=np.int64)
        #defined a variables for the last row in array LR_Deals
        i_Deals=0
        i_Deals_Count=0
        LR_Deals=0
        #------------------------------------------------------------------------------
        #take enter parameters from np_df_day array and df_ent_params dataframe
        D_O=int(np_df_day[0,2])
        #Per_Tr=0.2
        Per_Tr=df_ent_params.loc[i_Str_id,'Per_Tr']
        #k_Ent=0.08
        k_Ent=df_ent_params.loc[i_Str_id,'k_Ent']
        #k_Ext=0.16
        k_Ext=df_ent_params.loc[i_Str_id,'k_Ext']
        #k_Sl=round(Per_Tr-k_Ent,2)
        k_Sl=df_ent_params.loc[i_Str_id,'k_Sl']
        #create and fill df_day_open dataframe
        try:
            df_day_open
            #print('df_day_open already exists')
        except:
            df_day_open=pd.DataFrame(columns=['Date','D_O'])

        if not int(np_df_day[0,0]) in df_day_open.values:
            values_D_O={'Date':int(np_df_day[0,0]),'D_O':D_O}
            df_day_open=df_day_open.append(values_D_O,ignore_index=True)

        #------------------------------------------------------------------------------
        #defined other parameters
        St_Trade=100100
        CTr_block=0
        CTr_In=0
        CTr=0
        St_Pr=1
        Tr=0 #Trend identification 1-trend up 2-trend down 0-trend indefined
        New_Min=D_O
        New_Max=D_O
        block=0
        
        Tr_Ch_Max_Lvl=int(f_round.round_up(D_O*(1+Per_Tr/100)))
        Tr_Ch_Min_Lvl=int(f_round.round_down(D_O*(1-Per_Tr/100)))
        
        #------------------------------------------------------------------------------
        #Цикл определения тренда в начале торгов
        for i_np_df in range(0,len(np_df_day)):
            
            np_df_day[i_np_df,4]=Tr_Ch_Max_Lvl
            np_df_day[i_np_df,5]=Tr_Ch_Min_Lvl
            np_df_day[i_np_df,6]=New_Max
            np_df_day[i_np_df,7]=New_Min
            
            #print(i_np_df)
            if (np_df_day[i_np_df,2] > New_Max) and (Tr==0):
                New_Max = np_df_day[i_np_df,2]
                Tr_Ch_Min_Lvl = int(f_round.round_down(New_Max * (1 - Per_Tr / 100)))
        
            elif (np_df_day[i_np_df,2] < New_Min) and (Tr==0):
                New_Min = np_df_day[i_np_df,2]
                Tr_Ch_Max_Lvl = int(f_round.round_up(New_Min * (1 + Per_Tr / 100)))
        
            if (np_df_day[i_np_df,2] >= Tr_Ch_Max_Lvl) and (Tr!=1):
                Tr = 1 #trend up
                New_Max = np_df_day[i_np_df,2]
                Tr_Ch_Min_Lvl = int(f_round.round_down(New_Max * (1 - Per_Tr / 100))) #low boader for trande change
                Ent_Lvl = int(round(New_Max*(1-(k_Ent)/100)))
        
                #print(np_df_day[i_np_df,2])
                #print(i_np_df)
                break
            elif (np_df_day[i_np_df,2] <= Tr_Ch_Min_Lvl) and (Tr!=2):
                Tr = 2 #trend down
                New_Min = np_df_day[i_np_df,2]
                Tr_Ch_Max_Lvl = int(f_round.round_up(New_Min * (1 + Per_Tr / 100)))
                Ent_Lvl = int(round(New_Min*(1+(k_Ent)/100)))
        
                #print(np_df_day[i_np_df,2])
                #print(i_np_df)
                break
        #end Цикл определения тренда в начале торгов
        #------------------------------------------------------------------------------
        
        #Block cycle_for_all_data
        for i_np_df in range(i_np_df,len(np_df_day)):
            
            np_df_day[i_np_df,4]=Tr_Ch_Max_Lvl
            np_df_day[i_np_df,5]=Tr_Ch_Min_Lvl
            np_df_day[i_np_df,6]=New_Max
            np_df_day[i_np_df,7]=New_Min
            
            #--------------------------------------------------------------------------
            #working with np_Deals_table for control positions
            #cycle in np_Deals_table
            for i_Deals in range(i_Deals,len(np_Deals_table)):
                #print(i_Deals)
                if np_Deals_table[i_Deals,0]==0:
                    i_Deals=i_Deals_Count
                    break
                
                if np_Deals_table[i_Deals,0]!=3:
                    #if i_Deals_Count-i_Deals==0: 
                    i_Deals_Count+=1;i_Deals=i_Deals_Count
                    
                #if one of conditions is True then
                elif np_Deals_table[i_Deals,0]==3:
                    #i_Deals_Count=i_Deals
                    #**********************************************************
                    if Tr==1 and np_df_day[i_np_df,1]<184400:
                        #print('Tr=1, In_Tr_Max/Min')

                        #In_Tr_Max
                        if np_df_day[i_np_df,2]>np_Deals_table[i_Deals,13]:
                            np_Deals_table[i_Deals,13]=np_df_day[i_np_df,2]
                        #In_Tr_Min
                        elif np_df_day[i_np_df,2]<np_Deals_table[i_Deals,14] and np_Deals_table[i_Deals,10]==CTr:
                            np_Deals_table[i_Deals,14]=np_df_day[i_np_df,2]
 
                        #Move Sl_Lvl
                        if CTr>0 and np_Deals_table[i_Deals,6]!=Tr_Ch_Min_Lvl-1:
                            np_Deals_table[i_Deals,6]=Tr_Ch_Min_Lvl-1
        
                        #Check Ext_Lvl condition
                        if np_df_day[i_np_df,2]>=np_Deals_table[i_Deals,5]:
                            #print('if Tr=1, Status=5, Ext_Time, TP, CTr=CTr-1')
                            block=0
                            #Status=5 TP
                            np_Deals_table[i_Deals,0]=5
                            #Ext_Time
                            np_Deals_table[i_Deals,4]=np_df_day[i_np_df,1]
                            #TP
                            np_Deals_table[i_Deals,16]=np_Deals_table[i_Deals,5]-np_Deals_table[i_Deals,3]
                            #Sl NA
                            #Add Ext_Lvl to graphic
                            np_df_day[i_np_df,9]=np_Deals_table[i_Deals,5]
        
                        #Check Sl_Lvl condition
                        elif np_df_day[i_np_df,2]<=np_Deals_table[i_Deals,6]:
                            #print('if Tr=1, Status=4, Ext_Time, SL, CTr=CTr-1')
                            block=0
                            #Status=4 TP
                            np_Deals_table[i_Deals,0]=4
                            #Ext_Time
                            np_Deals_table[i_Deals,4]=np_df_day[i_np_df,1]
                            #TP NA
                            #Sl NA
                            np_Deals_table[i_Deals,17]=np_Deals_table[i_Deals,6]-np_Deals_table[i_Deals,3]
                            #Add Sl_Lvl to graphic
                            np_df_day[i_np_df,9]=np_Deals_table[i_Deals,6]
                    #**********************************************************        
                    #If time >=184400
                    elif Tr==1 and np_df_day[i_np_df,1]>=184400:    
                        #In_Tr_Max

                        if np_df_day[i_np_df,2]>np_Deals_table[i_Deals,13]:
                            np_Deals_table[i_Deals,13]=np_df_day[i_np_df,2]
                        #In_Tr_Min
                        elif np_df_day[i_np_df,2]<np_Deals_table[i_Deals,14] and np_Deals_table[i_Deals,10]==CTr:
                            np_Deals_table[i_Deals,14]=np_df_day[i_np_df,2]

                        #Move Sl_Lvl
                        if CTr>0 and np_Deals_table[i_Deals,6]!=Tr_Ch_Min_Lvl-1:
                            np_Deals_table[i_Deals,6]=Tr_Ch_Min_Lvl-1 
                        #Check Ext_Lvl condition
                        if np_df_day[i_np_df,2]>np_Deals_table[i_Deals,3]:
                            #print('if Tr=1, Status=5, Ext_Time, TP, CTr=CTr-1')
                            block=0
                            #Status=5 TP
                            np_Deals_table[i_Deals,0]=5
                            #Ext_Time
                            np_Deals_table[i_Deals,4]=np_df_day[i_np_df,1]
                            #Update Ext_Lvl
                            np_Deals_table[i_Deals,5]=np_df_day[i_np_df,2]
                            #TP
                            np_Deals_table[i_Deals,16]=np_df_day[i_np_df,2]-np_Deals_table[i_Deals,3]
                            #Sl NA
                            #Add Ext_Lvl to graphic
                            np_df_day[i_np_df,9]=np_df_day[i_np_df,2]
                        #Check Sl_Lvl condition
                        elif np_df_day[i_np_df,2]<=np_Deals_table[i_Deals,3]:
                            #print('if Tr=1, Status=4, Ext_Time, SL, CTr=CTr-1')
                            block=0
                            #Status=4 TP
                            np_Deals_table[i_Deals,0]=4
                            #Ext_Time
                            np_Deals_table[i_Deals,4]=np_df_day[i_np_df,1]
                            #Update Ext_Lvl
                            np_Deals_table[i_Deals,5]=np_df_day[i_np_df,2]
                            #TP NA
                            #Sl NA
                            np_Deals_table[i_Deals,17]=np_df_day[i_np_df,2]-np_Deals_table[i_Deals,3]
                            #Add Sl_Lvl to graphic
                            np_df_day[i_np_df,9]=np_df_day[i_np_df,2] 

                    #******************************************************************  
                    elif Tr==2 and np_df_day[i_np_df,1]<184400:
                        #print('if Tr=2, In_Tr_Max/Min')

                        #In_Tr_Max
                        if np_df_day[i_np_df,2]>np_Deals_table[i_Deals,13] and np_Deals_table[i_Deals,10]==CTr:
                            np_Deals_table[i_Deals,13]=np_df_day[i_np_df,2]
                        #In_Tr_Min
                        elif np_df_day[i_np_df,2]<np_Deals_table[i_Deals,14]:
                            np_Deals_table[i_Deals,14]=np_df_day[i_np_df,2]

                        #Move Sl_Lvl
                        if CTr>0 and np_Deals_table[i_Deals,6]!=Tr_Ch_Max_Lvl+1:
                            np_Deals_table[i_Deals,6]=Tr_Ch_Max_Lvl+1
                        
                        #Check Ext_Lvl condition
                        if np_df_day[i_np_df,2]<=np_Deals_table[i_Deals,5]:
                            #print('Tr=2, Status=5, Ext_Time, TP, CTr=CTr-1')
                            block=0
                            #Status=5 TP
                            np_Deals_table[i_Deals,0]=5
                            #Ext_Time
                            np_Deals_table[i_Deals,4]=np_df_day[i_np_df,1]
                            #TP
                            np_Deals_table[i_Deals,16]=abs(np_Deals_table[i_Deals,5]-np_Deals_table[i_Deals,3])
                            #Sl NA
                            #Add Ext_Lvl to graphic
                            np_df_day[i_np_df,9]=np_Deals_table[i_Deals,5]
                        #Check Sl_Lvl condition
                        elif np_df_day[i_np_df,2]>=np_Deals_table[i_Deals,6]:
                            #print('if Tr=2, Status=4, Ext_Time, SL, CTr=CTr-1')
                            block=0
                            #Status=4 TP
                            np_Deals_table[i_Deals,0]=4
                            #Ext_Time
                            np_Deals_table[i_Deals,4]=np_df_day[i_np_df,1]
                            #TP NA
                            #Sl NA
                            np_Deals_table[i_Deals,17]=(np_Deals_table[i_Deals,6]-np_Deals_table[i_Deals,3])*-1
                            #Add Sl_Lvl to graphic
                            np_df_day[i_np_df,9]=np_Deals_table[i_Deals,6]
                    #**********************************************************     
                    #If Tr==2 and time >=184400
                    elif Tr==2 and np_df_day[i_np_df,1]>=184400:

                        #In_Tr_Max
                        if np_df_day[i_np_df,2]>np_Deals_table[i_Deals,13] and np_Deals_table[i_Deals,10]==CTr:
                            np_Deals_table[i_Deals,13]=np_df_day[i_np_df,2]
                        #In_Tr_Min
                        elif np_df_day[i_np_df,2]<np_Deals_table[i_Deals,14]:
                            np_Deals_table[i_Deals,14]=np_df_day[i_np_df,2]
                            
                        #Move Sl_Lvl
                        if CTr>0 and np_Deals_table[i_Deals,6]!=Tr_Ch_Max_Lvl+1:
                            np_Deals_table[i_Deals,6]=Tr_Ch_Max_Lvl+1
                            
                        #Check Ext_Lvl condition
                        if np_df_day[i_np_df,2]<np_Deals_table[i_Deals,3]:
                            #print('Tr=2, Status=5, Ext_Time, TP, CTr=CTr-1')
                            block=0
                            #Status=5 TP
                            np_Deals_table[i_Deals,0]=5
                            #Ext_Time
                            np_Deals_table[i_Deals,4]=np_df_day[i_np_df,1]
                            #Update Ext_Lvl
                            np_Deals_table[i_Deals,5]=np_df_day[i_np_df,2]
                            #TP
                            np_Deals_table[i_Deals,16]=np_Deals_table[i_Deals,3]-np_df_day[i_np_df,2]
                            #Sl NA
                            #Add Ext_Lvl to graphic
                            np_df_day[i_np_df,9]=np_df_day[i_np_df,2]
                        #Check Sl_Lvl condition
                        elif np_df_day[i_np_df,2]>=np_Deals_table[i_Deals,3]:
                            #print('if Tr=2, Status=4, Ext_Time, SL, CTr=CTr-1')
                            block=0
                            #Status=4 TP
                            np_Deals_table[i_Deals,0]=4
                            #Ext_Time
                            np_Deals_table[i_Deals,4]=np_df_day[i_np_df,1]
                            #Update Ext_Lvl
                            np_Deals_table[i_Deals,5]=np_df_day[i_np_df,2]
                            #TP NA
                            #Sl NA
                            np_Deals_table[i_Deals,17]=np_Deals_table[i_Deals,3]-np_df_day[i_np_df,2]
                            #Add Sl_Lvl to graphic
                            np_df_day[i_np_df,9]=np_df_day[i_np_df,2]
                    #**********************************************************     
                #if nothing has changed in Deals table then number of row + 1
                #i_Deals=i_Deals_Count
            #------------------------------------------------------------------
            #END cycle in np_Deals_table  
            #------------------------------------------------------------------
            if np_df_day[i_np_df,2] > New_Max:
                New_Max=np_df_day[i_np_df,2] #'Определяем новый максимум цены
                Tr_Ch_Min_Lvl = int(f_round.round_down(New_Max * (1 - Per_Tr / 100))) # 'Обновляем уровень смены тренда
                Ent_Lvl = int(round(New_Max * (1 - k_Ent / 100), 0)) #обновляем уровень входа в позицию (цены заявки)
                block = 0
                CTr_In=0
                CTr_block=0
            elif np_df_day[i_np_df,2] < New_Min:
                New_Min=np_df_day[i_np_df,2] #'Определяем новый минимум цены
                Tr_Ch_Max_Lvl = int(f_round.round_up(New_Min * (1 + Per_Tr / 100))) # 'Обновляем уровень смены тренда
                Ent_Lvl=int(round(New_Min * (1 + k_Ent / 100), 0))
                block = 0 #'Снимаем блок
                CTr_In=0
                CTr_block=0   
            #Если пробит уровень максимума Tr_Ch_Max_Lvl и тренд нисходящий, то определяем тренд как восходящий
            if np_df_day[i_np_df,2]>Tr_Ch_Max_Lvl and Tr==2:
                Tr=1 #'Тренд восходящий
                CTr_In=0
                CTr=0
                CTr_block=0
                New_Max=np_df_day[i_np_df,2] #'Определяем новый максимум цены
                Tr_Ch_Min_Lvl = int(f_round.round_down(New_Max * (1 - Per_Tr / 100))) #'Обновляем уровень смены тренда
                Tr_Ch_Lvl=Tr_Ch_Min_Lvl #Записывем для расчета, на каком расстоянии от смены тренда был вход в позицию
                Ent_Lvl = int(round(New_Max * (1 - k_Ent / 100), 0))
                #Тренд изменился
            #Если пробит уровень минимума Tr_Ch_Min_Lvl и тренд восходящий, то определяем тренд как нисходящий
            elif np_df_day[i_np_df,2]<Tr_Ch_Min_Lvl and Tr==1:
                Tr=2 #'Тренд нисходящий
                CTr_In=0
                CTr=0
                CTr_block=0
                New_Min=np_df_day[i_np_df,2] #'Определяем новый минимум цены
                Tr_Ch_Max_Lvl = int(round(New_Min * (1 + Per_Tr / 100), 0)) #'Обновляем уровень смены тренда
                Tr_Ch_Lvl=Tr_Ch_Max_Lvl #Записывем для расчета, на каком расстоянии от смены тренда был вход в позицию
                Ent_Lvl = int(round(New_Min * (1 + k_Ent / 100), 0))
                #Тренд изменился
            
            if Tr==1 and np_df_day[i_np_df,2]<=Ent_Lvl and block!=1 and np_df_day[i_np_df,1]<184400 and np_df_day[i_np_df,1]>St_Trade:
                #print('Tr=1')
                #print(np_df_day[i_np_df,2])
                block=1
                #insert values to np_Deals_table
                #Status=3 - order has executed
                np_Deals_table[LR_Deals,0]=3
                #Date
                np_Deals_table[LR_Deals,1]=np_df_day[i_np_df,0]
                #Ent_time
                np_Deals_table[LR_Deals,2]=np_df_day[i_np_df,1]
                #Ent_Lvl
                #np_Deals_table[i_Deals,3]=np_df_day[i_np_df,2]
                np_Deals_table[LR_Deals,3]=Ent_Lvl
                np_df_day[i_np_df,8]=Ent_Lvl
                #Ext_time
                #Ext_Lvl defined
                if k_Ent==k_Ext:Ext_Lvl=New_Max
                else:Ext_Lvl=int(round(Ent_Lvl*(1+k_Ext/100),0))
                np_Deals_table[LR_Deals,5]=Ext_Lvl
                np_df_day[i_np_df,9]=Ext_Lvl
                #Sl_Lvl defined
                Sl_Lvl = Tr_Ch_Min_Lvl - St_Pr
                np_Deals_table[LR_Deals,6]=Sl_Lvl
                np_df_day[i_np_df,10]=Sl_Lvl
                #Tr
                np_Deals_table[LR_Deals,7]=Tr
                #Str_id
                np_Deals_table[LR_Deals,8]=df_ent_params.loc[i_Str_id,'Str_id']
                #CTr_In
                CTr_In+=1
                np_Deals_table[LR_Deals,9]=CTr_In
                #CTr
                if CTr_block==0: CTr+=1; CTr_block=1
                np_Deals_table[LR_Deals,10]=CTr
                #New_Max
                np_Deals_table[LR_Deals,11]=New_Max
                #New_Min
                np_Deals_table[LR_Deals,12]=New_Min
                #In_Tr_Max
                np_Deals_table[LR_Deals,13]=Ent_Lvl
                #In_Tr_Min
                np_Deals_table[LR_Deals,14]=Ent_Lvl
                
                #Tr_Ch_Lvl
                np_Deals_table[LR_Deals,15]=abs(Tr_Ch_Max_Lvl-New_Max)
                #TP
                #SL
                #Tr_Ch_Max_Lvl
                np_Deals_table[LR_Deals,18]=Tr_Ch_Max_Lvl
                #Tr_Ch_Max_Lvl
                np_Deals_table[LR_Deals,19]=Tr_Ch_Min_Lvl

                LR_Deals+=1 #for cycle in np_Deals_table
                
            elif Tr==2 and np_df_day[i_np_df,2]>=Ent_Lvl and block!=1 and np_df_day[i_np_df,1]<184400 and np_df_day[i_np_df,1]>St_Trade:
                #print('Tr=2')
                #print(np_df_day[i_np_df,2])
                block=1
                #insert values to np_Deals_table
                #Status=3 - order has executed
                np_Deals_table[LR_Deals,0]=3
                #Date
                np_Deals_table[LR_Deals,1]=np_df_day[i_np_df,0]
                #Ent_time
                np_Deals_table[LR_Deals,2]=np_df_day[i_np_df,1]
                #Ent_Lvl
                #np_Deals_table[i_Deals,3]=np_df_day[i_np_df,2]
                np_Deals_table[LR_Deals,3]=Ent_Lvl
                np_df_day[i_np_df,8]=Ent_Lvl
                #Ext_time
                #Ext_Lvl defined
                if k_Ent==k_Ext:Ext_Lvl=New_Min
                else:Ext_Lvl=int(round(Ent_Lvl*(1-k_Ext/100),0))
                np_Deals_table[LR_Deals,5]=Ext_Lvl
                np_df_day[i_np_df,9]=Ext_Lvl
                #Sl_Lvl defined
                Sl_Lvl = Tr_Ch_Max_Lvl + St_Pr
                np_Deals_table[LR_Deals,6]=Sl_Lvl
                np_df_day[i_np_df,10]=Sl_Lvl
                #Tr
                np_Deals_table[LR_Deals,7]=Tr
                #Str_id
                np_Deals_table[LR_Deals,8]=df_ent_params.loc[i_Str_id,'Str_id']
                #CTr_In
                CTr_In+=1 
                np_Deals_table[LR_Deals,9]=CTr_In
                #CTr
                if CTr_block==0:CTr+=1; CTr_block=1
                np_Deals_table[LR_Deals,10]=CTr
                #New_Max
                np_Deals_table[LR_Deals,11]=New_Max
                #New_Min
                np_Deals_table[LR_Deals,12]=New_Min
                #In_Tr_Max
                np_Deals_table[LR_Deals,13]=Ent_Lvl
                #In_Tr_Min
                np_Deals_table[LR_Deals,14]=Ent_Lvl
                #Tr_Ch_Lvl
                np_Deals_table[LR_Deals,15]=Tr_Ch_Min_Lvl-New_Min
                #TP
                #SL
                #Tr_Ch_Max_Lvl
                np_Deals_table[LR_Deals,18]=Tr_Ch_Max_Lvl
                #Tr_Ch_Max_Lvl
                np_Deals_table[LR_Deals,19]=Tr_Ch_Min_Lvl   
  
                LR_Deals+=1 #for cycle in np_Deals_table
        #----------------------------------------------------------------------       
        #drop 0 from np_Deals_table
        np_Deals_table=np_Deals_table[np_Deals_table[:,0]!=0] 
        #create dataframe table form np_Deals_table
        df_Deals_table=pd.DataFrame(np_Deals_table,columns=np_Deals_table_names)
        #join np_Deals_table with params by index 0
        #result=pd.merge(df_Deals_table, df_ent_params, how='inner',on='Str_id')
      
        #create dictionary for deals
        try:
            dict_day_deals
        except:
            dict_day_deals={} 
        #str_dict_day_deals=str(int(np_df_day[0,0]))+'_'+str(int(df_ent_params.loc[i_Str_id,'Str_id'])) #create string name of dictionary with date
        str_dict_day_deals=str(int(np_df_day[0,0]))
        dict_day_deals[str_dict_day_deals]=df_Deals_table #add table in dict_day with name=str_dict_day
        
        #create dictionary for data
        try:
            dict_day_data
        except:
            dict_day_data={} 
        str_dict_day_np_df_day=str(int(np_df_day[0,0]))
        dict_day_data[str_dict_day_np_df_day]=np_df_day
        #----------------------------------------------------------------------
        #END for i_txt in range(0,len(txtfiles)):

    #create dictionary for strategies
    try:
        dict_str_deals
    except:
        dict_str_deals={}
    #create string name of dictionary with strategie name
    str_dict_strategie_deals=int(df_ent_params.loc[i_Str_id,'Str_id'])
    dict_str_deals[str_dict_strategie_deals]=dict_day_deals #add dict_day dictionary to dict_str dictionary with name=str_dict_strategie
    
    del dict_day_deals
    
    #create dictionary for strategies
    try:
        dict_str_data
    except:
        dict_str_data={}
    #create string name of dictionary with strategie name
    str_dict_strategie_data=int(df_ent_params.loc[i_Str_id,'Str_id'])
    #str_dict_strategie=str(int(df_ent_params.loc[0,'Str_id']))
    dict_str_data[str_dict_strategie_data]=dict_day_data
    
    del dict_day_data
#------------------------------------------------------------------------------
# end backtest with different parameters

# delete temp variables
del CTr,CTr_In,CTr_block,Ent_Lvl,Ext_Lvl,LR_Deals,New_Max,New_Min,Per_Tr,Sl_Lvl,St_Pr,Tr,Tr_Ch_Lvl,Tr_Ch_Max_Lvl,Tr_Ch_Min_Lvl
del block,df_Deals_table,file,i_Deals,i_Deals_Count,i_Str_id,i_np_df,i_txt,k_Ent,k_Ext,k_Sl,np_Deals_table,np_df_day,np_df_ev
del str_dict_day_deals,str_dict_day_np_df_day,str_dict_strategie_data,str_dict_strategie_deals,txtfiles,values_D_O

# create table with all deals
#------------------------------------------------------------------------------
df_all_deals=f_all_deals.df_all_deals(dict_str_deals=dict_str_deals
                                   ,df_ent_params=df_ent_params)

# create dictionary with all stratagies and deals
#------------------------------------------------------------------------------
dict_str_all_deals=f_dict_str_all_deals.dict_str_all_deals(dict_str_deals=dict_str_deals)

# create dataframe with summary statistic stat1
#------------------------------------------------------------------------------
df_stat1=f_stat1.stat1(dict_str_all_deals=dict_str_all_deals)
df_stat1=pd.merge(df_stat1, df_ent_params, how='inner',on='Str_id')