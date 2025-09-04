from django.urls import path
from .views import healthcheck
from .api.registeruser import register_user
from .api.authorizeuser import authorize_user
from .api.registerBooks import register_book
from .api.bookDisbursement import book_disbursement
from .api.returnBook import return_book
from .api.deleteUser import delete_user
from .api.deleteBook import delete_book

urlpatterns = [
    path('healthcheck/', healthcheck, name='healthcheck'),
    path('register-user/', register_user, name='register_user'),
    path('authorize-user/', authorize_user, name='authorize_user'),
    path('register-book/', register_book, name='register_book'),
    path('book-disbursement/', book_disbursement, name='book_disbursement'),
    path('return-book/', return_book, name='return_book'),
    path('delete-user/', delete_user, name='delete_user'),
    path('delete-book/', delete_book, name='delete_book'),
]