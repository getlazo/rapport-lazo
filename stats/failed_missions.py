from db import get_connection
from utils import get_date_ranges

def get_failed_missions():
    start, end, start_prev, end_prev = get_date_ranges()
    query = f"""
        SELECT 'Current' AS period, COUNT(*) AS failed_missions
        FROM Mission
        WHERE dateFailed IS NOT NULL AND dateFailed BETWEEN '{start}' AND '{end}'
        UNION ALL
        SELECT 'Previous', COUNT(*)
        FROM Mission
        WHERE dateFailed IS NOT NULL AND dateFailed BETWEEN '{start_prev}' AND '{end_prev}';
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result