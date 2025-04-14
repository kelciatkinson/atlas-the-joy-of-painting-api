# Reads CSV data
import csv

def extract_data(filepath):
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)
