from rest_framework import generics
from .models import Book, Follow
from .serializers import BookSerializer, FollowSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import BookPermission
from django.shortcuts import get_object_or_404


class ListCreateBooks(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [BookPermission]
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class FollowBook(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        primary_key = self.kwargs["book_id"]
        book = get_object_or_404(Book, pk=primary_key)
        serializer.save(account=self.request.user, book=book)
