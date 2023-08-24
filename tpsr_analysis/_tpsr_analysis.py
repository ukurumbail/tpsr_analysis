"""Main module."""
import os
import pandas as pd

def generate_csv(dir_data):
	#fpath is the directory where the data lives. It should have the same structure as template_dir

	#1. Generate df from the temperature data.
	dir_T = dir_data+"\\temperature"
	fpath_T = dir_T + "\\" + os.listdir(dir_T)[0]
	df_T = pd.read_csv(fpath_T,skiprows=[0]) #skip first gibberish row

	timestamp_T = pd.to_datetime(df_T.pop('Timestamp'),format='%Y-%m-%d %H:%M:%S')
	df_T.insert(0,'Timestamp',timestamp_T) 	#move timestamp to first column
	T0 = df_T["Block Temp"].iloc[0] #degC


	#2. Generate MS data df
	dir_MS = dir_data+"\\MS"
	fpath_MS = dir_MS + "\\" + os.listdir(dir_MS)[0]
	df_MS = pd.read_csv(fpath_MS) #skip first gibberish row

	timestamp_MS = pd.to_datetime(df_MS.pop('Timestamp'),format='%m/%d/%y %H:%M:%S.%f')
	df_MS.insert(0,'Timestamp',timestamp_MS) 	#move timestamp to first column

	#3. Combine T and MS dfs
	df = pd.concat([df_T,df_MS]) #each entry now has either NaN for T or NaN for MS data
	df = df.sort_values(by=['Timestamp'])
	df = df.set_index(df['Timestamp'])
	for MS_col_name in [name for name in df.columns if 'V1_I_' in name]:
		df[MS_col_name] = df[MS_col_name].interpolate(method='time') #time-based interpolation of any data that's missing MS data
		df=df.rename(columns={MS_col_name:f'M/Z {MS_col_name[5:]}'}) #clean up column name
	df=df.dropna() #drop all columns missing T data (i.e. the MS datapoints)

	return df





		


