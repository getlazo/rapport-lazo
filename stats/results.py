from db import get_connection
from utils import get_date_ranges

def get_results_distribution():
    start, end, start_prev, end_prev = get_date_ranges()
    query = f"""
        SELECT 'Current' AS period,
            ROUND((COUNT(CASE WHEN result = 'Check_passed' THEN 1 END) * 100.0 / COUNT(*))) AS check_passed,
            ROUND((COUNT(CASE WHEN result = 'Fold' THEN 1 END) * 100.0 / COUNT(*))) AS fold,
            ROUND((COUNT(CASE WHEN result = 'No_Response' THEN 1 END) * 100.0 / COUNT(*))) AS no_response,
            ROUND((COUNT(CASE WHEN result = 'Conversation_outside_Lazo' THEN 1 END) * 100.0 / COUNT(*))) AS conversation_outside,
            ROUND((COUNT(CASE WHEN result NOT IN ('Check_passed', 'Fold', 'No_Response', 'Conversation_outside_Lazo') THEN 1 END) * 100.0 / COUNT(*))) AS other
        FROM Mission
        WHERE status = 'DONE_FOR_USER' AND doneAt BETWEEN '{start}' AND '{end}'

        UNION ALL

        SELECT 'Previous',
            ROUND((COUNT(CASE WHEN result = 'Check_passed' THEN 1 END) * 100.0 / COUNT(*))),
            ROUND((COUNT(CASE WHEN result = 'Fold' THEN 1 END) * 100.0 / COUNT(*))),
            ROUND((COUNT(CASE WHEN result = 'No_Response' THEN 1 END) * 100.0 / COUNT(*))),
            ROUND((COUNT(CASE WHEN result = 'Conversation_outside_Lazo' THEN 1 END) * 100.0 / COUNT(*))),
            ROUND((COUNT(CASE WHEN result NOT IN ('Check_passed', 'Fold', 'No_Response', 'Conversation_outside_Lazo') THEN 1 END) * 100.0 / COUNT(*)))
        FROM Mission
        WHERE status = 'DONE_FOR_USER' AND doneAt BETWEEN '{start_prev}' AND '{end_prev}';
    """
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
