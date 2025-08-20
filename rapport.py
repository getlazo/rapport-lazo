import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
from tabulate import tabulate
import os
from dotenv import load_dotenv

load_dotenv()  # Charge les variables depuis le .env

# Connexion MySQL
conn = mysql.connector.connect(
    host="tempted-db-usa.ckdg6yuue48n.us-east-1.rds.amazonaws.com",
    port=3306,
    user="tempted",
    password=os.getenv("MYSQL_PASSWORD"),
    database="production" 
)

cursor = conn.cursor(dictionary=True)

# Détermine les périodes
today = datetime.today()
end_current = today
start_current = end_current - timedelta(days=13)
end_previous = start_current - timedelta(days=1)
start_previous = end_previous - timedelta(days=13)

def format_date(dt):
    return dt.strftime('%Y-%m-%d 00:00:00')

# Fonctions
def run_query(start, end):
    query = f"""
    SELECT
        (SELECT COUNT(*) FROM Mission WHERE startedAt BETWEEN '{start}' AND '{end}') AS total_requests,
        (SELECT COUNT(*) FROM Mission WHERE doneAt BETWEEN '{start}' AND '{end}') AS done,
        (SELECT COUNT(*) FROM Mission WHERE status IN ('ONGOING', 'WAITING') AND startedAt BETWEEN '{start}' AND '{end}') AS ongoing_or_pending,
        (SELECT COUNT(*) FROM Mission WHERE status IN ('PARTIAL_REFUND') AND doneAt BETWEEN '{start}' AND '{end}') AS partial_refund,
        (SELECT COUNT(*) FROM Mission WHERE status IN ('EXPIRED_REQUEST', 'CANCELED_BY_PROVIDER') AND startedAt BETWEEN '{start}' AND '{end}') AS expired_requests,
        (SELECT COUNT(*) FROM Mission WHERE status = 'CANCELED_BY_USER' AND startedAt BETWEEN '{start}' AND '{end}') AS canceled_requests,
        (SELECT COUNT(*) FROM Mission WHERE status = 'Failed' AND doneAt BETWEEN '{start}' AND '{end}') AS failed
    """
    cursor.execute(query)
    return cursor.fetchone()

# Exécution
current_stats = run_query(format_date(start_current), format_date(end_current))
previous_stats = run_query(format_date(start_previous), format_date(end_previous))

# Mise en forme du tableau
rows = []
for key in current_stats:
    current = current_stats[key]
    previous = previous_stats[key]
    rows.append([key.replace("_", " ").title(), current, previous])

df = pd.DataFrame(rows, columns=["Mission Status", "These 2 weeks", "Past 2 weeks"])

print("\n📊 Missions key figures – ALL\n")
print(tabulate(df, headers='keys', tablefmt='github'))
