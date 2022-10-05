from django.urls import path
from .views import bbs
from .views import BbDetailView

urlpatterns = [
    path('bbs/<int:pk>/', BbDetailView.as_view()),
    path('bbs/', bbs),
]
