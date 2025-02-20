from django.urls import path
from . import views

urlpatterns = [
    path('health_dataform/', views.health_form, name='health_dataform'),
    path('dashboard/<str:token>/', views.dashboard, name='dashboard'),
    path('all_messages/', views.all_messages, name='all_messages'),
    path('all_submissions/', views.all_submisions, name='all_submissions'),
    path('form_details/<int:id>/', views.form_details, name='form_details'),
    path('admin/message/<int:id>/', views.Admin_message_view, name='Admin_message_view'),
    path('messages/<str:token>/', views.user_message_view, name='messages'),
    path('invalid_token_url/', views.expired_view, name='invalid_token_url'),
    path('message_sent_successfully/', views.success, name='success_url'),
    
]