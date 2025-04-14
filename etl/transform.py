# Cleans and formats the data
import ast
import csv

def clean_row(row):
    return {
        'title': row['title'],
        'season': int(row['season']),
        'episode': int(row['episode']),
        'og_date': row['og_date'],
        'month': row['month'],
        'colors': ast.literal_eval(row['color_list']),
        'subjects': ast.literal_eval(row['subject']),
    }
    all_colors = set()
    for row in episodes:
        all_colors.update(row['colors'])
    color_id_map = {}
    for color_name in sorted(all_colors):
        if color_name:
            cur.execute("INSERT INTO color (color_name) VALUES (%s)", (color_name,))
            color_id = cur.lastrowid
            color_id_map[color_name] = color_id
    
    all_subjects = set()
    for row in episodes:
        all_subjects.update(row['subjects'])
    
    subject_id_map = {}
    for subject_name in sorted(all_subjects):
        if subject_name:
            cur.execute("INSERT INTO subject (subject_name) VALUES (%s)", (subject_name,))
            subject_id = cur.lastrowid
            subject_id_map[subject_name] = subject_id

def transform_data(file_path):
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        return [clean_row(row) for row in reader]
