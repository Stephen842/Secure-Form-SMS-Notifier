from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.crypto import get_random_string
from cryptography.fernet import Fernet
from django.conf import settings
from encrypted_model_fields.fields import EncryptedTextField
# Create your models here.

# To Load my encryption key from settings
ENCRYPTION_KEY = settings.FIELD_ENCRYPTION_KEY

# To initialize Fernet encryption with the key
cipher_suite = Fernet(ENCRYPTION_KEY)

class Health(models.Model):
    SYMPTOM_ONSET_CHOICES = [
        ('sudden', 'Sudden'),
        ('gradual', 'Gradual'),
    ]

    SYMPTOM_PATTERN_CHOICES = [
        ('constant', 'Constant'),
        ('waves', 'Comes in Waves'),
    ]

    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = PhoneNumberField(region='US')     
    symptom = models.TextField()
    onset = models.CharField(max_length=20, choices=SYMPTOM_ONSET_CHOICES)
    duration = models.CharField(max_length=100)
    worse_factors = models.TextField(verbose_name='Things that make it worse')
    better_factors = models.TextField(verbose_name='Things that make it better')
    pattern = models.CharField(max_length=20, choices=SYMPTOM_PATTERN_CHOICES)
    possible_cause = models.TextField(verbose_name="Any idea what could be causing it", blank=True, null=True)
    concerns = models.TextField(verbose_name="Any specific concerns about the symptoms", blank=True, null=True)
    doctor_expectation = models.TextField(verbose_name="What expectation do you want your family doctor to meet?")
    medication_allergy = models.TextField(verbose_name="Do you have any medication allergy?", blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    # Fields for encrypted URL
    encrypted_url = models.CharField(max_length=255, blank=True, null=True)
    access_attempts = models.IntegerField(default=20, blank=True, null=True)

    def generate_encrypted_url(self):
        # To generate a unique encrypted url
        unique_token = get_random_string(32)
        encrypted_token = cipher_suite.encrypt(unique_token.encode()).decode()
        self.encrypted_url = encrypted_token
        self.access_attempts = 20
        self.save()
        return encrypted_token 
    
    def get_decrypted_url(self):
        # Decrypt the encrypted URL
        if self.encrypted_url:
            decrypted_token = cipher_suite.decrypt(self.encrypted_url.encode()).decode()
            return decrypted_token
        return None

    def __str__(self):
        return f'Health Form -{self.name} ({self.submitted_at})'
    
    class Meta:
        verbose_name_plural = 'Health Form'
    
class Reply(models.Model):
    # Model for storing messages between admin and users.
    health = models.ForeignKey(Health, on_delete=models.CASCADE, related_name='replies')
    message = models.TextField()
    file = models.FileField(upload_to='uploads/', null=True, blank=True)  # File upload support
    sender_type = models.CharField(
        max_length=50,
        choices=[('admin', 'Admin'), ('user', 'User')],
        default='admin'
    )
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    encrypted_reply_url = models.CharField(max_length=255, blank=True, null=True)
    reply_attempts = models.IntegerField(default=20)

    def generate_encrypted_reply_url(self):
        # To generate a unique encrypted url for the reply
        unique_token = get_random_string(32)
        encrypted_token = cipher_suite.encrypt(unique_token.encode()).decode()
        self.encrypted_reply_url = encrypted_token
        self.reply_attempts = 20
        self.save()
        return encrypted_token
    
    def get_decrypted_reply_url(self):
        # Decrypt the encrypted reply URL
        if self.encrypted_reply_url:
            decrypted_token = cipher_suite.decrypt(self.encrypted_reply_url.encode()).decode()
            return decrypted_token
        return None
    
    def __str__(self):
        return f'Reply by {self.sender_type} to {self.health.name} - {self.created_at}'

    class Meta:
        verbose_name_plural = 'Messages'

"""
Run the following on the python shell to generate your secure key and make sure to store in .env, before calling it via settings

from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())

This will give you a random 32-byte string. Copy this value and add to your .env or settings.py
"""