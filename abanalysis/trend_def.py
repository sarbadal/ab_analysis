
"""
Created on Sat Dec 30 10:51:22 2017

@author: Sarbadal.Pal
"""
import pandas as pd
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def trend_def(data = None, Identifier = 'Store', Cluster = 'Cluster', Changed = 'Changed', Test = 'Test'):
  #create a temporary trand data. This is to make sure it does not overwrite original trand data.
  #Add "All" cluster into the temporary trend data.
  trend_df = data.copy()
  trend_df.rename(columns={Identifier:'Identifier',Cluster:'Cluster',Changed:'Changed',Test:'Test'}, inplace=True)
  trend_df_all_cluster = trend_df.copy()
  trend_df_all_cluster['Cluster'] = 'All'
  trend_df = pd.concat([trend_df, trend_df_all_cluster])
  trend_df.reset_index(drop=True, inplace=True)
  return trend_df
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
