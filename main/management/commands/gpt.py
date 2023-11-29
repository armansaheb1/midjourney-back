from main.models import Site, Link, ImagineOrder, Image
from django.core.management.base import BaseCommand, CommandError
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from shopbot.settings import ROOT
from openai import OpenAI
client = OpenAI(api_key= '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')


class Command(BaseCommand):

    def handle(self, *args, **options):
        def get_embedding(text, model="text-embedding-ada-002"):
            text = text.replace("\n", " ")
            return client.embeddings.create(input = [text], model=model)['data'][0]['embedding']
        print(get_embedding(text = 'Write a tagline for an ice cream shop.'))