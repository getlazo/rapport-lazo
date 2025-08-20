from db import get_connection
from utils import get_date_ranges

def get_detailed_internal_missions():
    start, end, start_prev, end_prev = get_date_ranges()
    query = f"""
        SELECT 'Current' as period,
            COUNT(*) AS total_missions_started,
            SUM(CASE WHEN m.doneAt IS NOT NULL THEN 1 ELSE 0 END) AS total_missions_done,
            SUM(CASE WHEN m.status IN ('ONGOING', 'WAITING') THEN 1 ELSE 0 END) AS ongoing_or_pending,
            SUM(CASE WHEN m.status = 'Failed' THEN 1 ELSE 0 END) AS failed_missions,
            SUM(CASE WHEN m.status IN ('EXPIRED_REQUEST', 'CANCELED_BY_PROVIDER') THEN 1 ELSE 0 END) AS expired_requests,
            SUM(CASE WHEN m.status = 'PARTIAL_REFUND' THEN 1 ELSE 0 END) AS partial_refunds,
            SUM(CASE WHEN m.status = 'CANCELED_BY_USER' THEN 1 ELSE 0 END) AS canceled_requests
        FROM Mission m
        JOIN ProviderProfile p ON m.providerProfileId = p.id
        WHERE p.comPlanId = 2 AND m.startedAt BETWEEN '{start}' AND '{end}'

        UNION ALL

        SELECT 'Previous',
            COUNT(*),
            SUM(CASE WHEN m.doneAt IS NOT NULL THEN 1 ELSE 0 END),
            SUM(CASE WHEN m.status IN ('ONGOING', 'WAITING') THEN 1 ELSE 0 END),
            SUM(CASE WHEN m.status = 'Failed' THEN 1 ELSE 0 END),
            SUM(CASE WHEN m.status IN ('EXPIRED_REQUEST', 'CANCELED_BY_PROVIDER') THEN 1 ELSE 0 END),
            SUM(CASE WHEN m.status = 'PARTIAL_REFUND' THEN 1 ELSE 0 END),
            SUM(CASE WHEN m.status = 'CANCELED_BY_USER' THEN 1 ELSE 0 END)
        FROM Mission m
        JOIN ProviderProfile p ON m.providerProfileId = p.id
        WHERE p.comPlanId = 2 AND m.startedAt BETWEEN '{start_prev}' AND '{end_prev}';
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
