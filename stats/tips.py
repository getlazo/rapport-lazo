from db import get_connection
from utils import get_date_ranges

def get_tips():
    start, end, start_prev, end_prev = get_date_ranges()
    query = f"""
        SELECT 'Current' AS period,
            ROUND((COUNT(CASE WHEN tip > 0 THEN 1 END) * 100.0 / COUNT(*))) AS percentage_tipped_missions,
            SUM(tip) AS total_tip_amount
        FROM Mission
        WHERE status = 'DONE_FOR_USER' AND doneAt BETWEEN '{start}' AND '{end}'

        UNION ALL

        SELECT 'Previous',
            ROUND((COUNT(CASE WHEN tip > 0 THEN 1 END) * 100.0 / COUNT(*))),
            SUM(tip)
        FROM Mission
        WHERE status = 'DONE_FOR_USER' AND doneAt BETWEEN '{start_prev}' AND '{end_prev}';
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result