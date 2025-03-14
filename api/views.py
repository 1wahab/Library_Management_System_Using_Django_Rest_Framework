from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny  # Explicit import
from .models import *
from .serializers import *
from .permissions import *
from django.utils import timezone
from django.db.models import Q
from django.core.cache import cache

# Authentication Views

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user': serializer.data, 'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = RefreshToken.for_user(user)
            user_data = UserRegisterSerializer(user).data
            return Response(
                {'message': 'Login successful', 'user_data': user_data, 'token': {
                    'refresh': str(token),
                    'access': str(token.access_token),
                }},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Author Management Views

class AuthorCreateAPIView(APIView):
    permission_classes = [StaffUser]
    
    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Author created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AuthorListAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Check cache first
        cached_data = cache.get('author_list')
        if cached_data:
            return Response(cached_data)
            
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        response_data = serializer.data
        
        # Cache the response for 15 minutes
        cache.set('author_list', response_data, 60*15)
        return Response(response_data)

class AuthorDetailAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, id):
        try:
            author = Author.objects.get(pk=id)
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        except Author.DoesNotExist:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

class AuthorUpdateAPIView(APIView):
    permission_classes = [StaffUser]
    
    def put(self, request, id):
        try:
            author = Author.objects.get(pk=id)
            serializer = AuthorSerializer(author, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Author updated successfully!', 'data': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Author.DoesNotExist:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

class AuthorDeleteAPIView(APIView):
    permission_classes = [StaffUser]
    
    def delete(self, request, id):
        try:
            author = Author.objects.get(pk=id)
            author.delete()
            return Response({'message': 'Author deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Author.DoesNotExist:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)

# Book Management Views

class BookCreateAPIView(APIView):
    permission_classes = [StaffUser]
    
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Book created successfully!', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookListAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Check cache first
        cached_data = cache.get('book_list')
        if cached_data:
            return Response(cached_data)
            
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        response_data = serializer.data
        
        # Cache the response for 15 minutes
        cache.set('book_list', response_data, 60*15)
        return Response(response_data)

class BookDetailAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, id):
        try:
            book = Book.objects.get(pk=id)
            serializer = BookSerializer(book)
            return Response(serializer.data)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

class BookUpdateAPIView(APIView):
    permission_classes = [StaffUser]
    
    def put(self, request, id):
        try:
            book = Book.objects.get(pk=id)
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Book updated successfully!', 'data': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

class BookDeleteAPIView(APIView):
    permission_classes = [StaffUser]
    
    def delete(self, request, id):
        try:
            book = Book.objects.get(pk=id)
            book.delete()
            return Response({'message': 'Book deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

# Borrowing Operation Views

class BorrowBookAPIView(APIView):
    permission_classes = [RegularUser]
    
    def post(self, request):
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
            
        if not book.available:
            return Response({'error': 'This book is not available for borrowing'}, status=status.HTTP_400_BAD_REQUEST)
            
        borrower = request.user.borrower
        if borrower.books_borrowed.count() >= 3:
            return Response({'error': 'You cannot borrow more than 3 books at a time'}, status=status.HTTP_400_BAD_REQUEST)
            
        borrower.books_borrowed.add(book)
        book.available = False
        book.last_borrowed_date = timezone.now()
        book.save()
        
        return Response({'message': 'Book borrowed successfully', 'book': BookSerializer(book).data}, status=status.HTTP_200_OK)

class ReturnBookAPIView(APIView):
    permission_classes = [RegularUser]
    
    def post(self, request):
        book_id = request.data.get('book_id')
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
            
        borrower = request.user.borrower
        if book not in borrower.books_borrowed.all():
            return Response({'error': 'You have not borrowed this book'}, status=status.HTTP_400_BAD_REQUEST)
            
        borrower.books_borrowed.remove(book)
        book.available = True
        book.save()
        
        return Response({'message': 'Book returned successfully'}, status=status.HTTP_200_OK)

# Search and Statistics Views

class BookSearchAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Check cache first
        query_params = request.query_params
        cache_key = f'book_search_{query_params}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
            
        books = Book.objects.all()
        
        title_query = request.query_params.get('title', '')
        if title_query:
            books = books.filter(title__icontains=title_query)
            
        author_query = request.query_params.get('author', '')
        if author_query:
            books = books.filter(author__name__icontains=author_query)
            
        available_query = request.query_params.get('available')
        if available_query:
            books = books.filter(available=(available_query.lower() == 'true'))
            
        serializer = BookSerializer(books, many=True)
        response_data = serializer.data
        
        # Cache the response for 15 minutes
        cache.set(cache_key, response_data, 60*15)
        return Response(response_data)

class LibraryStatisticsAPIView(APIView):
    permission_classes = [StaffUser]
    
    def get(self, request):
        # Check cache first
        cached_data = cache.get('library_statistics')
        if cached_data:
            return Response(cached_data)
            
        total_books = Book.objects.count()
        available_books = Book.objects.filter(available=True).count()
        borrowed_books = total_books - available_books
        total_authors = Author.objects.count()
        total_borrowers = Borrower.objects.count()
        
        data = {
            'total_books': total_books,
            'available_books': available_books,
            'borrowed_books': borrowed_books,
            'total_authors': total_authors,
            'total_borrowers': total_borrowers,
        }
        
        # Cache the response for 15 minutes
        cache.set('library_statistics', data, 60*15)
        return Response(data)

class BorrowerListAPIView(APIView):
    permission_classes = [StaffUser]
    
    def get(self, request):
        # Check cache first
        cached_data = cache.get('borrower_list')
        if cached_data:
            return Response(cached_data)
            
        borrowers = Borrower.objects.filter(books_borrowed__isnull=False).distinct()
        serializer = BorrowerSerializer(borrowers, many=True)
        response_data = serializer.data
        
        # Cache the response for 15 minutes
        cache.set('borrower_list', response_data, 60*15)
        return Response(response_data)