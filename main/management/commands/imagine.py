from main.models import Site, Link, ImagineOrder, Image
from django.core.management.base import BaseCommand, CommandError
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from shopbot.settings import ROOT

class Command(BaseCommand):

    def handle(self, *args, **options):
        for item in ImagineOrder.objects.filter(done = False):
            url = "https://api.thenextleg.io/v2/message/"
            headers = {
            'Authorization': 'Bearer 3c64be29-a698-4a52-976f-b2dfb9ca08b0',
            'Content-Type': 'application/json'
            }

            response = requests.request("GET", url + item.code, headers=headers)
            response = response.json()
            if not 'imageUrls' in response['response']:
                item.percent = response['progress']
            elif 'imageUrls' in response['response']:
                im = requests.get(response['response']['imageUrl'])
                name = urlparse(response['response']['imageUrl']).path.split('/')[-1]
                if response.status_code == 200:
                    image = Image()
                    image.image.save(name, ContentFile(im.content), save=True)
                    whole = ROOT + 'media/' + image.name
                    list = []
                    for item in response['response']['imageUrls']:
                        im = requests.get(item)
                        name = urlparse(item).path.split('/')[-1]
                        image = Image()
                        image.image.save(name, ContentFile(im.content), save=True)
                        
                        list.append(ROOT + 'media/' + image.name)
                item.image = whole
                item.result = list
                item.done = True
                item.percent = response['progress']
            item.save()