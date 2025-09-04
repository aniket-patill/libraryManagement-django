from django.http import JsonResponse
from librarymanager.database.create_connection import get_db_connection

def healthcheck(request):
    db_status = 'error'
    try:
        conn = get_db_connection()
        if conn and conn.is_connected():
            db_status = 'ok'
            conn.close()
    except Exception as e:
        db_status = f'error: {str(e)}'
    return JsonResponse({
        'database_custom_connection': db_status,
        'status': 'ok' if db_status == 'ok' else 'error'
    })