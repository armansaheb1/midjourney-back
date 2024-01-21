from main.models import Site, Link, ImagineOrder, Image, Permissions, Package
from django.core.management.base import BaseCommand, CommandError
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from shopbot.settings import ROOT
from openai import OpenAI
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        for item in ImagineOrder.objects.filter(done = False):
            wals = Package.objects.filter(user=item.user , expired = False, amount__gte=1)
            if not len(wals):
                item.done = True
                item.save()
                print(wals)
                continue
            url = "https://api.thenextleg.io/v2/message/"
            headers = {
            'Authorization': 'Bearer 3c64be29-a698-4a52-976f-b2dfb9ca08b0',
            'Content-Type': 'application/json'
            }

            response = requests.request("GET", url + item.code, headers=headers)
            response = response.json()
            if not 'imageUrl' in response['response']:
                if type(response['progress']) == 'int':
                    item.percent = response['progress']
                elif response['progress'] == 'incomplete':
                    item.progress = response['progress']
                    item.done = True
            elif len(response['response']['imageUrl']):
                wal = wals.first()
                wal.amount = wal.amount - 1
                wal.save()
                item.result = response['response']['imageUrls']
                item.image = response['response']['imageUrl']
                item.done = True
                item.bid =response['response']['buttonMessageId']
                item.percent = response['progress']
                item.buttons = response['response']['buttons']
            else:
                item.progress = response['progress']
                item.done = True
            item.save()
