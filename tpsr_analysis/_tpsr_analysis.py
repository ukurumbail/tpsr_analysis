"""Main module."""
import os
import pandas as pd
import numpy as np
from datetime import datetime

#defined variables
BP_T_Range = 10 #degC above T0 to go for 'bypass's

def generate_csv_IR(dir_IR,dir_IR_xy):

	
	xy_files = os.listdir(dir_IR_xy)
	timestamp_IR = [datetime.fromtimestamp(os.stat(dir_IR+f'\\{fname}').st_mtime) for fname in xy_files]

	fpath = dir_IR_xy+f'\\{xy_files[0]}' #get column values from the first file
	data = pd.read_csv(fpath,header=None,index_col=0).transpose() 

	IR_wavenumbers = [str(i) for i in data.columns]
	df_IR = pd.DataFrame(np.nan,index=timestamp_IR,columns=IR_wavenumbers) #set IR wavenumbers as column headers. Units cm^-1

	for (timestamp,fname) in zip(timestamp_IR,xy_files):
		fpath = dir_IR_xy+f'\\{fname}' 
		data = pd.read_csv(fpath,header=None,index_col=0).transpose() #one-row df
		df_IR.loc[timestamp,IR_wavenumbers] = data.values
	df_IR["XY Filenames"] = xy_files
	df_IR["Timestamp"] = df_IR.index
	return df_IR

def generate_csv(dir_data,IR_data_exists=False,only_IR=False):

	dir_IR = dir_data+"\\DRIFTS"
	dir_IR_xy = dir_data+"\\DRIFTS_xy"
	if only_IR:
		return generate_csv_IR(dir_IR,dir_IR_xy)

	dir_T = dir_data+"\\temperature"
	fpath_T = dir_T + "\\" + os.listdir(dir_T)[0]
	df_T = pd.read_csv(fpath_T,skiprows=[0]) #skip first gibberish row

	timestamp_T = pd.to_datetime(df_T.pop('Timestamp'),format='%Y-%m-%d %H:%M:%S')
	df_T.insert(0,'Timestamp',timestamp_T) 	#move timestamp to first column


	#2. Generate df from the MS data
	dir_MS = dir_data+"\\MS"
	fpath_MS = dir_MS + "\\" + os.listdir(dir_MS)[0]
	df_MS = pd.read_csv(fpath_MS) #skip first gibberish row

	timestamp_MS = pd.to_datetime(df_MS.pop('Timestamp'),format='%m/%d/%y %H:%M:%S.%f')
	df_MS.insert(0,'Timestamp',timestamp_MS) 	#move timestamp to first column


	#3. Generate df from the IR data if it exists
	if IR_data_exists:
		df_IR = generate_df_IR(dir_IR,dir_IR_xy)

	#4. Combine dfs
	if IR_data_exists: #generate one datapt per IR spectrum
		df = pd.concat([df_T,df_MS,df_IR]) 
		df = df.sort_values(by=['Timestamp'])
		df = df.set_index(df['Timestamp'])
		for MS_col_name in [name for name in df.columns if 'V1_I_' in name]:
			df[MS_col_name] = df[MS_col_name].interpolate(method='time') #time-based interpolation of any data that's missing MS data
			df=df.rename(columns={MS_col_name:f'M/Z {MS_col_name[5:]}'}) #clean up column name
		for T_col_name in ["Seconds","Block Temp","Set Point"]:
			df[T_col_name] = df[T_col_name].interpolate(method='time') #time-based interpolation of any data that's missing T data
		df=df.dropna() #drop all rows that have missing IR data (i.e. everything but the IR datapoints)
	else: #generate one datapt per T setpoints
		df = pd.concat([df_T,df_MS]) #each entry now has either NaN for T or NaN for MS data
		df = df.sort_values(by=['Timestamp'])
		df = df.set_index(df['Timestamp'])
		for MS_col_name in [name for name in df.columns if 'V1_I_' in name]:
			df[MS_col_name] = df[MS_col_name].interpolate(method='time') #time-based interpolation of any data that's missing MS data
			df=df.rename(columns={MS_col_name:f'M/Z {MS_col_name[5:]}'}) #clean up column name
		df=df.dropna() #drop all columns missing T data (i.e. the MS datapoints)

	return df

def analyze_tpsr(df,inert):
	#1. Generate bypass
	T0 = df['Block Temp'].iloc[0]
	bypass_pre = df[[col for col in df.columns if ('M/Z' in col or 'Block Temp' in col)]]
	bypass = bypass_pre[bypass_pre['Block Temp'] < T0 + BP_T_Range].mean()
	bypass_std = bypass_pre[bypass_pre['Block Temp'] < T0 + BP_T_Range].std()

	#2. Calculate Conversion 
	mass_range = [int(i.split(' ')[1]) for i in df.columns if 'M/Z' in i]
	internal_std = bypass[f'M/Z {inert}'] * 1/df[f'M/Z {inert}'] # in / out

	for mass in mass_range:
		species = f'M/Z {mass}'
		df[f'X {mass}'] = (bypass[species] - df[species].multiply(internal_std))/bypass[species]
		df['ISTD Ratio'] = internal_std

	return df