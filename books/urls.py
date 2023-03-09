from django.urls import path
from .views import ListCreateBooks, FollowBook, FollowDetailView

urlpatterns = [
    path("books/", ListCreateBooks.as_view()),
    path("users/follow/<str:book_id>/", FollowBook.as_view()),
    path("users/unfollow/<str:book_id>/", FollowDetailView.as_view()),
]
