from django.db import models

# Create your models here.
from django.db import models
from rest_framework_simple_api_key.models import AbstractAPIKey
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone
from main.lib.age import age
from shopbot.settings import ROOT
from django.forms.models import model_to_dict
import uuid
from django.utils.crypto import get_random_string
from ckeditor.fields import RichTextField

class Organization(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        saved = super().save(*args, **kwargs)
        _, key = OrganizationAPIKey.objects.create_api_key(
            name="Org Api Key", entity=self
        )
        OrganizationAPI.objects.create(organization = self, key = key)
        return saved

class OrganizationAPIKey(AbstractAPIKey):
    entity = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="api_keys",
    )

class OrganizationAPI(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="apis",
    )
    key = models.CharField(max_length = 300)

class User(models.Model):
    username = models.CharField(max_length = 50)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)


class ApiKey(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)


class GPTChatRoom(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add= True)
    first_message = models.CharField(max_length=1000, null=True)

    def get_age(self):
        return age(self.date)

class GPTMessages(models.Model):
    room = models.ForeignKey(GPTChatRoom, on_delete=models.CASCADE, null=True, blank=True, related_name='chats')
    role = models.CharField(max_length=8)
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add= True)
    like = models.IntegerField(default = 0, validators=[MaxValueValidator(2), MinValueValidator(0)])
