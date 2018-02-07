
"""
Created on Sat Dec 30 10:51:22 2017

@author: Sarbadal.Pal
"""
import pandas as pd
from abanalysis import add_years
from scipy.stats import ttest_ind

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def prep_measure_def(cluster_date=None, test=None, Date_Col=None, Measure=None, Identifier=None, Lift_Threshold=None,                                                                                                              #
                     test_control=None, Cluster=None, cluster_name=None, measure_data=None, PriodOrYoY=None):                                                                                                                      #
  #Extract Dates from Cluster Date Data...                                                                                                                                                                                         #
  Test_StartDate = cluster_date.loc[cluster_date[Cluster]==cluster_name, 'Test_StartDate'].tolist()[0]                                                                                                                             #
  Test_EndDate = cluster_date.loc[cluster_date[Cluster]==cluster_name, 'Test_EndDate'].tolist()[0]                                                                                                                                 #
  Prior_StartDate = cluster_date.loc[cluster_date[Cluster]==cluster_name, 'Prior_StartDate'].tolist()[0]                                                                                                                           #
  Prior_EndDate = cluster_date.loc[cluster_date[Cluster]==cluster_name, 'Prior_EndDate'].tolist()[0]                                                                                                                               #
  YoY_StartDate = cluster_date.loc[cluster_date[Cluster]==cluster_name, 'YoY_StartDate'].tolist()[0]                                                                                                                               #
  YoY_EndDate = cluster_date.loc[cluster_date[Cluster]==cluster_name, 'YoY_EndDate'].tolist()[0]                                                                                                                                   #
                                                                                                                                                                                                                                   #
  Test_StartDate = str(Test_StartDate)[0: min(10, len(str(Test_StartDate)))]                                                                                                                                                       #
  Test_EndDate = str(Test_EndDate)[0: min(10, len(str(Test_EndDate)))]                                                                                                                                                             #
  Prior_StartDate = str(Prior_StartDate)[0: min(10, len(str(Prior_StartDate)))]                                                                                                                                                    #
  Prior_EndDate = str(Prior_EndDate)[0: min(10, len(str(Prior_EndDate)))]                                                                                                                                                          #
  YoY_StartDate = str(YoY_StartDate)[0: min(10, len(str(YoY_StartDate)))]                                                                                                                                                          #
  YoY_EndDate = str(YoY_EndDate)[0: min(10, len(str(YoY_EndDate)))]                                                                                                                                                                #
                                                                                                                                                                                                                                   #
  if PriodOrYoY == 'YoY':                                                                                                                                                                                                          #
    Prior_StartDate, Prior_EndDate = YoY_StartDate, YoY_EndDate                                                                                                                                                                    #
                                                                                                                                                                                                                                   #
  try:                                                                                                                                                                                                                             #
    Test_StartDate, Test_EndDate = pd.to_datetime(Test_StartDate), pd.to_datetime(Test_EndDate)                                                                                                                                    #
    if (len(Prior_StartDate)!=10) or (len(Prior_EndDate)!=10):                                                                                                                                                                     #
      Prior_StartDate = add_years.add_years(pd.to_datetime(Test_StartDate), -1)                                                                                                                                                    #
      Prior_EndDate = add_years.add_years(pd.to_datetime(Test_EndDate), -1)                                                                                                                                                        #
    else:                                                                                                                                                                                                                          #
      try:                                                                                                                                                                                                                         #
        Prior_StartDate, Prior_EndDate = pd.to_datetime(Prior_StartDate), pd.to_datetime(Prior_EndDate)                                                                                                                            #
      except:                                                                                                                                                                                                                      #
        print('Priod Date format is not correct. Please check.')                                                                                                                                                                   #
  except:                                                                                                                                                                                                                          #
    print('Date format is not correct. Please check.')                                                                                                                                                                             #
                                                                                                                                                                                                                                   #
  test_store_df = test.copy()                                                                                                                                                                                                      #
  measure_df = measure_data.copy()                                                                                                                                                                                                 #
  measure_df.rename(columns={Date_Col:'Date', Measure:'Sales', Identifier:'Identifier'}, inplace=True)                                                                                                                             #
  measure_df['Date'] = pd.to_datetime(measure_df['Date'])                                                                                                                                                                          #
  measure_df['P_Type'] = 'NTCP'                                                                                                                                                                                                    #
  measure_df.loc[(measure_df['Date'] >= Test_StartDate) & (measure_df['Date'] <= Test_EndDate), 'P_Type'] = 'Test'                                                                                                                 #
  measure_df.loc[(measure_df['Date'] >= Prior_StartDate) & (measure_df['Date'] <= Prior_EndDate), 'P_Type'] = 'Comparison'                                                                                                         #
                                                                                                                                                                                                                         ###       #
  test_store_df['U_Type'] = 'Treatment'                                                                                                                                                                                  ###       #
  test_store_df['Control_ID'] = test_store_df['Identifier']                                                                                                                                                              ###       #
  test_store_df['TtoC_Dist'] = 0                                                                                                                                                                                         ###       #
  test_store_df = test_store_df[['Identifier','U_Type','Control_ID','TtoC_Dist']].copy()                                                                                                                                 ###       #
                                                                                                                                                                                                                         ###       #
  test_control['U_Type'] = 'Control'                                                                                                                                                                                     ###       #
  test_control_df = pd.concat([test_store_df, test_control[['Identifier','U_Type','Control_ID','TtoC_Dist']]])                                                                                                           ###       #
  TC_List =  test_control_df['Control_ID'].unique().tolist()                                                                                                                                                             ###       #
  sales_df_to_use = measure_df[(measure_df['P_Type'].isin(['Comparison','Test'])) & (measure_df['Identifier'].isin(TC_List))][['Identifier','Date','P_Type','Sales']].rename(columns={'Identifier':'Control_ID'}).copy() ###       #
  test_control_df = pd.merge(sales_df_to_use, test_control_df, how='left',left_on='Control_ID', right_on='Control_ID',left_index=False, right_index=False, sort=False)                                                   ###       #
                                                                                                                                                    ###                                                                  ###       #
  avg_sales = pd.DataFrame(test_control_df[test_control_df['P_Type']=='Comparison'].groupby(['Control_ID'])['Sales'].mean()).rename(columns={'Sales':'AVG_Sales'})                                                       ###       #
  avg_sales.reset_index(inplace=True)                                                                                                                                                                                    ###       #
  avg_sales = pd.merge(test_control_df[test_control_df['P_Type'].isin(['Comparison','Test'])], avg_sales, how='left', on=['Control_ID'], left_index=False, right_index=False, sort=False)                                ###       #
  avg_sales['P_Sales'] = 100*(avg_sales['Sales']-avg_sales['AVG_Sales'])/avg_sales['AVG_Sales']                                                                                                                          ###       #


  #TIMESERIRS DATA PREP....................

  time_series_control = avg_sales[avg_sales['U_Type']=='Control'].groupby(['P_Type','Date'])[['P_Sales']].mean()
  time_series_control.reset_index(inplace=True)
  time_series_control.rename(columns={'P_Sales': 'Control'}, inplace=True)

  time_series_treatment = avg_sales[avg_sales['U_Type']=='Treatment'].groupby(['P_Type','Date'])[['P_Sales']].mean()
  time_series_treatment.reset_index(inplace=True)
  time_series_treatment.rename(columns={'P_Sales': 'Treatment'}, inplace=True)

  time_series = pd.merge(time_series_treatment, time_series_control, how='inner', on=['P_Type','Date'], left_index=False, right_index=False, sort=False) 
  time_series = time_series[['P_Type','Date','Control','Treatment']]

  #End of Timeseries data Prep..............
                                                                                                                                                                                                                         ###       #
  c = ['Identifier','Control_ID', 'P_Sales']                                                                                                                                                                             ###       #
  p1_sales = avg_sales[(avg_sales['P_Type']=='Comparison') & (avg_sales['U_Type']=='Control')][c].groupby(['Identifier','Control_ID'])[['P_Sales']].mean()                                                               ###       #
  p1_sales.reset_index(inplace=True)                                                                                                                                                                                     ###       #
                                                                                                                                                                                                                         ###       #
  p2_sales = avg_sales[(avg_sales['P_Type']=='Test') & (avg_sales['U_Type']=='Control')][c].groupby(['Identifier','Control_ID'])[['P_Sales']].mean()                                                                     ###       #
  p2_sales.reset_index(inplace=True)                                                                                                                                                                                     ###       #
                                                                                                                                                                                                                         ###       #
  p3_sales = avg_sales[(avg_sales['P_Type']=='Comparison') & (avg_sales['U_Type']=='Treatment')][c].groupby(['Identifier','Control_ID'])[['P_Sales']].mean()                                                             ###       #
  p3_sales.reset_index(inplace=True)                                                                                                                                                                                     ###       #
                                                                                                                                                                                                                         ###       #
  p3_avg_sales = avg_sales[(avg_sales['P_Type']=='Comparison') & (avg_sales['U_Type']=='Treatment')].groupby(['Identifier',])[['AVG_Sales']].mean()                                                                      ###       #
  p3_avg_sales.reset_index(inplace=True)                                                                                                                                                                                 ###       #
                                                                                                                                                                                                                         ###       #
  p4_sales = avg_sales[(avg_sales['P_Type']=='Test') & (avg_sales['U_Type']=='Treatment')][c].groupby(['Identifier','Control_ID'])[['P_Sales']].mean()                                                                   ###       #
  p4_sales.reset_index(inplace=True)                                                                                                                                                                                     ###       #
                                                                                                                                                                                                                         ###       #
  p1p2_sales = pd.merge(p1_sales.rename(columns={'P_Sales':'PTypeComparison_P_Sales'}), p2_sales.rename(columns={'P_Sales':'PTypeTest_P_Sales'}),                                                                        ###       #
                        how='inner', on=['Identifier','Control_ID'], left_index=False, right_index=False, sort=False)                                                                                                    ###       #
  p1p2_sales['D_Measure'] = p1p2_sales['PTypeTest_P_Sales'] - p1p2_sales['PTypeComparison_P_Sales']                                                                                                                      ###       #
                                                                                                                                                                                                                         ###       #
  p3p4_sales = pd.merge(p3_sales.rename(columns={'P_Sales':'PTypeComparison_P_Sales'}), p4_sales.rename(columns={'P_Sales':'PTypeTest_P_Sales'}),                                                                        ###       #
                        how='inner', on=['Identifier','Control_ID'], left_index=False, right_index=False, sort=False)                                                                                                    ###       #
  p3p4_sales['D_Measure'] = p3p4_sales['PTypeTest_P_Sales'] - p3p4_sales['PTypeComparison_P_Sales']                                                                                                                      ###       #
                                                                                                                                                                                                                         ###       #
  p1p2_sales.drop(['PTypeTest_P_Sales','PTypeComparison_P_Sales'], axis=1, inplace=True)                                                                                                                                 ###       #
  p1p2_sales.rename(columns={'D_Measure':'Control_DMeasure'}, inplace=True)                                                                                                                                              ###       #
  p3p4_sales.drop(['PTypeTest_P_Sales','PTypeComparison_P_Sales','Control_ID'], axis=1, inplace=True)                                                                                                                    ###       #
  p3p4_sales.rename(columns={'D_Measure':'Treatment_DMeasure'}, inplace=True)                                                                                                                                            ###       #
                                                                                                                                                                                                                         ###       #
  lift_analysis_df = pd.merge(p1p2_sales, p3p4_sales, how='outer', on=['Identifier'], left_index=False, right_index=False, sort=False)                                                                                   ###       #
  lift_analysis_df['Lift'] = (lift_analysis_df['Treatment_DMeasure']-lift_analysis_df['Control_DMeasure'])/(1+0.01*lift_analysis_df['Control_DMeasure'])                                                                 ###       #
  lift_analysis_df = lift_analysis_df[['Identifier','Control_ID','Lift']].copy()                                                                                                                                                   #
                                                                                                                                                                                                                                   #
  ###... TTest ANALYSIS... TTest ANALYSIS... TTest ANALYSIS... TTest ANALYSIS... TTest ANALYSIS... TTest ANALYSIS... TTest ANALYSIS... TTest ANALYSIS... TTest ANALYSIS... TTest ANALYSIS... TTest ANALYSIS   ##############       #
  t_stat, p_val = ttest_ind(p1p2_sales['Control_DMeasure'], p3p4_sales['Treatment_DMeasure'], equal_var=False)                                                                                        # Expected           #       #
  impact_df = pd.merge(lift_analysis_df, avg_sales[['Identifier','Control_ID','P_Sales']], how='left', on=['Identifier','Control_ID'], left_index=False, right_index=False, sort=False)               # Impact             #       #
  impact_df = pd.merge(impact_df, p3_avg_sales, how='left', on=['Identifier'], left_index=False, right_index=False, sort=False)                                                                       #                    #       #
  impact_df = pd.DataFrame(impact_df.groupby(['Identifier','Control_ID'])['AVG_Sales','P_Sales','Lift'].mean())                                                                                       # and                #       #
  impact_df.reset_index(inplace=True)                                                                                                                                                                 # Significance Level #       #
  impact_df['Expected_Impact'] = 0.01*impact_df['Lift']*impact_df['AVG_Sales']                                                                                                                        #                    #       #
  impact_df['Significance_Level'] = 100*(1-p_val)                                                                                                                                                     #                    #       #
  impact_df['Above_Thres'] = 0                                                                                                                                                                        #                    #       #
  impact_df.loc[impact_df['Lift']>Lift_Threshold,'Above_Thres'] = 1                                                                                                                                   #                    #       #
                                                                                                                                                                                                                                   #
  return [impact_df, p_val, p4_sales, p2_sales, time_series]                                                                                                                                                                       #
                                                                                                                                                                                                                                   #
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
