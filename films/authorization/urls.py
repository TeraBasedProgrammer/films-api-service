from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import register

urlpatterns = [
    path('register/', register, name='registration'),
    path('login/', TokenObtainPairView.as_view(), name='tokem_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]