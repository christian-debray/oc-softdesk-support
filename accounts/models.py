from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    can_be_contacted = models.BooleanField(blank=False, null=False, default=False)
    can_data_be_shared = models.BooleanField(blank=False, null=False, default=False)
    date_of_birth = models.DateField(blank=False, null=False)
