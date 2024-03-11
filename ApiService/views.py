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
from typing import List, Optional
from scipy import spatial
import math
import numpy as np
import pandas as pd

def distances_from_embeddings(
    query_embedding: List[float],
    embeddings: List[List[float]],
    distance_metric="cosine",
) -> List[List]:
    """Return the distances between a query embedding and a list of embeddings."""
    distance_metrics = {
        "cosine": spatial.distance.cosine,
        "L1": spatial.distance.cityblock,
        "L2": spatial.distance.euclidean,
        "Linf": spatial.distance.chebyshev,
    }
    distances = [
        distance_metrics[distance_metric](query_embedding, embedding)
        for embedding in embeddings
    ]
    return distances


client = OpenAI(api_key= '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')


class Gpt(APIView):
    authentication_classes = (OrganizationAPIKeyAuthentication, )
    permission_classes = [IsActiveEntity]

    def create_context(self, 
        question, df, max_len=1800, size="ada"
        ):
            """
            Create a context for a question by finding the most similar context from the dataframe
            """

            # Get the embeddings for the question
            q_embeddings = client.embeddings.create(input=question, model='text-embedding-ada-002').data[0].embedding

            # Get the distances from the embeddings
            df['distances'] = distances_from_embeddings(q_embeddings, df['embeddings'].values, distance_metric='cosine')


            returns = []
            cur_len = 0

            # Sort by distance and add the text to the context until the context is too long
            for i, row in df.sort_values('distances', ascending=True).iterrows():

                # Add the length of the text to the current length
                cur_len += row['n_tokens'] + 4

                # If the context is too long, break
                if cur_len > max_len:
                    break

                # Else add it to the text that is being returned
                returns.append(row["text"])

            # Return the context
            return "\n\n###\n\n".join(returns)

    def answer_question(
            self,
        df,
        model="gpt-3.5-turbo",
        question="Am I allowed to publish model outputs to Twitter, without a human review?",
        max_len=10000,
        size="ada",
        debug=False,
        max_tokens=600,
        stop_sequence=None
    ):
        """
        Answer a question based on the most similar context from the dataframe texts
        """
        context = self.create_context(
            question,
            df,
            max_len=max_len,
            size=size,
        )
        # If debug, print the raw model response
        if debug:
            print("Context:\n" + context)
            print("\n\n")

        # Create a chat completion using the question and context
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "if there is question response answer from context and make sure to add further reading link to the bottom else response as an assistance in messages language"},
                {"role": "user", "content": f"Context: {context}\n\n---\n\nQuestion: {question}"}
            ],
            temperature=0.3,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
        )
        return [response.choices[0].message.content.replace('Further reading:', '').replace('Answer:', '').replace('[Further Reading on ePlanet Brokers]', ''), context]

    def get_text(self, text):
            df=pd.read_csv('/midjourney-back/media/brockerdone/embeddings.csv', index_col=0)
            df['embeddings'] = df['embeddings'].apply(eval).apply(np.array)

            df.head()
            return self.answer_question(df=df, question=text)

    def get(self, request, ids=None, page=0):
        if not ids:
            return Response('Username is required as parameter', status=status.HTTP_406_NOT_ACCEPTABLE)
        if not page:
            page = 0
        
        user= User.objects.filter(username = ids)
        if not len(user):
            return Response('User not found', status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            user = user.last()
        room = GPTChatRoom.objects.get(user = user, organization = request.user)
        query = GPTMessages.objects.filter(room = room).order_by('-id')
        pages = math.ceil(query.count()/10)
        serializer = GPTMessagesSerializer(query, many=True)
        if int(page) + 1 < pages:
            next = f'https://limoo.ai/api/v1/support/{ids}/{str(int(page) + 1)}'
        else:
            next = None

        return Response({'count' : query.count(),'pages': pages , 'id': ids, 'nextpage': next,'result': serializer.data}) 
    
    def post(self, request, format=None):
        if not 'username' in request.data:
            return Response('Username is required', status=status.HTTP_406_NOT_ACCEPTABLE)
        user, was = User.objects.get_or_create(username=request.data['username'], organization = request.user)
        room, was = GPTChatRoom.objects.get_or_create(user= user, organization = request.user)
        message = GPTMessages(room = room, message = request.data['text'], role = 'user')
        message.save()
        try:
            result = self.get_text(request.data['text'])
            context = result[1]
            while '\n###\n' in context:
                context = context.replace('\n###\n', ',')
            message = GPTMessages(room = room, message = result[0], context = context, role = 'System')
            message.save()
            query = GPTMessages.objects.filter(room = room)
            serializer = GPTMessagesSerializer(query, many=True)
            
            return Response({'result': result[0], 'id': room.id}) 
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
