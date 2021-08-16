from django.urls import path

from .views import *



app_name = 'main'

urlpatterns = [
    path('', index, name='index'),
    path('<str:page>', other_page, name='other'),
    path('accounts/login/', BBLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change/', ChangeUserInfoViwe.as_view(), name='profile_change'),
    path('accounts/password/change/', BBPasswordChangeView.as_view(), name='password_change'),
    path('accounts/register/done/', RegisterDoneViwe.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserViwe.as_view(), name='register'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/logout/', BBLogoutView.as_view(), name='logout'),
]