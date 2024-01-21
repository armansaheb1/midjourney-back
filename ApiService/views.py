from django.shortcuts import render
from rest_framework import viewsets
from rest_framework_simple_api_key.backends import APIKeyAuthentication
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.views import APIView 
from rest_framework.decorators import action
from rest_framework_simple_api_key.permissions import IsActiveEntity
from rest_framework import status
from ApiService.backends import OrganizationAPIKeyAuthentication
from ApiService.models import OrganizationAPIKey, Organization, OrganizationAPI
import random
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from openai import OpenAI
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, LLMPredictor, ServiceContext, StorageContext, load_index_from_storage, PromptHelper
from .models import GPTChatRoom, GPTMessages, User
import os
from .serializers import GPTChatRoomSerializer, GPTMessagesSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny



class Gpt(APIView):
    authentication_classes = (OrganizationAPIKeyAuthentication, )
    permission_classes = [IsActiveEntity]

    def get_text(self, text):
            max_input_size = 4096
            num_outputs = 512
            max_chunk_overlap = 0.2
            chunk_size_limit = 600
            prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)
            llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.1, model_name="text-babbage-001", max_tokens=num_outputs))
            documents = SimpleDirectoryReader('/midjourney-back/media/train').load_data()
            service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt_helper)
            index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
            index.storage_context.persist(persist_dir='/midjourney-back/media/train/done')
            storage_context = StorageContext.from_defaults(persist_dir='/midjourney-back/media/train/done')
            index = load_index_from_storage(storage_context)
            response = index.as_query_engine().query(text)
            return response.response

    def get(self, request, ids):
        user= User.objects.get(username = ids)
        room = GPTChatRoom.objects.get(user = user, organization = request.user)
        query = GPTMessages.objects.filter(room = room)
        serializer = GPTMessagesSerializer(query, many=True)
        
        return Response({'result': serializer.data, 'id': ids}) 
    
    def post(self, request, format=None):
        if not 'username' in request.data:
            return Response('Username is required', status=status.HTTP_406_NOT_ACCEPTABLE)
        user, was = User.objects.get_or_create(username=request.data['username'], organization = request.user)
        room, was = GPTChatRoom.objects.get_or_create(user= user, organization = request.user)
        message = GPTMessages(room = room, message = request.data['text'], role = 'user')
        message.save()
        try:
            result = self.get_text(request.data['text'])
            message = GPTMessages(room = room, message = result, role = 'System')
            message.save()
            query = GPTMessages.objects.filter(room = room)
            serializer = GPTMessagesSerializer(query, many=True)
            
            return Response({'result': serializer.data, 'id': room.id}) 
        except Exception as error:
            return Response(str(error),status=status.HTTP_400_BAD_REQUEST)   

class MyGPT(APIView):
    authentication_classes = (OrganizationAPIKeyAuthentication, )
    permission_classes = [IsActiveEntity]

    def get(self, request, format=None):
        if not len(User.objects.filter(username = request.data['username'])):
            return Response('Username not found', status=status.HTTP_404_NOT_FOUND)
        query = GPTChatRoom.objects.all().order_by('-id')
        serializer = GPTChatRoomSerializer(query, many=True)
        return Response(serializer.data)

class Like(APIView):
    authentication_classes = (OrganizationAPIKeyAuthentication, )
    permission_classes = [IsActiveEntity]

    def post(self, request, format=None):
        gpt = GPTMessages.objects.filter(id = request.data['id'])
        if not len(gpt):
            return Response('Message not found', status=status.HTTP_404_NOT_FOUND)
        if not 'like' in  request.data:
            return Response('like required', status=status.HTTP_406_NOT_ACCEPTABLE)
        if int(request.data['like']) > 2 or int(request.data['like']) < 0:
            return Response('like must be between 0 and 2', status=status.HTTP_406_NOT_ACCEPTABLE)
        gpt = gpt.last()
        gpt.like = request.data['like']
        gpt.save()
        return Response('Done')
