from main.models import Site, Link, ImagineOrder, Image, Permissions, Package
from django.core.management.base import BaseCommand, CommandError
import requests
from urllib.parse import urlparse
from django.core.files.base import ContentFile
from shopbot.settings import ROOT
from openai import OpenAI
from django.contrib.auth.models import User
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from openai import OpenAI

from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, LLMPredictor, ServiceContext, StorageContext, load_index_from_storage, PromptHelper

import os
os.environ['OPENAI_API_KEY'] = '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'

gpt_client = OpenAI(api_key= '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')


class Command(BaseCommand):

    def handle(self, *args, **options):
        max_input_size = 4096
        num_outputs = 512
        max_chunk_overlap = 0.2
        chunk_size_limit = 600
        prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.3, model_name="gpt-4-1106-preview", max_tokens=num_outputs))
        documents = SimpleDirectoryReader('/midjourney-back/media/brocker').load_data()
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
        index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
        index.storage_context.persist(persist_dir='/midjourney-back/media/brocker/done')
        print('done')






