from django import forms
from .models import Health, Reply

class HealthForm(forms.ModelForm):
    class Meta:
        model = Health
        fields = '__all__'

class AdminReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['message', 'file']

class UserReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['message', 'file']