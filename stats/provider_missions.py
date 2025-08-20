from db import get_connection
from utils import get_date_ranges

def get_provider_missions():
    start, end, start_prev, end_prev = get_date_ranges()
    
    # Query pour la période actuelle
    query_current = f"""
    SELECT
        CASE 
            WHEN LOWER(u.email) LIKE 'raph%' THEN 'Raph'
            WHEN LOWER(u.email) LIKE 'jules%' THEN 'Jules'
            WHEN LOWER(u.email) LIKE 'tim%' THEN 'Tim'
            ELSE 'Externals'
        END AS person,
        COUNT(CASE WHEN m.dateFailedForUser IS NOT NULL THEN 1 END) AS mark_as_failed
    FROM
        Mission m
    JOIN
        ProviderProfile p ON m.providerProfileId = p.id
    JOIN
        User u ON p.userId = u.id
    WHERE
        m.startedAt >= '{start}'
    GROUP BY
        person
    ORDER BY
        CASE person
            WHEN 'Tim' THEN 1
            WHEN 'Raph' THEN 2
            WHEN 'Jules' THEN 3
            WHEN 'Externals' THEN 4
        END
    """
    
    # Query pour la période précédente
    query_previous = f"""
    SELECT
        CASE 
            WHEN LOWER(u.email) LIKE 'raph%' THEN 'Raph'
            WHEN LOWER(u.email) LIKE 'jules%' THEN 'Jules'
            WHEN LOWER(u.email) LIKE 'tim%' THEN 'Tim'
            ELSE 'Externals'
        END AS person,
        COUNT(CASE WHEN m.dateFailedForUser IS NOT NULL THEN 1 END) AS mark_as_failed
    FROM
        Mission m
    JOIN
        ProviderProfile p ON m.providerProfileId = p.id
    JOIN
        User u ON p.userId = u.id
    WHERE
        m.startedAt >= '{start_prev}'
    GROUP BY
        person
    ORDER BY
        CASE person
            WHEN 'Tim' THEN 1
            WHEN 'Raph' THEN 2
            WHEN 'Jules' THEN 3
            WHEN 'Externals' THEN 4
        END
    """
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(query_current)
    current_results = cursor.fetchall()
    
    cursor.execute(query_previous)
    previous_results = cursor.fetchall()
    
    conn.close()
    
    # Créer des dictionnaires avec les résultats
    current_dict = {row['person']: row['mark_as_failed'] for row in current_results}
    previous_dict = {row['person']: row['mark_as_failed'] for row in previous_results}
    
    # Retourner le format attendu par utils.py
    return [
        {
            'period': 'Current',
            'tim': current_dict.get('Tim', 0),
            'raph': current_dict.get('Raph', 0),
            'jules': current_dict.get('Jules', 0),
            'externals': current_dict.get('Externals', 0)
        },
        {
            'period': 'Previous',
            'tim': previous_dict.get('Tim', 0),
            'raph': previous_dict.get('Raph', 0),
            'jules': previous_dict.get('Jules', 0),
            'externals': previous_dict.get('Externals', 0)
        }
    ] 