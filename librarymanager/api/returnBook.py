import os
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from librarymanager.database.create_connection import get_db_connection

@csrf_exempt
@require_POST
def return_book(request):
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

        # Get book id
        cursor.execute("SELECT id FROM Book WHERE title=%s", (book_title,))
        book = cursor.fetchone()
        if not book:
            cursor.close()
            conn.close()
            return JsonResponse({'error': 'Book not found.'}, status=404)
        book_id = book[0]

        # Check if rental exists and not yet returned
        cursor.execute(
            "SELECT id FROM Rental WHERE user_id=%s AND book_id=%s AND returned_at IS NULL",
            (user_id, book_id)
        )
        rental = cursor.fetchone()
        if not rental:
            cursor.close()
            conn.close()
            return JsonResponse({'error': 'No active rental found for this user and book.'}, status=400)
        rental_id = rental[0]

        # Update rental with return date
        return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "UPDATE Rental SET returned_at=%s WHERE id=%s",
            (return_date, rental_id)
        )
        # Update book availability
        cursor.execute(
            "UPDATE Book SET available=%s WHERE id=%s",
            (True, book_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return JsonResponse({
            'rental_id': rental_id,
            'user_id': user_id,
            'book_id': book_id,
            'returned_at': return_date,
            'message': 'Book returned successfully.'
        }, status=200)
    except Exception as e:
        if conn:
            conn.close()
        return JsonResponse({'error': str(e)}, status=500)