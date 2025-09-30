import sqlite3
import sqlite3
import os
from random import choice, randint
from datetime import datetime, timedelta
db_path = "/home/sanskar/Downloads/chat-with-your-data-presales_demo_preview/db/prequel_ai_volume/presales_demo_ecom.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("select * from loan_payments")
rows = cursor.fetchall()

column_names = [description[0] for description in cursor.description]
print("\t".join(column_names))  # tab-separated header

# Print each row
for row in rows:
    print(row)
