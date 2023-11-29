from main.models import Site, Link, ImagineOrder, Image, Transaction
from django.core.management.base import BaseCommand, CommandError
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from shopbot.settings import ROOT
import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        for item in ImagineOrder.objects.filter(done=False):
            item.done = True
            item.save()