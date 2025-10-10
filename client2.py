import sqlite3
import sqlite3
import os
from random import choice, randint
from datetime import datetime, timedelta
db_path = "/home/aidetic/Desktop/aidetic/sqlbacked/chat_backend/prequel_ai_volume/presales_demo_loan.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS loan_payments (
    Loan_ID TEXT,
    loan_status TEXT,
    Principal INTEGER,
    terms INTEGER,
    effective_date TEXT,
    due_date TEXT,
    paid_off_time TEXT,
    past_due_days REAL,
    age INTEGER,
    education TEXT,
    Gender TEXT
);
"""
cursor.execute(create_table_query)

statuses = ["PAIDOFF", "COLLECTION", "COLLECTION_PAIDOFF"]
education_levels = ["High School or Below", "Bachelor", "College"]
genders = ["male", "female"]

# Generate 10 sample rows
sample_rows = []
base_date = datetime(2016, 9, 1)
for i in range(10):
    loan_id = f"xqd201662{60 + i + 3}"  # continuing IDs
    loan_status = choice(statuses)
    principal = randint(500, 2000)
    terms = choice([7, 15, 30])
    effective_date = base_date + timedelta(days=randint(0, 30))
    due_date = effective_date + timedelta(days=terms)
    paid_off_time = None if loan_status != "PAIDOFF" else due_date - timedelta(days=randint(0, 3))
    past_due_days = None if loan_status == "PAIDOFF" else randint(1, 100)
    age = randint(20, 60)
    education = choice(education_levels)
    gender = choice(genders)

    sample_rows.append((
        loan_id, loan_status, principal, terms,
        effective_date.strftime("%Y-%m-%d"),
        due_date.strftime("%Y-%m-%d"),
        paid_off_time.strftime("%Y-%m-%d %H:%M") if paid_off_time else None,
        past_due_days,
        age,
        education,
        gender
    ))

# =========================
# Insert rows
# =========================
insert_query = """
INSERT INTO loan_payments (
    Loan_ID, loan_status, Principal, terms, effective_date, due_date,
    paid_off_time, past_due_days, age, education, Gender
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

cursor.executemany(insert_query, sample_rows)
conn.commit()
conn.close()

print(f"Inserted {len(sample_rows)} new rows into the loan_payments table.")


# Server response: 
# {'query_id': 'ee06cdcd-42ee-405f-a8fb-dfedd7dffc14', 'message': 'Generated SQL Query Validated', 'status_code': 200, 'error_message': None, 
#  'data': {'proceed': True, 'validated_queries':
#            [{'data':
#               [{'Loan_ID': 'xqd20166250', 'loan_status': 'PAIDOFF', 'Principal': 1000, 'terms': 15, 
#                 'effective_date': '2016-09-08', 'due_date': '2016-09-23', 'paid_off_time': '2016-09-22 14:30', 
#                 'past_due_days': 0.0, 'age': 30, 'education': 'Bachelor', 'Gender': 'male'},
#                   {'Loan_ID': 'xqd20166252', 'loan_status': 'PAIDOFF', 'Principal': 1500, 'terms': 30, 'effective_date': '2016-09-01', 'due_date': '2016-10-01', 'paid_off_time': '2016-09-28 10:00', 'past_due_days': 0.0, 'age': 45, 'education': 'College', 'Gender': 'male'},
#                  {'Loan_ID': 'xqd20166272', 'loan_status': 'PAIDOFF', 'Principal': 549, 'terms': 15, 'effective_date': '2016-09-21', 'due_date': '2016-10-06', 'paid_off_time': '2016-10-04 00:00', 'past_due_days': None, 'age': 56, 'education': 'College', 'Gender': 'male'}], 'fixed_query': "SELECT * FROM loan_payments WHERE LOWER(loan_status) = 'paidoff';", 'query_after_regex_match': "SELECT * FROM loan_payments WHERE LOWER(loan_status) = 'paidoff';", 'query_validation_remark': 'COMPLETED', 'no_attempts': 0}]}, 'step_data': [], 'type': 'INTERMEDIATE'}