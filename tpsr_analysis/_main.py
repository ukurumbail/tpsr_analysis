"""Console script for tpsr_analysis."""
import os
import sys
import click
from _tpsr_analysis import generate_csv


@click.command()
def main(args=None):
	print("Welcome to the TPSR analysis software for the Hermans group DRIFTS setup!")
	print("Please ensure that you have copied the template folder into a new directory (e.g. 20230823-TPSR) and populated it with the correct files.")
	print("Please ensure that your bypass is contained within the MS CSV file.")
	dir_path = input("Please provide the directory (e.g. C://20230823-TPSR): ")




	if os.path.exists(dir_path):
		df = generate_csv(dir_path)
		df.to_csv(dir_path+"/TPSR_dataset.csv",index=False)
	else:
		print("Input directory does not exist! Please be sure you submit a proper directory.")


if __name__ == "__main__":
	sys.exit(main())  # pragma: no cover

