import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from librarymanager.database.create_connection import get_db_connection

@csrf_exempt
@require_POST
def book_disbursement(request):
    user_name = request.POST.get('user_name')
    user_email = request.POST.get('user_email')
    book_title = request.POST.get('book_title')

    if not user_name or not user_email or not book_title:
        return JsonResponse({'error': 'user_name, user_email, and book_title are required.'}, status=400)

    conn = get_db_connection()
    if not conn:
        return JsonResponse({'error': 'Database connection error.'}, status=500)

    try:
        cursor = conn.cursor()
        # Get user id
        cursor.execute("SELECT id FROM User WHERE name=%s AND email=%s", (user_name, user_email))
        user = cursor.fetchone()
        if not user:
            cursor.close()
            conn.close()
            return JsonResponse({'error': 'User not found.'}, status=404)
        user_id = user[0]

        # Get book id and availability
        cursor.execute("SELECT id, available FROM Book WHERE title=%s", (book_title,))
        book = cursor.fetchone()
        if not book:
            cursor.close()
            conn.close()
            return JsonResponse({'error': 'Book not found.'}, status=404)
        book_id, available = book
        if not available:
            cursor.close()
            conn.close()
            return JsonResponse({'error': 'Book is not available.'}, status=400)

        # Insert into Rental
        cursor.execute(
            "INSERT INTO Rental (user_id, book_id) VALUES (%s, %s)",
            (user_id, book_id)
        )
        # Update book availability
        cursor.execute(
            "UPDATE Book SET available=%s WHERE id=%s",
            (False, book_id)
        )
        conn.commit()
        rental_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return JsonResponse({
            'rental_id': rental_id,
            'user_id': user_id,
            'book_id': book_id,
            'message': 'Book rented successfully.'
        }, status=201)
    except Exception as e:
        if conn:
            conn.close()
        return JsonResponse({'error': str(e)}, status=500)