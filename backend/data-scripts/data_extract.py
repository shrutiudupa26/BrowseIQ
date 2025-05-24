import os
import sqlite3
import pandas as pd
import shutil

# --------- Configuration ----------
user_profile_name = "Profile 2"  # Chrome profile directory name
base_path = os.path.expanduser(f"~")  # user home directory
chrome_history_path = os.path.join(base_path, "AppData", "Local", "Google", "Chrome", "User Data", user_profile_name, "History")

# Backup to avoid DB lock issues
backup_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "chrome_history_backup.db")
os.makedirs(os.path.dirname(backup_path), exist_ok=True)
shutil.copy2(chrome_history_path, backup_path)

# Connect to the copied database
conn = sqlite3.connect(backup_path)
cursor = conn.cursor()

# --------- Extract URLs Table ----------
urls_query = """
SELECT id, url, title, visit_count, typed_count, last_visit_time FROM urls
"""
urls_df = pd.read_sql_query(urls_query, conn)

# --------- Extract Visits Table ----------
visits_query = """
SELECT id, url, visit_time, from_visit, transition FROM visits
"""
visits_df = pd.read_sql_query(visits_query, conn)

# --------- Extract Search Terms Table ----------
keywords_query = """
SELECT * FROM keyword_search_terms
"""
keywords_df = pd.read_sql_query(keywords_query, conn)

# --------- Convert visit_time to readable format ----------
# Chrome stores timestamps in "Webkit time": microseconds since Jan 1, 1601
def convert_webkit_time(webkit_timestamp):
    if webkit_timestamp:
        # Convert WebKit timestamp (microseconds since 1601-01-01) to Unix timestamp (seconds since 1970-01-01)
        unix_timestamp = (webkit_timestamp / 1000000) - 11644473600  # Difference in seconds between 1601 and 1970
        return pd.to_datetime(unix_timestamp, unit='s')
    return None

visits_df['visit_time'] = visits_df['visit_time'].apply(convert_webkit_time)
urls_df['last_visit_time'] = urls_df['last_visit_time'].apply(convert_webkit_time)

# --------- Merge Data ----------
combined_df = visits_df.merge(urls_df, left_on='url', right_on='id', suffixes=('_visit', '_url'))

# --------- Save to CSV ----------
output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(output_dir, exist_ok=True)

urls_df.to_csv(os.path.join(output_dir, "urls.csv"), index=False)
visits_df.to_csv(os.path.join(output_dir, "visits.csv"), index=False)
keywords_df.to_csv(os.path.join(output_dir, "search_terms.csv"), index=False)
combined_df.to_csv(os.path.join(output_dir, "combined_history.csv"), index=False)

print(f"Extraction complete. Files saved in {output_dir}")

# --------- Cleanup ----------
cursor.close()
conn.close()
os.remove(backup_path)
