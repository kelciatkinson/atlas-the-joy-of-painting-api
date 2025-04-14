# Runs the full ETL pipeline
from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

if __name__ == '__main__':
    file_path = 'clean_data/clean_data.csv'
    rows = transform_data(file_path)
    load_data(rows)
    print("ETL completed successfully.")