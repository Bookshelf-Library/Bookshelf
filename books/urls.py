from django.contrib import admin
from django.urls import path
from .views import ListCreateBooks, FollowBook

urlpatterns = [
    path("admin/", admin.site.urls),
    path("books/", ListCreateBooks.as_view()),
    path("users/follow/<str:book_id>/", FollowBook.as_view())
]
