from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    hospital = models.CharField(max_length=200,help_text="current hospital or clinic", blank=False)

    def __str__(self):
        return self.first_name
    