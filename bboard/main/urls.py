from django.urls import path
from .views import index
from .views import other_page
from .views import BbLoginView

app_name = 'main'
urlpatterns = [
    path('accounts/login/', BbLoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]
