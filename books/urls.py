from django.urls import path
from .views import ListCreateBooks, FollowBook

urlpatterns = [
    path("books/", ListCreateBooks.as_view()),
    path("users/follow/<str:book_id>/", FollowBook.as_view())
]
