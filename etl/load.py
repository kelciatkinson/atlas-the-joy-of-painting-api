# Loads clean data into MySQL
from db.config import get_connection

def load_data(episodes):
    # get rid of duplicates episodes by title
    unique_episodes = {}
    for episode in episodes:
        if episode['title'] not in unique_episodes:
            unique_episodes[episode['title']] = episode
    
    # Converting back to a list for processing
    deduplicated_episodes = list(unique_episodes.values())
    # print(f"Original episode count: {len(episodes)}")
    # print(f"Deduplicated episode count: {len(deduplicated_episodes)}")
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Clears existing data
    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    cur.execute("TRUNCATE TABLE episode_color")
    cur.execute("TRUNCATE TABLE episode_subject")
    cur.execute("TRUNCATE TABLE episode")
    cur.execute("TRUNCATE TABLE color")
    cur.execute("TRUNCATE TABLE subject")
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")
    
    # Insert episodes
    episode_ids = {}
    for i, row in enumerate(deduplicated_episodes, start=1):
        episode_id = i
        episode_ids[row['title']] = episode_id
        
        cur.execute("""
            INSERT INTO episode (episode_id, title, season, episode, og_date, month, colors, subjects)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            episode_id,
            row['title'],
            row['season'],
            row['episode'],
            row['og_date'],
            row['month'],
            ','.join(row['colors']),
            ','.join(row['subjects']),
        ))
    
    # Insert colors
    all_colors = set()
    for row in deduplicated_episodes:
        for color in row['colors']:
            all_colors.add(color)
    
    color_ids = {}
    for i, color_name in enumerate(sorted(all_colors), start=1):
        cur.execute("INSERT INTO color (color_id, color_name) VALUES (%s, %s)", 
                    (i, color_name))
        color_ids[color_name] = i
    
    # Insert episode_color relationships
    for row in deduplicated_episodes:
        episode_id = episode_ids[row['title']]
        # Get rid of duplicate colors
        unique_episode_colors = set(row['colors'])
        
        for color_name in unique_episode_colors:
            color_id = color_ids[color_name]
            cur.execute("INSERT INTO episode_color (episode_id, color_id) VALUES (%s, %s)",
                        (episode_id, color_id))
    
    # Insert subjects
    all_subjects = set()
    for row in deduplicated_episodes:
        # Add each unique subject to our set
        for subject in row['subjects']:
            all_subjects.add(subject)
    
    subject_ids = {}
    for i, subject_name in enumerate(sorted(all_subjects), start=1):
        cur.execute("INSERT INTO subject (subject_id, subject_name) VALUES (%s, %s)", 
                    (i, subject_name))
        subject_ids[subject_name] = i
    
    # Inserts episode_subject relationships
    for row in deduplicated_episodes:
        episode_id = episode_ids[row['title']]
        # Gets rid of any duplicate subjects
        unique_episode_subjects = set(row['subjects'])
        
        for subject_name in unique_episode_subjects:
            subject_id = subject_ids[subject_name]
            cur.execute("INSERT INTO episode_subject (episode_id, subject_id) VALUES (%s, %s)",
                        (episode_id, subject_id))
    
    # Commit all changes and close connection
    conn.commit()
    cur.close()
    conn.close()
    
    print("ETL completed successfully.")