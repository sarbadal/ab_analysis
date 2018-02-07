
"""
Created on Sat Dec 30 10:51:22 2017

@author: Sarbadal.Pal
"""
import numpy as np

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def control_def(data=None, method='Original', cluster=None, var2pickneighbors = ['Seasonality','Trend']):                                                                                                                          #
  #Create the control data.                                                                                                                                                                                                        #
  if method=='Original': control_store_df = data[(data['Cluster']==cluster) & (data['Changed']==False)].copy()                                                                                                                     #
  else: control_store_df = data[(data['Cluster']==cluster)].copy()                                                                                                                                                                 #
                                                                                                                                                                                                                                   #
  #Normalized the Variales for distance calculation.                                                                                                                                                                               #
  vcn = []                                                                                                                                                                                                                         #
  for varI in var2pickneighbors:                                                                                                                                                                                                   #
    normal_z = 'Normal_'+varI                                                                                                                                                                                                      #
    vcn.append(normal_z)                                                                                                                                                                                                           #
    avg, std = control_store_df[varI].mean(), np.std(control_store_df[varI], ddof=1)                                                                                                                                               #
    control_store_df[normal_z] = (control_store_df[varI]-avg)/std                                                                                                                                                                  #
  return [control_store_df, vcn]                                                                                                                                                                                                   #
                                                                                                                                                                                                                                   #
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
