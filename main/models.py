from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from main.lib.age import age
from shopbot.settings import ROOT
from django.forms.models import model_to_dict

# Create your models here.
class Site(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Link(models.Model):
    link=models.URLField()
    sizes = models.JSONField(null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    size = models.BooleanField(default = False)
    have = models.BooleanField(default = True, editable= False)

    def __str__(self) -> str:
        return self.link


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add= True)
    amount = models.IntegerField()

    def get_age(self):
        return age(self.date)

    def username(self):
        return self.user.username


class ImagineOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order= models.ForeignKey('self', on_delete=models.CASCADE, related_name='variations', null=True, blank = True)
    text = models.CharField(max_length = 1000, null = True)
    date = models.DateTimeField(auto_now_add= True)
    code = models.CharField(max_length = 1000)
    percent = models.IntegerField(default = 0)
    done = models.BooleanField(default = False)
    result = models.JSONField(null=True, blank=True)
    image = models.URLField(null=True, blank = True)
    bid = models.CharField(max_length=100, null=True)
    buttons = models.JSONField(null=True, blank=True)
    act = models.CharField(max_length=5, null=True)
    type = models.CharField(max_length=15, null=True)

    def get_age(self):
        return age(self.date)
    
    def get_variations(self):
        list = []
        for item in self.variations.all():
            list.append(model_to_dict(item))
        return list

class Package(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add= True)
    amount = models.IntegerField()
    expired = models.BooleanField(default = False)

class Pretrans(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    code = models.CharField(max_length= 100, null=True)


class Image(models.Model):
    image = models.ImageField(upload_to='image')

    def get_image(self):
        return ROOT + 'media/' + self.image.name
