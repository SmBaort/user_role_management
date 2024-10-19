from django.db import models
from django.utils import timezone

class Role(models.Model):
    roleName = models.CharField(max_length=100, unique=True)
    accessModules = models.JSONField(default=list)
    createdAt = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.roleName


class User(models.Model):
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.firstName + self.lastName
