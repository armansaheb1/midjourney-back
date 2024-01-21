from main.models import Site, Link, ImagineOrder, Image, Permissions
from django.core.management.base import BaseCommand, CommandError
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from shopbot.settings import ROOT
from openai import OpenAI
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        for item in User.objects.all():
            if not hasattr(item, 'permissionss'):
                per = Permissions.objects.create(user = item)
