from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView, Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from django.shortcuts import get_object_or_404
from .serializers import AccountSerializer
from copies.serializers import LoanSerializer
from .models import Account
from copies.models import Copy, Loan
from .permissions import CreateUserOrIsColaborator, IsOwnerOrColaborator
import ipdb

from datetime import timedelta, datetime


class AccountView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CreateUserOrIsColaborator]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrColaborator]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    lookup_url_kwarg = "account_id"


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
