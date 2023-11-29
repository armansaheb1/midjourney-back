from django.shortcuts import render
from main.models import ImagineOrder, Package, Pretrans, Image, Transaction, Plan, FaceSwaped,Bonus
from django.contrib.auth.models import User
import requests
import json
from rest_framework.views import APIView 
from rest_framework.response import Response
from main.serializers import UserSerializer, ImagineOrderSerializer, ImageSerializer, TransactionSerializer, PlanSerializer, FaceSwapedSerializer, BonusSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework import status

class Users(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        query = User.objects.all()
        list = []
        for item in query:
            balance = 0
            for items in Package.objects.filter(user = item, expired=False):
                balance = balance + items.amount
            list.append({'id': item.id ,'username': item.username, 'balance': balance})
        return Response(list)

class Transactions(APIView):
    permission_classes = [IsAdminUser]

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
        query = ImagineOrder.objects.filter( order=None).order_by('-id')
        serializer= ImagineOrderSerializer(query, many=True)
        return Response(serializer.data)


class Charge(APIView):
    def post(self, request, format=None):
        balance = 0
        for item in Package.objects.filter(user= User.objects.get(id = request.data['id']), expired=False):
            balance = balance + item.amount
        return Response(balance)
    def put(self, request, format=None):
        amount = int(request.data['amount'])
        if request.data['act'] == '+':
            pk = Package(user=User.objects.get(id = request.data['id']), amount = amount)
            pk.save()
            balance = 0
            for item in Package.objects.filter(user= User.objects.get(id = request.data['id']), expired=False):
                balance = balance + item.amount
            return Response(balance)
        else:
            pk = Package.objects.filter(user=User.objects.get(id = request.data['id']), expired = False)
            i = 0
            balance = 0
            for item in pk:
                balance = balance + item.amount
            if amount <= balance:
                for item in pk:
                    if(item.amount > amount):
                        item.amount = item.amount - amount
                        item.save()
                        balance = 0
                        for item in Package.objects.filter(user= User.objects.get(id = request.data['id']), expired=False):
                            balance = balance + item.amount
                        return Response(balance)
                    elif(item.amount == amount):
                        item.amount = item.amount - amount
                        item.save()
                        balance = 0
                        for item in Package.objects.filter(user= User.objects.get(id = request.data['id']), expired=False):
                            balance = balance + item.amount
                        return Response(balance)
                    else:
                        amount = amount - item.amount
                        item.amount = 0
                        item.save()
                        i = i + 1
                balance = 0
                for item in Package.objects.filter(user= User.objects.get(id = request.data['id']), expired=False):
                    balance = balance + item.amount
                return Response(balance)
            else:
                return Response(status = status.HTTP_400_BAD_REQUEST)


class Plans(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = Plan.objects.all().order_by('price')
        serializer = PlanSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlanSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            query = Plan.objects.all().order_by('price')
            serializer = PlanSerializer(query, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ids):
        query = Plan.objects.get(id = ids)
        query.delete()
        query = Plan.objects.all().order_by('price')
        serializer = PlanSerializer(query, many=True)
        return Response(serializer.data)


class FaceSwap(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query = FaceSwaped.objects.all()
        serializer = FaceSwapedSerializer(query, many=True)
        return Response(serializer.data)



class Bonuss(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        query = Bonus.objects.all().order_by('-id')
        serializer = BonusSerializer(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BonusSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            query = Bonus.objects.all().order_by('-id')
            serializer = BonusSerializer(query, many=True)
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ids):
        query = Bonus.objects.get(id = ids)
        query.delete()
        query = Bonus.objects.all().order_by('-id')
        serializer = BonusSerializer(query, many=True)
        return Response(serializer.data)
