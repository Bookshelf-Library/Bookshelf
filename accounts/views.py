from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    RetrieveAPIView,
)
from django.shortcuts import get_object_or_404
from .serializers import AccountSerializer
from .models import Account
from .permissions import CreateUserOrIsColaborator, IsOwnerOrColaborator
from drf_spectacular.utils import extend_schema


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
