import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from librarymanager.database.create_connection import get_db_connection

@csrf_exempt
@require_POST
def register_user(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    if not name or not email or not password:
        return JsonResponse({'error': 'Name, email, and password are required.'}, status=400)
    
    conn = get_db_connection()
    if not conn:
        return JsonResponse({'error': 'Database connection error.'}, status=500)
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM User WHERE email=%s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return JsonResponse({'error': 'Email already registered.'}, status=400)
        
        cursor.execute(
            "INSERT INTO User (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return JsonResponse({'id': user_id, 'name': name, 'email': email},message='User registered successfully.', status=201)
    except Exception as e:
        if conn:
            conn.close()
        return JsonResponse({'error': str(e)}, status=500)
