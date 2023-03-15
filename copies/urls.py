from django.urls import path
from .views import CopiesDetailView

urlpatterns = [
    path("books/<str:book_id>/copies/<int:copies_qtd>/", CopiesDetailView.as_view()),
]
