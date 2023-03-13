from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView, Response, Request, status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from django.shortcuts import get_object_or_404
from .serializers import AccountSerializer
from copies.serializers import LoanSerializer
from .models import Account
from copies.models import Copy, Loan
from .permissions import CreateUserOrIsColaborator, IsOwnerOrColaborator
from drf_spectacular.utils import extend_schema
import ipdb

from datetime import timedelta, datetime


from django.core.mail import send_mail
from django.conf import settings


class AccountView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CreateUserOrIsColaborator]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @extend_schema(
        operation_id="follow_create",
        request=AccountSerializer,
        responses={201: AccountSerializer},
        description="Rota para listar os usuários",
        summary="Listar usuários",
        tags=["Accounts"],
    )
    def get(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        operation_id="follow_create",
        request=AccountSerializer,
        responses={201: AccountSerializer},
        description="Rota para criar um usuário",
        summary="Criar usuário",
        tags=["Accounts"],
    )
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AccountDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrColaborator]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    lookup_url_kwarg = "account_id"

    @extend_schema(
        operation_id="follow_create",
        request=AccountSerializer,
        responses={201: AccountSerializer},
        description="Rota para listar um usuário com base no UUID",
        summary="Listar usuário específico",
        tags=["Accounts"],
    )
    def get(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        operation_id="follow_create",
        request=AccountSerializer,
        responses={201: AccountSerializer},
        description="Rota para atualizar os usuários",
        summary="Atualização de usuários",
        tags=["Accounts"],
    )
    def put(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        operation_id="follow_create",
        request=AccountSerializer,
        responses={201: AccountSerializer},
        description="Rota para atualizar um usuário com base no UUID",
        summary="Atualizar um usuário específico",
        tags=["Accounts"],
    )
    def patch(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @extend_schema(
        operation_id="follow_create",
        request=AccountSerializer,
        responses={201: AccountSerializer},
        description="Rota para deleção de usuário com base no UUID",
        summary="Deleção de usuário",
        tags=["Accounts"],
    )
    def delete(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class AccountStatusDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrColaborator]

    def get(self, request, account_id):
        find_account = get_object_or_404(Account, pk=account_id)

        serializer = AccountSerializer(find_account)

        return Response(serializer.data, 200)


class AccountLoanView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def create(self, request, *args, **kwargs):
        account_id = kwargs["account_id"]
        book_id = kwargs["book_id"]

        avaliable_copies = Copy.objects.filter(
            book_id=book_id, is_avaliable=True
        ).first()

        if avaliable_copies is None:
            return Response({"message": "No copy avaliable"})

        avaliable_copies.is_avaliable = False

        deliver = datetime.now() + timedelta(days=7)

        loan = Loan(
            account_id=account_id,
            copy=avaliable_copies,
            deliver_in=deliver,
        )

        avaliable_copies.last_loan = datetime.now()
        avaliable_copies.save()
        loan.save()

        serializer = LoanSerializer(loan)
        return Response(serializer.data, 201)


class AccountDeliveryView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        copy_id = self.kwargs["copy_id"]

        user_loan = Loan.objects.filter(account=request.user, copy_id=copy_id).first()

        if user_loan is None:
            return Response(
                {"message": "Loan not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if not user_loan.is_active:
            return Response(
                {"message": "Copy already returned"}, status=status.HTTP_409_CONFLICT
            )

        today_date = datetime.now()

        user_loan.delivery_at = today_date
        user_loan.is_active = False
        user_loan.save()

        copy = Copy.objects.get(pk=copy_id)
        copy.is_avaliable = True
        copy.save()

        serializer = LoanSerializer(user_loan)

        followers = user_loan.copy.book.followers

        emails = [account.email for account in followers.all()]

        send_mail(
            subject="Sua cópia está disponível!",
            message=f'Olá !\n\nSua cópia do livro "{user_loan.copy.book.title}" está disponível para retirada.\n\nObrigado por utilizar nossa biblioteca!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=emails,
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountLoansDetailView(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrColaborator]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    lookup_url_kwarg = "account_id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data["loans"])
