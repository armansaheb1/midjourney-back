from django.shortcuts import render
from main.models import ImagineOrder, Package, Pretrans, Image, Transaction
from django.contrib.auth.models import User
import requests
import json
from rest_framework.views import APIView 
from rest_framework.response import Response
from main.serializers import UserSerializer, ImagineOrderSerializer, ImageSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

class Users(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        query = User.objects.all()
        serializer = UserSerializer(query, many =True)
        return Response(serializer.data)

class Transactions(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = Transaction.objects.all()
        serializer= TransactionSerializer(query, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        all = 0
        for item in Transaction.objects.all():
            all = all + item.amount
        return Response(all)
    
class Imagines(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = ImagineOrder.objects.filter( order=None)
        serializer= ImagineOrderSerializer(query, many=True)
        return Response(serializer.data)


class Charge(APIView):
    def post(self, request, format=None):
        balance = 0
        for item in Package.objects.filter(user= User.objects.get(id = request.data['id']), expired=False):
            balance = balance + item.amount
        return Response(balance)