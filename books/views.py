from rest_framework import generics, status
from .models import Book, Follow
from .serializers import BookSerializer, FollowSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import BookPermission
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        find_account = Book.objects.filter(account=request.user)
        if find_account:
            return Response({"message": "user is already following this book"}, status=400)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        primary_key = self.kwargs["book_id"]
        book = get_object_or_404(Book, pk=primary_key)
        serializer.save(account=self.request.user, book=book)
