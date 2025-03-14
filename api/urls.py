from django.urls import path
from .views import *

urlpatterns = [
    # Authentication URLs
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    
    # Author URLs
    path('authors/create/', AuthorCreateAPIView.as_view(), name='author-create'),
    path('authors/', AuthorListAPIView.as_view(), name='author-list'),
    path('authors/<int:id>/', AuthorDetailAPIView.as_view(), name='author-detail'),
    path('authors/<int:id>/update/', AuthorUpdateAPIView.as_view(), name='author-update'),
    path('authors/<int:id>/delete/', AuthorDeleteAPIView.as_view(), name='author-delete'),
    
    # Book URLs
    path('books/create/', BookCreateAPIView.as_view(), name='book-create'),
    path('books/', BookListAPIView.as_view(), name='book-list'),
    path('books/<int:id>/', BookDetailAPIView.as_view(), name='book-detail'),
    path('books/<int:id>/update/', BookUpdateAPIView.as_view(), name='book-update'),
    path('books/<int:id>/delete/', BookDeleteAPIView.as_view(), name='book-delete'),
    
    # Borrowing URLs
    path('books/borrow/', BorrowBookAPIView.as_view(), name='borrow-book'),
    path('books/return/', ReturnBookAPIView.as_view(), name='borrower-return'),
    
    # Search and Statistics URLs
    path('search-filter/', BookSearchAPIView.as_view(), name='book-search'),
    path('library/statistics/', LibraryStatisticsAPIView.as_view(), name='library-statistics'),
    path('borrowers/', BorrowerListAPIView.as_view(), name='borrower-list'),
]