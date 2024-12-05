from django.db import models
from accounts.models import User


class Contributor(models.Model):
    user = models.OneToOneField(to=User, to_field="username", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    class ProjectType(models.TextChoices):
        BACKEND = "BACKEND", "Backend"
        FRONTEND = "FRONTEND", "Frontend"
        IOS = "IOS", "iOS"
        ANDROID = "ANDROID", "Android"

    name = models.CharField(max_length=128, unique=True, null=False, blank=False)
    type = models.CharField(choices=ProjectType, null=False, blank=False, max_length=8)
    description = models.TextField(null=False, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)
