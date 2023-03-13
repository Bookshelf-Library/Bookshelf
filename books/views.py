from rest_framework import generics, status
from .models import Book, Follow
from .serializers import BookSerializer, FollowSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import BookPermission
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class FollowBook(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    @extend_schema(
        operation_id="follow_create",
        request=FollowSerializer,
        responses={201: FollowSerializer},
        description="Rota para seguir um livro",
        summary="Seguir um livro",
        tags=["Follow"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        find_account = Book.objects.filter(account=request.user)
        if find_account:
            return Response(
                {"message": "user is already following this book"}, status=400
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        primary_key = self.kwargs["book_id"]
        book = get_object_or_404(Book, pk=primary_key)
        serializer.save(account=self.request.user, book=book)


class FollowDetailView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    lookup_url_kwarg = "book_id"

    @extend_schema(
        operation_id="follow_create",
        request=FollowSerializer,
        responses={201: FollowSerializer},
        description="Rota para deixar de seguir um livro",
        summary="Parar de seguir o livro",
        tags=["Follow"],
    )
    def delete(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ListCreateBooks(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [BookPermission]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @extend_schema(
        operation_id="books_list",
        request=BookSerializer,
        responses={201: BookSerializer},
        description="Rota para criação de livros",
        summary="Listagem de livros",
        tags=["Books"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @extend_schema(
        operation_id="books_post",
        request=BookSerializer,
        responses={201: BookSerializer},
        description="Rota para criação de livros",
        summary="Criação de livros",
        tags=["Books"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
