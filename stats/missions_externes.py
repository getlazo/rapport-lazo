from db import get_connection
from utils import get_date_ranges

def get_missions_externes():
    start, end, start_prev, end_prev = get_date_ranges()
    query = f"""
        SELECT 'Current' AS period, COUNT(*) AS total_missions
        FROM Mission m
        JOIN ProviderProfile p ON m.providerProfileId = p.id
        WHERE (p.comPlanId IS NULL OR p.comPlanId != 2) AND m.startedAt BETWEEN '{start}' AND '{end}'
        UNION ALL
        SELECT 'Previous', COUNT(*)
        FROM Mission m
        JOIN ProviderProfile p ON m.providerProfileId = p.id
        WHERE (p.comPlanId IS NULL OR p.comPlanId != 2) AND m.startedAt BETWEEN '{start_prev}' AND '{end_prev}';
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result