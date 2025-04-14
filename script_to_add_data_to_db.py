import pandas as pd
import ast
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
USERNAME = os.getenv("MYSQL_USERNAME")
PASSWORD = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
DB_NAME = os.getenv("MYSQL_DB_NAME")

# Connect to the MySQL database
engine = create_engine(f"mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{DB_NAME}")
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

# Reflect existing tables
episodes = Table("episode", metadata, autoload_with=engine)
colors = Table("color", metadata, autoload_with=engine)
episode_colors = Table("episode_color", metadata, autoload_with=engine)
subject_matter = Table("subject", metadata, autoload_with=engine)
episode_subject_matter = Table("episode_subject", metadata, autoload_with=engine)

# Load cleaned CSV
df = pd.read_csv("clean_data/clean_data.csv")

# Track mappings for lookup
color_id_map = {}
subject_id_map = {}

# Insert Episodes
for idx, row in df.iterrows():
    episode_id = idx + 1
    title = row["title"]
    air_date = row["og_date"]

    # Insert episode
    session.execute(
        episodes.insert().values(
            EpisodeID=episode_id,
            Title=title,
            AirDate=air_date
        )
    )

    # --- Handle colors ---
    color_list = ast.literal_eval(row["color_list"])
    for color_name in color_list:
        if color_name not in color_id_map:
            # Insert or get existing color
            existing_color = session.execute(
                select(colors.c.ColorID).where(colors.c.ColorName == color_name)
            ).scalar()
            if existing_color:
                color_id_map[color_name] = existing_color
            else:
                result = session.execute(colors.insert().values(ColorName=color_name))
                color_id = result.inserted_primary_key[0]
                color_id_map[color_name] = color_id

        # Link episode and color
        session.execute(
            episode_colors.insert().values(
                EpisodeID=episode_id,
                ColorID=color_id_map[color_name]
            )
        )

    # --- Handle subjects ---
    subject_list = ast.literal_eval(row["subject"])
    for subject in subject_list:
        if subject not in subject_id_map:
            existing_subject = session.execute(
                select(subject_matter.c.SubjectID).where(subject_matter.c.SubjectName == subject)
            ).scalar()
            if existing_subject:
                subject_id_map[subject] = existing_subject
            else:
                result = session.execute(subject_matter.insert().values(SubjectName=subject))
                subject_id = result.inserted_primary_key[0]
                subject_id_map[subject] = subject_id

        # Link episode and subject
        session.execute(
            episode_subject_matter.insert().values(
                EpisodeID=episode_id,
                SubjectID=subject_id_map[subject]
            )
        )

session.commit()
session.close()
print("Data has loaded into the database.")
