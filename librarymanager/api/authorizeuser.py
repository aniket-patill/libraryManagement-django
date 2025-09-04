import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from librarymanager.database.create_connection import get_db_connection

@csrf_exempt
@require_POST
def authorize_user(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    if not email or not password:
        return JsonResponse({'error': 'Email and password are required.'}, status=400)
    
    conn = get_db_connection()
    if not conn:
        return JsonResponse({'error': 'Database connection error.'}, status=500)
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name FROM User WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return JsonResponse({'id': user[0], 'name': user[1], 'email': email, 'message': 'Login successful.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid email or password.'}, status=401)
    except Exception as e:
        if conn:
            conn.close()
        return JsonResponse({'error': str(e)}, status=500)