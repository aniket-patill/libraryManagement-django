from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from librarymanager.database.create_connection import get_db_connection

@csrf_exempt
@require_POST
def delete_book(request):
    book_title = request.POST.get('book_title')

    if not book_title:
        return JsonResponse({'error': 'book_title is required.'}, status=400)

    conn = get_db_connection()
    if not conn:
        return JsonResponse({'error': 'Database connection error.'}, status=500)

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Book WHERE title=%s", (book_title,))
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        if affected:
            return JsonResponse({'message': 'Book deleted successfully.'}, status=200)
        else:
            return JsonResponse({'error': 'Book not found.'}, status=404)
    except Exception as e:
        if conn:
            conn.close()
        return JsonResponse({'error': str(e)}, status=500)