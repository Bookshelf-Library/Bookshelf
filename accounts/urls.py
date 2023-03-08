from django.urls import path
from .views import AccountView, AccountDetailView, AccountStatusDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("users/", AccountView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("users/<str:account_id>/", AccountDetailView.as_view()),
    path("users/<str:account_id>/status/", AccountStatusDetailView.as_view())
]
