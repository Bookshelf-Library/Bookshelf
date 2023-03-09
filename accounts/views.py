from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from .serializers import AccountSerializer
from .models import Account
from .permissions import CreateUserOrIsColaborator, IsOwnerOrColaborator


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


class AccountLoansDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrColaborator]

    def get(self, request, account_id):
        find_account = get_object_or_404(Account, pk=account_id)

        serializer = AccountSerializer(find_account)

        return Response(serializer.data["loans"], 200)