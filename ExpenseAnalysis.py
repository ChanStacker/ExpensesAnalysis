import pandas as pd
import datetime
import os

# Get the input directory path
input_dir = r'D:\Finance\CreditCards\Monzo\2024'

# Loop through all files in the input directory
for input_file in os.listdir(input_dir):
    # Check if the file is a CSV file
    if input_file.endswith('.csv'):
        # Load the CSV file into a pandas DataFrame
        df = pd.read_csv(os.path.join(input_dir, input_file))

        # Group the DataFrame by the 'Category' and 'Description' columns and calculate the total amount spent in each group
        grouped_df = df.groupby(['Category', 'Description'])['Amount'].sum().reset_index()

        # Sort the resulting DataFrame by the 'Category' and 'Amount' columns in descending order
        sorted_df = grouped_df.sort_values(['Category', 'Amount'], ascending=[True, False])

        # Add a column for the number of entries in each group
        sorted_df['Count'] = df.groupby(['Category', 'Description'])['Amount'].size().values

        # Add a column for the cumulative sum in each category
        sorted_df['Cumulative Sum'] = sorted_df.groupby('Category')['Amount'].cumsum()

        # Get the current datetime up to the minute
        now = datetime.datetime.now().strftime('%Y_%m_%d_%H%M')

        # Create the Output folder if it doesn't exist
        output_folder = 'Output'
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Write the results to a CSV file
        output_file = f'{output_folder}/{input_file.replace('.csv', '_output.csv')}_{now}.csv'
        sorted_df.to_csv(output_file, index=False)

        # Calculate the sum of the negative numbers
        negative_sum = df[df['Amount'] < 0]['Amount'].sum()

        # Print the sum of the negative numbers for the current file
        print(f'{input_file}: {negative_sum}')