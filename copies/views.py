from rest_framework import generics
from rest_framework.views import Response, status
from books.permissions import BookPermission
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from books.models import Book
from accounts.models import Account
from .models import Copy
from .serializers import CopySerializer
#from django.core.mail import send_mall
#from django.conf import settings
#import ipdb


class CopiesDetailView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [BookPermission]

    def create(self, request, *args, **kwargs):
        book_id = kwargs["book_id"]
        copies_qtd = kwargs["copies_qtd"]

        find_book = get_object_or_404(Book, pk=book_id)

        data = [Copy(book=find_book) for _ in range(copies_qtd)]
        Copy.objects.bulk_create(data)

        serializer = CopySerializer(data, many=True)

        return Response(serializer.data, 201)


class CopyDeliveryView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]

    def update(self, request, *args, **kwargs):
        copy_id = self.kwargs["copy_id"]
        copy = get_object_or_404(Copy, pk=copy_id)

        # Verifica se a cópia já foi entregue
        if copy.is_avaliable:
            return Response({"message": "This copy has already been delivered"},
                status=status.HTTP_400_BAD_REQUEST)

        # Atualiza o estado da cópia para "entregue"
        copy.is_delivered = True
        copy.is_avaliable = True
        copy.save()

        serializer = CopySerializer(copy)

        
        # Cria o objeto EmailMessage com as informações do email
        #subject = "Sua cópia está disponível!"
        #message = f'Olá {request.user.username},\n\nSua cópia do livro "{copy.book.title}" está disponível para retirada.\n\nObrigado por utilizar nossa biblioteca!'
        #email_from = settings.EMAIL_HOST_USER
        #email_to = [request.user.email]
        #email = EmailMessage(subject, message, email_from, email_to)

        # Envia o email
        #ipdb.set_trace()
        #email.send()

        return Response(serializer.data, status=status.HTTP_200_OK)
