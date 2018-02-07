
"""
Created on Sat Dec 30 10:51:22 2017

@author: Sarbadal.Pal
"""
import pandas as pd

def cond_check_def(no_of_control = 10,
                var2pickneighbors = ['Seasonality','Trend'],
                with_replacement = 'T',
                Lift_Threshold = 2,
                Identifier = 'Store', Date_Col = 'Date', Measure = 'Sales', Cluster = 'Cluster', Changed = 'Changed', Test = 'Test',
                trend_data=None, measure_data=None, cluster_date=None): 
  
  if (type(no_of_control)==type(1)) or (type(no_of_control)==type(1.0)):
    if (type(no_of_control)==type(1)) & (no_of_control>0): 
      return1_type = True
      return1_msg = ''
    else: 
      return1_type = False
      return1_msg = '\nno_of_control takes only None or positive integer number.'
  elif no_of_control==None:
    return1_type = True
    return1_msg = ''
  else:
    return1_type = False
    return1_msg = '\nno_of_control takes only None or positive integer number.'

  if type(var2pickneighbors)==type([]):
    return2_type = True
    return2_msg = ''
  else: 
    return2_type = False
    return2_msg = '\nvar2pickneighbors takes only List.'

  if (type(with_replacement)==type(True)) or (with_replacement in ['T','F','t','f']):
    return3_type = True
    return3_msg = ''
  else:
    return3_type = False
    return3_msg = '\nwith_replacement takes either (True or False) or (T or F)'

  if (type(Lift_Threshold)==type(1)) or (type(Lift_Threshold)==type(1.0)): 
    return4_type = True
    return4_msg = ''
  else:
    return4_type = False
    return4_msg = '\nLift_Threshold takes only Number'

  basic_tf = return1_type & return2_type & return3_type & return4_type
  basic_msg = return1_msg + return2_msg + return3_msg + return4_msg


  if type(trend_data)==type(pd.DataFrame()):

    td = True
    td_msg = ''

    if Changed in trend_data.columns.tolist():
      return10_type = True
      return10_msg = ''
    else:
      return10_type = False
      return10_msg = '\n{} column does not exist in {} DataFrame'.format(Changed, 'trend_data')

    if Test in trend_data.columns.tolist():
      return11_type = True
      return11_msg = ''
    else:
      return11_type = False
      return11_msg = '\n{} column does not exist in {} DataFrame'.format(Test, 'trend_data')

    if Identifier in trend_data.columns.tolist():
      return12_type = True
      return12_msg = ''
    else:
      return12_type = False
      return12_msg = '\n{} column does not exist in {} DataFrame'.format(Identifier, 'trend_data')

    if Cluster in trend_data.columns.tolist():
      return13_type = True
      return13_msg = ''
    else:
      return13_type = False
      return13_msg = '\n{} column does not exist in {} DataFrame'.format(Cluster, 'trend_data')

    tmp_dic = {}
    itm_type = True
    itm_msg = ''
    if type(var2pickneighbors)==type([]):
      for i, itm in enumerate(var2pickneighbors):
        if itm in trend_data.columns.tolist():
          tmp_dic[itm+'_type'] = True
          tmp_dic[itm+'_msg'] = ''
        else:
          tmp_dic[itm+'_type'] = False
          tmp_dic[itm+'_msg'] = '\n{} column does not exist in {} DataFrame'.format(itm, 'trend_data')

      for i, itm in enumerate(var2pickneighbors):
        itm_type = itm_type & tmp_dic[itm+'_type']
        itm_msg = itm_msg + tmp_dic[itm+'_msg']

    td_tf = return10_type & return11_type & return12_type & return13_type & itm_type
    td_msg = return10_msg + return11_msg + return12_msg + return13_msg + itm_msg

  else:
    td_tf = False
    td_msg = '\nNo valid data for trend_data param is given.'


  if type(measure_data)==type(pd.DataFrame()):

    md = True
    md_msg = ''

    if Identifier in measure_data.columns.tolist():
      return21_type = True
      return21_msg = ''
    else:
      return21_type = False
      return21_msg = '\n{} column does not exist in {} DataFrame'.format(Identifier, 'measure_data')

    if Date_Col in measure_data.columns.tolist():
      return22_type = True
      return22_msg = ''
    else:
      return22_type = False
      return22_msg = '\n{} column does not exist in {} DataFrame'.format(Date_Col, 'measure_data')

    if Measure in measure_data.columns.tolist():
      return23_type = True
      return23_msg = ''
    else:
      return23_type = False
      return23_msg = '\n{} column does not exist in {} DataFrame'.format(Measure, 'measure_data')

    md_tf = return21_type & return22_type & return23_type
    md_msg = return21_msg + return22_msg + return23_msg

  else:
    md_tf = False
    md_msg = '\nNo valid data for measure_data param is given.'

  if type(cluster_date)==type(pd.DataFrame()):

    cd = True
    cd_msg = ''

    if Cluster in cluster_date.columns.tolist():
      return31_type = True
      return31_msg = ''
    else:
      return31_type = False
      return31_msg = '\n{} column does not exist in {} DataFrame'.format(Cluster, 'cluster_date')

    if 'Test_StartDate' in cluster_date.columns.tolist():
      return32_type = True
      return32_msg = ''
    else:
      return32_type = False
      return32_msg = '\n{} column does not exist in {} DataFrame'.format('Test_StartDate', 'cluster_date')

    if 'Test_EndDate' in cluster_date.columns.tolist():
      return33_type = True
      return33_msg = ''
    else:
      return33_type = False
      return33_msg = '\n{} column does not exist in {} DataFrame'.format('Test_EndDate', 'cluster_date')

    if 'Prior_StartDate' in cluster_date.columns.tolist():
      return34_type = True
      return34_msg = ''
    else:
      return34_type = False
      return34_msg = '\n{} column does not exist in {} DataFrame'.format('Prior_StartDate', 'cluster_date')

    if 'Prior_EndDate' in cluster_date.columns.tolist():
      return35_type = True
      return35_msg = ''
    else:
      return35_type = False
      return35_msg = '\n{} column does not exist in {} DataFrame'.format('Prior_EndDate', 'cluster_date')

    if 'YoY_StartDate' in cluster_date.columns.tolist():
      return36_type = True
      return36_msg = ''
    else:
      return36_type = False
      return36_msg = '\n{} column does not exist in {} DataFrame'.format('YoY_StartDate', 'cluster_date')

    if 'YoY_EndDate' in cluster_date.columns.tolist():
      return37_type = True
      return37_msg = ''
    else:
      return37_type = False
      return37_msg = '\n{} column does not exist in {} DataFrame'.format('YoY_EndDate', 'cluster_date')

    cd_tf = return31_type & return32_type & return33_type & return34_type & return35_type & return36_type & return37_type
    cd_msg = return31_msg + return32_msg + return33_msg + return34_msg + return35_msg + return36_msg + return37_msg

  else:
    cd_tf = False
    cd_msg = '\nNo valid data for cluster_date param is given.'

  
  if basic_tf & td_tf & md_tf & cd_tf:
    final_tf = True
    final_msg = 'All is well.' 
  else:
    final_tf = False
    final_msg = '\nError:' + basic_msg + td_msg + md_msg + cd_msg

  return [final_tf, final_msg]















