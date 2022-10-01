from django.urls import path
from .views import index
from .views import other_page
from .views import BbLoginView
from .views import profile
from .views import BbLogoutView
from .views import ChangeInfoViewUser
from .views import BbPasswordChangeView
from .views import RegisterViewUser, RegisterViewDone
from .views import user_activate
from .views import DeleteViewUser
from .views import PasswordViewReset
from .views import PasswordResetViewDone
from .views import PasswordResetViewConfirm
from .views import PasswordResetViewComplete
from .views import by_rubric
from .views import detail
from .views import profile_bb_detail

app_name = 'main'
urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterViewDone.as_view(), name='register_done'),
    path('accounts/register/', RegisterViewUser.as_view(), name='register'),
    path('accounts/profile/delete/', DeleteViewUser.as_view(), name='profile_delete'),
    path('accounts/profile/change/', ChangeInfoViewUser.as_view(), name='profile_change'),
    path('accounts/logout/', BbLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', BbPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/<int:pk>/',profile_bb_detail, name ='profile_bb_detail'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', BbLoginView.as_view(), name='login'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
    path('accounts/password_reset/', PasswordViewReset.as_view(), name='reset_password'),
    path('accounts/password_reset/done/', PasswordResetViewDone.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetViewConfirm.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetViewComplete.as_view(), name='password_reset_complete'),
]
