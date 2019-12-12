# James Lovie 2019
# Disbursement Report Sum Script

# Import required libraries
import csv
from pathlib import Path
import pandas as pd
import os
import glob
# Class names should follow the UpperCaseCamelCase convention.
class Determine_Filenames:
    
    # Constructor: Instance variable names should be all lower case.
    def __init__(self, dirpath):
        self.dirpath = dirpath
    # A method to list all csv files in current path.
    def convert(self):
        directory = self.dirpath
        csv_file_list = []

        for csv_file in glob.glob('*.csv'):
            csv_file_list.append(csv_file)

        return csv_file_list, directory

class Disbursement_Extractor:

	# Constructor: Instance variable names should be all lower case.
    def __init__(self, directory, target_filename):
        self.directory = directory
        self.target_filename = target_filename
    # A method to extract fees and sum them.
    def extract_totals(self):
        data_folder = Path(self.directory)

        file_to_open = data_folder / self.target_filename

        with open(file_to_open, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            df = pd.DataFrame.from_dict(reader)

        # Remove all empty rows from dataframe.
        df = df[df['PP Total'].str.strip().astype(bool)]
        # Remove , and $ from values.
        df['PP Total'] = df['PP Total'].str.replace(',', '')
        df['PP Total'] = df['PP Total'].str.replace('$', '')
        # Convert values from object to float.
        df['PP Total'] = df['PP Total'].astype(float)
        # Sum values and round float to 2 decimal places.
        sum_of_fees = df['PP Total'].sum()
        sum_of_fees = round(sum_of_fees, 2)

        return sum_of_fees

def main():
    # Obtain current path.
    dirpath = os.getcwd()
    # Instantiating the class (for constants).
    filename_extractor =  Determine_Filenames(dirpath)
    # Call the method to obtain list of all csv files in current path.
    csv_file_list, directory = filename_extractor.convert()

    for csv_file in csv_file_list:
        print(csv_file)
        extractor = Disbursement_Extractor(directory, csv_file)
        # Call the method to extract the totals data.
        disbursement = extractor.extract_totals()
        # Output the results to the terminal.
        print(disbursement)

if __name__ == '__main__':
    main()
