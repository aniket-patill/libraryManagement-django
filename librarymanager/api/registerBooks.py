import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from librarymanager.database.create_connection import get_db_connection

@csrf_exempt
@require_POST
def register_book(request):
    title = request.POST.get('title')
    author = request.POST.get('author')

    if not title or not author:
        return JsonResponse({'error': 'Title and author are required.'}, status=400)
    
    conn = get_db_connection()
    if not conn:
        return JsonResponse({'error': 'Database connection error.'}, status=500)
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Book (title, author, available) VALUES (%s, %s, %s)",
            (title, author, True)
        )
        conn.commit()
        book_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return JsonResponse({'id': book_id, 'title': title, 'author': author, 'message': 'Book registered successfully.'}, status=201)
    except Exception as e:
        if conn:
            conn.close()
        return JsonResponse({'error': str(e)}, status=500)