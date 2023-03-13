from rest_framework import generics
from rest_framework.views import Response
from books.permissions import BookPermission
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from books.models import Book
from .models import Copy
from .serializers import CopySerializer
from drf_spectacular.utils import extend_schema

# Programador é quem programa


class CopiesDetailView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [BookPermission]
    serializer = [CopySerializer]

    def create(self, request, *args, **kwargs):
        book_id = kwargs["book_id"]
        copies_qtd = kwargs["copies_qtd"]

        find_book = get_object_or_404(Book, pk=book_id)

        data = [Copy(book=find_book) for _ in range(copies_qtd)]
        Copy.objects.bulk_create(data)

        serializer = CopySerializer(data, many=True)

        return Response(serializer.data, 201)

    @extend_schema(
        operation_id="copies_post",
        request=CopySerializer,
        responses={201: CopySerializer},
        description="Rota para criação de copias",
        summary="Rota para criação de copias",
        tags=["Copias"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
