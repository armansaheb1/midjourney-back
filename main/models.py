from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone
from main.lib.age import age
from shopbot.settings import ROOT
from django.forms.models import model_to_dict
import uuid
from django.utils.crypto import get_random_string
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Phone(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    number = models.CharField(max_length=12, unique = True)
    verify = models.BooleanField(default = False)
    code = models.IntegerField(null = True)

class Permissions(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="permissionss")
    gpt = models.BooleanField(default = True)

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
    progress = models.CharField(max_length = 10, null=True)
    done = models.BooleanField(default = False)
    result = models.JSONField(null=True, blank=True)
    image = models.URLField(null=True, blank = True)
    bid = models.CharField(max_length=100, null=True)
    buttons = models.JSONField(null=True, blank=True)
    act = models.CharField(max_length=5, null=True)
    type = models.CharField(max_length=15, null=True)

    def __str__(self):
        return str(self.user.username) + ' - ' +  str(self.code) + ' - ' + str(self.percent) + ' - ' + str(self.progress) + ' - ' + str(self.done) + ' - ' + self.text

    def get_age(self):
        return age(self.date)
    
    def get_variations(self):
        list = []
        for item in self.variations.all().order_by('-id'):
            list.append({'text': item.text, 'image': item.image, 'get_age': item.get_age(), 'type': item.type, 'code': item.code})
        return list

    def username(self):
        return self.user.username

class Package(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add= True)
    amount = models.FloatField()
    expired = models.BooleanField(default = False)

    def __str__(self):
        return self.user.username + '-' + str(self.amount)

class Pretrans(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    code = models.CharField(max_length= 100, null=True)


class Image(models.Model):
    image = models.ImageField(upload_to='image')

    def get_image(self):
        return ROOT + 'media/' + self.image.name


class File(models.Model):
    file = models.FileField(upload_to='file-ex')

    def get_image(self):
        return ROOT + 'media/' + self.file.name

class FaceSwaped(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fsid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.URLField(null=True)
    date = models.DateTimeField(auto_now_add= True)
    code = models.CharField(max_length = 1000, null=True)

    def __str__(self):
        return str(self.fsid)

    def get_age(self):
        return age(self.date)

    def username(self):
        return self.user.username


class Plan(models.Model):
    price = models.IntegerField()
    coin = models.IntegerField()




class Coupon(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    percent = models.IntegerField()
    code = models.CharField(max_length=8, default=get_random_string(length=8), null=True)



class Bonus(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.IntegerField()
    code = models.CharField(max_length=8, default=get_random_string(length=8), blank = True)
    
    def username(self):
        if self.user:
            return self.user.username
        else: 
            return 'all'
    
class UsedBonus(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bonus= models.ForeignKey(Bonus, on_delete=models.CASCADE, null=True, blank=True)


class GPTChatRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add= True)
    first_message = models.CharField(max_length=1000, null=True)

    def get_age(self):
        return age(self.date)

class GPTMessages(models.Model):
    room = models.ForeignKey(GPTChatRoom, on_delete=models.CASCADE, null=True, blank=True, related_name='chats')
    role = models.CharField(max_length=8)
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add= True)


class ImageDetail(models.Model):
    title = models.CharField(max_length=100)
    prompt = models.CharField(max_length=100)
    image = models.ImageField(upload_to='param')

    def get_image(self):
        return ROOT + 'media/' + self.image.name

class AddDetail(models.Model):
    title = models.CharField(max_length=100)
    prompt = models.CharField(max_length=100)
    image = models.ImageField(upload_to='param')

    def get_image(self):
        return ROOT + 'media/' + self.image.name
    
class Mimic(models.Model):
    title = models.CharField(max_length=100)
    prompt = models.CharField(max_length=100)
    image = models.ImageField(upload_to='param')

    def get_image(self):
        return ROOT + 'media/' + self.image.name


class Parameter(models.Model):
    title = models.CharField(max_length=100)
    prompt = models.CharField(max_length=100)
    minimum = models.FloatField(null = True)
    maximum = models.FloatField(null = True)
    default = models.FloatField(null = True)


class Size(models.Model):
    title = models.CharField(max_length=100)
    prompt = models.CharField(max_length=100)
    image = models.ImageField(upload_to='param')

    def get_image(self):
        return ROOT + 'media/' + self.image.name



class Post(models.Model):
    content = RichTextField()
    files = models.FileField(upload_to='file', null=True)

    def get_file(self):
        if not self.files:
            return None
        return ROOT + 'media/' + self.files.name

class Training(models.Model):
    text = models.FileField(upload_to='train', null=True)

    def __str__(self):
        return self.text.name