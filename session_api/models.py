from django.db import models

# Create your models here.
from django.utils import timezone
from datetime import datetime, timedelta

from session_api.generators import generate_client_id, generate_client_secret

class session_client_data(models.Model):
    """ untuk menyimpan client id dan secret untuk custom session."""
    client_id = models.CharField(
        max_length=100, unique=True, default=generate_client_id, db_index=True
    )
    client_secret = models.CharField(
        max_length=100, unique=True, default=generate_client_id, db_index=True
    )
    activate = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.client_id

class AuthToken(models.Model):
    access_token = models.CharField(max_length=100, unique=True)
    refresh_token = models.CharField(max_length=100, unique=True)
    expiry_date = models.DateTimeField()
    refresh_token_expiry = models.DateTimeField()
    expired = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    session_application = models.OneToOneField(
        session_client_data, on_delete=models.CASCADE, related_name="session_data_client", primary_key=True
    )
    def __str__(self):
        return self.access_token
