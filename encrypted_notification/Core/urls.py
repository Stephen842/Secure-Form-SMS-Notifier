from django.urls import path
from . import views

urlpatterns = [
    path('Health-DataForm/', views.health_form, name='Health-DataForm'),
    path('Dashboard/<str:token>/', views.dashboard, name='dashboard'),
    path('messages/<str:token>/', views.message_view, name='messages'),
]