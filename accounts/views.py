from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
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
