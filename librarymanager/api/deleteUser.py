from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from librarymanager.database.create_connection import get_db_connection

@csrf_exempt
@require_POST
def delete_user(request):
    user_name = request.POST.get('user_name')
    user_email = request.POST.get('user_email')
    password = request.POST.get('password')

    if not user_name or not user_email or not password:
        return JsonResponse({'error': 'user_name, user_email, and password are required.'}, status=400)

    conn = get_db_connection()
    if not conn:
        return JsonResponse({'error': 'Database connection error.'}, status=500)

    try:
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM User WHERE name=%s AND email=%s AND password=%s",
            (user_name, user_email, password)
        )
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        if affected:
            return JsonResponse({'message': 'User deleted successfully.'}, status=200)
        else:
            return JsonResponse({'error': 'User not found or password incorrect.'}, status=404)
    except Exception as e:
        if conn:
            conn.close()
        return JsonResponse({'error': str(e)}, status=500)