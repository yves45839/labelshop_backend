from django.urls import path
from .views import register_user, login_user, logout_user, cancel_account, verify_otp_view

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('cancel/', cancel_account, name='cancel_account'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
]
