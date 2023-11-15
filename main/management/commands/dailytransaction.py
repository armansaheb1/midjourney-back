from main.models import Site, Link, ImagineOrder, Image, Transaction
from django.core.management.base import BaseCommand, CommandError
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from shopbot.settings import ROOT
import datetime

class Command(BaseCommand):

    def handle(self, *args, **options):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        for item in Transaction.objects.all():
            pass