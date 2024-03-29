# Rest_Framework
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

# Models
from .models import Account
from copies.models import Copy, Loan

# Serializers
from .serializers import AccountSerializer
from copies.serializers import LoanSerializer

# Custom Permissions
from .permissions import CreateUserOrIsColaborator, IsOwnerOrColaborator

# Utility Functions
from .utils import permission_to_loan, openingtime, remove_punishment

# Django
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

# DRF Spectacular
from drf_spectacular.utils import extend_schema

# Datetime
from datetime import timedelta, datetime

# APScheculer
from apscheduler.schedulers.background import BackgroundScheduler


class AccountView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CreateUserOrIsColaborator]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    @extend_schema(
        operation_id="follow_create",
        request=AccountSerializer,
        responses={200: AccountSerializer},
        description="Rota para listar os usuários",
        summary="Listar usuários",
        tags=["Accounts"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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
        responses={200: AccountSerializer},
        description="Rota para listar um usuário com base no UUID",
        summary="Listar usuário específico",
        tags=["Accounts"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="follow_create",
        request=AccountSerializer,
        responses={200: AccountSerializer},
        description="Rota para atualizar os usuários",
        summary="Atualização de usuários",
        tags=["Accounts"],
    )
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @extend_schema(
        operation_id="follow_create",
        request=AccountSerializer,
        responses={200: AccountSerializer},
        description="Rota para atualizar um usuário com base no UUID",
        summary="Atualizar um usuário específico",
        tags=["Accounts"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="follow_create",
        request=AccountSerializer,
        responses={204: AccountSerializer},
        description="Rota para deleção de usuário com base no UUID",
        summary="Deleção de usuário",
        tags=["Accounts"],
    )
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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
        current_date = datetime.now()
        current_day = current_date.strftime("%A")
        current_time = current_date.strftime("%H")
        is_working = openingtime(current_day, current_time)

        if not is_working:
            return Response(
                {
                    "message": "The library is currently not open. Opening hours: 9am - 6pm Monday to Friday"
                },
                status.HTTP_401_UNAUTHORIZED,
            )

        allowed_to_loan = permission_to_loan(
            account_id=account_id, Loan=Loan, current_date=current_date
        )

        if not allowed_to_loan:
            return Response(
                {"message": "Not allowed to loan. Check loans from this account."},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )

        avaliable_copies = Copy.objects.filter(
            book_id=book_id, is_avaliable=True
        ).first()

        if avaliable_copies is None:
            return Response(
                {"message": "No copy avaliable"}, status=status.HTTP_404_NOT_FOUND
            )

        avaliable_copies.is_avaliable = False

        deliver = current_date + timedelta(seconds=7)

        loan = Loan(
            account_id=account_id,
            copy=avaliable_copies,
            deliver_in=deliver,
        )

        avaliable_copies.last_loan = current_date
        avaliable_copies.save()
        loan.save()

        serializer = LoanSerializer(loan)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AccountDeliveryView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        copy_id = self.kwargs["copy_id"]

        user_loan = Loan.objects.filter(
            account=request.user, copy_id=copy_id, delivery_at=None
        ).first()

        if user_loan is None:
            return Response(
                {"message": "Loan not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if not user_loan.is_active:
            return Response(
                {"message": "Copy already returned"}, status=status.HTTP_409_CONFLICT
            )

        current_date = datetime.now()

        account: Account = request.user
        allowed_to_loan = permission_to_loan(
            account_id=account.id, Loan=Loan, current_date=current_date
        )

        if not allowed_to_loan and not account.punishment:
            account.punishment = datetime.now() + timedelta(days=2)
            account.save()

            scheduler = BackgroundScheduler()
            scheduler.add_job(remove_punishment, "interval", days=2, args=[account])
            scheduler.start()

        user_loan.delivery_at = current_date
        user_loan.is_active = False
        user_loan.save()

        serializer = LoanSerializer(user_loan)

        copy = Copy.objects.get(pk=copy_id)
        copy.is_avaliable = True
        copy.save()

        followers = user_loan.copy.book.followers

        emails = [account.email for account in followers.all()]

        if emails:
            send_mail(
                subject="Sua cópia está disponível!",
                message=f'Olá !\n\nSua cópia do livro "{user_loan.copy.book.title}" está disponível para retirada.\n\nObrigado por utilizar nossa biblioteca!',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=emails,
                fail_silently=True,
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
