from django.urls import path
from .views import CopiesDetailView, CopyDeliveryView

urlpatterns = [
    path("books/<str:book_id>/copies/<int:copies_qtd>/", CopiesDetailView.as_view()),
    path("users/copy/<str:copy_id>/", CopyDeliveryView.as_view()),
]
