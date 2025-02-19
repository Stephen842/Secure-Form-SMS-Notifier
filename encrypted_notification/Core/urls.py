from django.urls import path
from . import views

urlpatterns = [
    path('health_dataform/', views.health_form, name='health_dataform'),
    path('dashboard/<str:token>/', views.dashboard, name='dashboard'),
    path('messages/<str:token>/', views.message_view, name='messages'),
    path('invalid_token_url/', views.expired_view, name='invalid_token_url'),
    path('message_sent_successfully/', views.success, name='success_url'),
    
]