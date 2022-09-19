from django.urls import path
from .views import index
from .views import other_page
from .views import BbLoginView
from .views import profile
from .views import BbLogoutView
from .views import ChangeInfoViewUser
from .views import BbPasswordChangeView
from .views import RegisterViewUser,RegisterViewDone
from .views import user_activate
from .views import DeleteViewUser
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordResetCompleteView

app_name = 'main'
urlpatterns = [
    path('accounts/register/activate/<str:sign>/',user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterViewDone.as_view(),name = 'register_done'),
    path('accounts/register/', RegisterViewUser.as_view(),name='register'),
    path('accounts/profile/delete/',DeleteViewUser.as_view(),name= 'profile_delete'),
    path('accounts/profile/change/', ChangeInfoViewUser.as_view(), name='profile_change'),
    path('accounts/logout/', BbLogoutView.as_view(), name='logout'),
    path('accounts/password/change/',BbPasswordChangeView.as_view(),name='password_change'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', BbLoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
    path('accounts/password_reset/',PasswordResetView.as_view(
        template_name='registration/reset_password.html',
        subject_template_name='registration/reset_subject.txt',
        email_template_name='registration/reset_email.txt'),
         name='reset_password'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(
             template_name='registration/confirm_password.html'),
         name='password_reset_confirm'),
    path('accounts/reset/done/',PasswordResetCompleteView.as_view(
             template_name='registration/password_confirmed.html'),
         name='password_reset_complete'),
    ]
