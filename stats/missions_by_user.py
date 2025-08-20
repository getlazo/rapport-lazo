from db import get_connection
from utils import get_date_ranges

def get_missions_by_user():
    start, end, start_prev, end_prev = get_date_ranges()
    query = f"""
        SELECT 'Current' AS period,
            SUM(CASE WHEN LOWER(u.email) LIKE 'bea%' THEN 1 ELSE 0 END) AS beatrice,
            SUM(CASE WHEN LOWER(u.email) LIKE 'ra%' OR LOWER(u.email) LIKE 'admin%' THEN 1 ELSE 0 END) AS raphael,
            SUM(CASE WHEN LOWER(u.email) LIKE 'jul%' THEN 1 ELSE 0 END) AS jules,
            SUM(CASE WHEN LOWER(u.email) LIKE 'ti%' THEN 1 ELSE 0 END) AS tim
        FROM Mission m
        JOIN ProviderProfile p ON m.providerProfileId = p.id
        JOIN User u ON p.userId = u.id
        WHERE m.startedAt BETWEEN '{start}' AND '{end}'

        UNION ALL

        SELECT 'Previous',
            SUM(CASE WHEN LOWER(u.email) LIKE 'bea%' THEN 1 ELSE 0 END),
            SUM(CASE WHEN LOWER(u.email) LIKE 'ra%' OR LOWER(u.email) LIKE 'admin%' THEN 1 ELSE 0 END),
            SUM(CASE WHEN LOWER(u.email) LIKE 'jul%' THEN 1 ELSE 0 END),
            SUM(CASE WHEN LOWER(u.email) LIKE 'ti%' THEN 1 ELSE 0 END)
        FROM Mission m
        JOIN ProviderProfile p ON m.providerProfileId = p.id
        JOIN User u ON p.userId = u.id
        WHERE m.startedAt BETWEEN '{start_prev}' AND '{end_prev}';
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
