
"""
Created on Sat Dec 30 10:51:22 2017

@author: Sarbadal.Pal
"""
import pandas as pd
import numpy as np
from abanalysis import Color
from abanalysis import check_def
from abanalysis import add_years
from abanalysis import trend_def
from abanalysis import control_def
from abanalysis import BOS_control_def
from abanalysis import test_def
from abanalysis import KDTree_def
from abanalysis import BOS_KDTree_def
from abanalysis import prep_measure_def
import datetime as dt

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def ab_analysis(no_of_control = 10,                                                                                                                                                                                                #
                var2pickneighbors = ['Seasonality','Trend'],                                                                                                                                                                       #
                with_replacement = 'T',                                                                                                                                                                                            #
                Lift_Threshold = 2,                                                                                                                                                                                                #
                Identifier = 'Store', Date_Col = 'Date', Measure = 'Sales', Cluster = 'Cluster', Changed = 'Changed', Test = 'Test',                                                                                               #
                trend_data=None, measure_data=None, cluster_date=None):                                                                                                                                                            #
                                                                                                                                                                                                                                   #
  final_tf, final_msg = check_def.cond_check_def(no_of_control = no_of_control,                                                                                                                                                    #
                                                var2pickneighbors = var2pickneighbors,                                                                                                                                             #
                                                with_replacement = with_replacement,                                                                                                                                               #
                                                Lift_Threshold = Lift_Threshold,                                                                                                                                                   #
                                                Identifier = Identifier, Date_Col = Date_Col, Measure = Measure, Cluster = Cluster, Changed = Changed, Test = Test,                                                                #
                                                trend_data=trend_data, measure_data=measure_data, cluster_date=cluster_date)                                                                                                       #
                                                                                                                                                                                                                                   #
  if final_tf:                                                                                                                                                                                                                     #
                                                                                                                                                                                                                                   #
    if (with_replacement==True): with_replacement = 'T'                                                                                                                                                                            #
    if (with_replacement==False): with_replacement = 'F'                                                                                                                                                                           #
    trend_df = trend_def.trend_def(data=trend_data, Identifier = Identifier, Cluster = Cluster, Changed = Changed, Test = Test)                                                                                                    #
    #Create a list of all cluster and sort it. We are also making sure 'All' cluster comes at the end.                                                                                                                             #
    cluster_list = trend_df['Cluster'].unique().tolist()                                                                                                                                                                           #
    cluster_list.remove('All')                                                                                                                                                                                                     #
    cluster_list.sort()                                                                                                                                                                                                            #
    cluster_list.append('All')                                                                                                                                                                                                     #
                                                                                                                                                                                                                                   #
    Method_Cluster = []                                                                                                                                                                                                            #
    PorYoY_C = []                                                                                                                                                                                                                  #
    Method_C = []                                                                                                                                                                                                                  #
    Cluster_C = []                                                                                                                                                                                                                 #
    Significance_Level = []                                                                                                                                                                                                        #
    Significance_Word = []                                                                                                                                                                                                         #
    AVG_Lift = []                                                                                                                                                                                                                  #
    Expected_Impact = []                                                                                                                                                                                                           #
    P_Value = []                                                                                                                                                                                                                   #
    Count = []                                                                                                                                                                                                                     #
    Sum_Above_Zero = []                                                                                                                                                                                                            #
    Sum_Above_Thres = []                                                                                                                                                                                                           #
    Threshold = []                                                                                                                                                                                                                 #
    AVG_Treatment = []                                                                                                                                                                                                             #
    AVG_Control = []                                                                                                                                                                                                               #
    PCT_Above_Thres = []                                                                                                                                                                                                           #
    PCT_Above_Zero = []                                                                                                                                                                                                            #
    AVG_Diff = []                                                                                                                                                                                                                  #
    BOS_Matched = []                                                                                                                                                                                                               #
    control_map = []                                                                                                                                                                                                               #
    Tmt = []                                                                                                                                                                                                                       #
    Ctrl = []      

    timeseries_df, summary_df = pd.DataFrame(), pd.DataFrame()                                                                                                                                                                     #
                                                                                                                                                                                                                                   #
    for BOSorMatch in ['Matched', 'BoS']:                                                                                                                                                                                          #
      for PriodOrYoY in ['Prior','YoY']:                                                                                                                                                                                           #
        for m in ['Original', 'Reassigned']:                                                                                                                                                                                       #
          for c in cluster_list:                                                                                                                                                                                                   #
                                                                                                                                                                                                                                   #
            control_df, vcn = control_def.control_def(data=trend_df, method=m, cluster=c, var2pickneighbors = var2pickneighbors)                                                                                                   #
            test_store_df = test_def.test_def(data=control_df)                                                                                                                                                                     #
                                                                                                                                                                                                                                   #
            if BOSorMatch == 'Matched':                                                                                                                                                                                            #
              control_df, vcn = control_df, vcn                                                                                                                                                                                    #
            else:                                                                                                                                                                                                                  #
              control_df, vcn = BOS_control_def.bos_control_def(data=trend_df, method=m, cluster=c, var2pickneighbors = var2pickneighbors)                                                                                         #
              control_df = pd.concat([control_df, test_store_df])                                                                                                                                                                  #
                                                                                                                                                                                                                                   #
            df = pd.merge(control_df, test_store_df[['Identifier']].rename(columns={'Identifier':'Control_Identifier'}, inplace=False),                                                                                            #
                          how='left', left_on='Identifier', right_on='Control_Identifier', left_index=False, right_index=False, sort=True)                                                                                         #
                                                                                                                                                                                                                                   #
            df.loc[df['Control_Identifier'].notnull(), 'Test/Control'] = 'Test'                                                                                                                                                    #
            df.loc[df['Test/Control']!='Test', 'Test/Control'] = 'Control'                                                                                                                                                         #
            df.drop(['Control_Identifier'], axis=1, inplace=True)                                                                                                                                                                  #
                                                                                                                                                                                                                                   #
            treatment_store_df = df.loc[df['Test/Control']=='Test'].copy()                                                                                                                                                         #
            treatment_store_df.reset_index(drop=True, inplace=True)                                                                                                                                                                #
                                                                                                                                                                                                                                   #
            c_store_df = df.loc[df['Test/Control']=='Control'].copy()                                                                                                                                                              #
            c_store_df.reset_index(drop=True, inplace=True)                                                                                                                                                                        #
                                                                                                                                                                                                                                   #
              # print('\nHere Is Test-Control Data...('+BOSorMatch+'-'+PriodOrYoY+'-'+m+'-'+c+')\n', c_store_df.head(), '\nTotal Obs:', len(c_store_df))                                                                           #
            if BOSorMatch == 'Matched':                                                                                                                                                                                            #
              test_control_df, c_map = KDTree_def.KDTree_def(data=df, test=treatment_store_df, control=c_store_df,                                                                                                                 #
                                                             vcn=vcn, var2pickneighbors=var2pickneighbors, no_of_control=no_of_control, replacement=with_replacement,                                                              #
                                                             Identifier='Identifier', Cluster='Cluster', Changed='Changed', Test='Test')                                                                                           #
              control_map.append(c_map)                                                                                                                                                                                            #
            else:                                                                                                                                                                                                                  #
              test_control_df = BOS_KDTree_def.BOS_KDTree_def(data=df, test=treatment_store_df, control=c_store_df,                                                                                                                #
                                                              vcn=vcn, var2pickneighbors=var2pickneighbors, Identifier='Identifier', Cluster='Cluster', Changed='Changed', Test='Test')                                            #
              control_map.append(len(c_store_df))                                                                                                                                                                                  #
            # print('\nHere Is Test-Control Data...('+BOSorMatch+'-'+PriodOrYoY+'-'+m+'-'+c+')\n', test_control_df.head(n=60),'\nHere is the Control Data:\n', control_df.head(n=60), '\n')                                        #
                                                                                                                                                                                                                                   #
            impact_df, p_val, p4_sales, p2_sales, timeseries, summary = prep_measure_def.prep_measure_def( cluster_date=cluster_date,                                                                                                       #
                                                                                                   test=treatment_store_df,                                                                                                        #
                                                                                                   Date_Col=Date_Col,                                                                                                                                            #
                                                                                                   Measure=Measure,                                                                                                                                              #
                                                                                                   Identifier=Identifier,                                                                                                                                        #
                                                                                                   test_control=test_control_df,                                                                                                                                 #
                                                                                                   Cluster=Cluster,                                                                                                                                              #
                                                                                                   cluster_name=c,                                                                                                                                               #
                                                                                                   measure_data=measure_data,                                                                                                                                    #
                                                                                                   Lift_Threshold=Lift_Threshold,                                                                                                                                #
                                                                                                   PriodOrYoY=PriodOrYoY )                                                                                                                                       #
            timeseries['PriodOrYoY'] = PriodOrYoY
            timeseries['BOSorMatch'] = BOSorMatch
            timeseries['Cluster'] = c
            timeseries['Method'] = m
            timeseries_df = pd.concat([timeseries_df, timeseries], axis=0, ignore_index=True)


            summary['PriodOrYoY'] = PriodOrYoY
            summary['BOSorMatch'] = BOSorMatch
            summary['Cluster'] = c
            summary['Method'] = m
            summary_df = pd.concat([summary_df, summary], axis=0, ignore_index=True)



            Tmt.append(len(treatment_store_df))                                                                                                                                                                                    #
            Ctrl.append(len(c_store_df))                                                                                                                                                                                           #
            Method_Cluster.append(PriodOrYoY+'_'+m+'_'+c)                                                                                                                                                                          #
            PorYoY_C.append(PriodOrYoY)                                                                                                                                                                                            #
            Method_C.append(m)                                                                                                                                                                                                     #
            Cluster_C.append(c)                                                                                                                                                                                                    #
            BOS_Matched.append(BOSorMatch)                                                                                                                                                                                         #
            Significance_Level.append(impact_df['Significance_Level'].mean())                                                                                                                                                      #
            AVG_Lift.append(impact_df['Lift'].mean())                                                                                                                                                                              #
            Expected_Impact.append(impact_df['Expected_Impact'].mean())                                                                                                                                                            #
            P_Value.append(p_val)                                                                                                                                                                                                  #
            Count.append(len(impact_df))                                                                                                                                                                                           #
            Sum_Above_Zero.append(impact_df.loc[impact_df['Lift']>0,'Identifier'].count())                                                                                                                                         #
            Sum_Above_Thres.append(impact_df['Above_Thres'].sum())                                                                                                                                                                 #
            Threshold.append(Lift_Threshold)                                                                                                                                                                                       #
            AVG_Treatment.append(p4_sales['P_Sales'].mean())                                                                                                                                                                       #
            AVG_Control.append(p2_sales['P_Sales'].mean())                                                                                                                                                                         #
            PCT_AT = 100*(impact_df['Above_Thres'].sum()/len(impact_df))                                                                                                                                                           #
            PCT_Above_Thres.append("{0:.5f}%".format(PCT_AT))                                                                                                                                                                      #
            PCT_AZ = 100*(impact_df.loc[impact_df['Lift']>0,'Identifier'].count()/len(impact_df))                                                                                                                                  #
            PCT_Above_Zero.append("{0:.5f}%".format(PCT_AZ))                                                                                                                                                                       #
            AVG_Diff.append(p4_sales['P_Sales'].mean() - p2_sales['P_Sales'].mean())                                                                                                                                               #
            if p_val <= 0.01: Significance_Word.append('High')                                                                                                                                                                     #
            elif (p_val > 0.01) & (p_val <= 0.05): Significance_Word.append('Moderate')                                                                                                                                            #
            elif (p_val > 0.05) & (p_val <= 0.10): Significance_Word.append('Marginal')                                                                                                                                            #
            else: Significance_Word.append('Not')                                                                                                                                                                                  #
                                                                                                                                                                                                                                   #
    if with_replacement.upper()=='T': re_placmt = True                                                                                                                                                                             #
    else: re_placmt = False                                                                                                                                                                                                        #
    lift_analysis_df = pd.DataFrame({'Method_Cluster': Method_Cluster,                                                                                                                                                             #
                                     'Method': Method_C,                                                                                                                                                                           #
                                     'PriorOrYoY': PorYoY_C,                                                                                                                                                                       #
                                     'BoSorMatched': BOS_Matched,                                                                                                                                                                  #
                                      Cluster: Cluster_C,                                                                                                                                                                          #
                                     'No_of_Tmt': Tmt,                                                                                                                                                                             #
                                     'No_of_Ctrl': Ctrl,                                                                                                                                                                           #
                                     'No_of_Ctrl_Map': control_map,                                                                                                                                                                #
                                     'Sig_Lvl': Significance_Level,                                                                                                                                                                #
                                     'Avg_Lift': AVG_Lift,                                                                                                                                                                         #
                                     'Exp_Imp': Expected_Impact,                                                                                                                                                                   #
                                     'P_Value': P_Value,                                                                                                                                                                           #
                                     'Count': Count,                                                                                                                                                                               #
                                     'Sum_Abv_Zero': Sum_Above_Zero,                                                                                                                                                               #
                                     'Sum_Abv_Thres': Sum_Above_Thres,                                                                                                                                                             #
                                     'Thres': Threshold,                                                                                                                                                                           #
                                     'Avg_Tmt': AVG_Treatment,                                                                                                                                                                     #
                                     'Avg_Ctrl': AVG_Control,                                                                                                                                                                      #
                                     'Pct_Abv_Thres': PCT_Above_Thres,                                                                                                                                                             #
                                     'Pct_Abv_Zero': PCT_Above_Zero,                                                                                                                                                               #
                                     'Avg_Diff': AVG_Diff,                                                                                                                                                                         #
                                     'Sig_Word': Significance_Word})                                                                                                                                                               #
    lift_analysis_df['Prfm_Meas'] = Measure                                                                                                                                                                                        #
    lift_analysis_df['Re_Plcmt'] = re_placmt                                                                                                                                                                                       #
    lift_analysis_df['Run_Date'] = dt.datetime.now().strftime("%Y-%m-%d")                                                                                                                                                          #
    Lift_Data_Col = ['BoSorMatched','PriorOrYoY','Method',Cluster,'No_of_Tmt','No_of_Ctrl','Re_Plcmt','No_of_Ctrl_Map','Sig_Lvl','Sig_Word','Avg_Lift','Exp_Imp',                                                                  #
                     'P_Value','Prfm_Meas','Count','Sum_Abv_Zero','Sum_Abv_Thres','Thres','Avg_Tmt','Avg_Ctrl','Pct_Abv_Thres','Pct_Abv_Zero','Avg_Diff','Run_Date']                                                               #
    lift_analysis_df = lift_analysis_df[Lift_Data_Col]                                                                                                                                                                             #
    print('\nHere Is The Final Lift Data...(No of Control: '+str(no_of_control)+')\n', lift_analysis_df.to_string(index=False))                                                                                                    #
    return [lift_analysis_df, timeseries_df, summary_df]                                                                                                                                                                                                        #
                                                                                                                                                                                                                                   #
  else:                                                                                                                                                                                                                            #
    print(Color.Color.R + Color.Color.Itallic + final_msg + Color.Color.W)                                                                                                                                                         #
    return final_msg                                                                                                                                                                                                               #
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#