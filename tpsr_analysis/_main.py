"""Console script for tpsr_analysis."""
import os
import sys
import click
from _tpsr_analysis import generate_csv,analyze_tpsr


@click.command()
@click.option('--analyze',default=True,help='Run analysis of TPSR data.')
@click.option('--inert',default=28,help='M/Z of inert gas (e.g. 14, 28, 40).')
@click.option('--ir_data_exists',default=False,help='True if you wish to collate OPUS IR data as well, False if not.')
def main(analyze,inert,ir_data_exists):
	print("Welcome to the TPSR analysis software for the Hermans group DRIFTS setup!")
	print("Please ensure that you have copied the template folder into a new directory (e.g. 20230823-TPSR) and populated it with the correct files.")
	dir_path = input("Please provide the directory (e.g. C://20230823-TPSR): ")




	if os.path.exists(dir_path):

		#collate T and MS data
		print("\nGenerating dataset...")
		df = generate_csv(dir_path,IR_data_exists=ir_data_exists)




		if ir_data_exists:
			df.to_csv(dir_path+"/TPSR_dataset_with_IR.csv",index=False)
			print("\nSuccessully generated TPSR_dataset_with_IR.csv.")
		else:
			df.to_csv(dir_path+"/TPSR_dataset.csv",index=False)
			print("\nSuccessully generated TPSR_dataset.csv.")

		if analyze: #if we wish to perform analysis:
			df = analyze_tpsr(df,inert=inert)
			if ir_data_exists:
				df.to_csv(dir_path+"/TPSR_analysis_with_IR.csv",index=False)
				print("\nSuccessully generated TPSR_analysis_with_IR.csv.")

			else:
				df.to_csv(dir_path+"/TPSR_analysis.csv",index=False)
				print("\nSuccessully generated TPSR_analysis.csv.")

	else:
		print("Input directory does not exist! Please be sure you submit a proper directory.")



if __name__ == "__main__":
	sys.exit(main())  # pragma: no cover

