# from rest_framework import permissions


# class Admin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return bool(request.user.is_superuser)


# class StaffUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if not request.user.is_staff:
#             return False

#         allowed_views = [
#             'author_list', 'author_create', 'get_author', 'update_author', 'delete_author', 'book_list', 'book_create', 'get_book', 'update_book', 'delete_book', 
#         ]
#         return allowed_views


# class RegularUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if not request.user or not request.user.is_authenticated:
#             return False
#         if request.user.is_staff or request.user.is_superuser:
#             return False
#         allowed_views = ['borrow_book', 'return_book']
#         return  allowed_views

from rest_framework import permissions

class Admin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True

class StaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if  request.user.is_staff:
            return True

class RegularUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True