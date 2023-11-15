from django.shortcuts import render
from .models import ImagineOrder, Package, Pretrans, Image, Transaction
from django.contrib.auth.models import User
import requests
import json
from rest_framework.views import APIView 
from rest_framework.response import Response
from .serializers import UserSerializer, ImagineOrderSerializer, ImageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
import requests
import json
from django.shortcuts import redirect
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

MERCHANT = '3c64be29-a698-4a52-976f-b2dfb9ca08b0'
ZP_API_REQUEST = "https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/"
CALL_BACK = "http://172.93.231.240/api/verify"

class send_request(APIView):
    def post(self, request, format=None):
        if request.data['amount'] == 100000:
                charge = Package(user=request.user, amount = 50)
                charge.save()
        elif request.data['amount'] == 200000:
            charge = Package(user=request.user, amount = 150)
            charge.save()
        elif request.data['amount'] == 800000:
            charge = Package(user=request.user, amount = 1000)
            charge.save()
        trans = Transaction(user = request.user, amount = request.data['amount'])
        trans.save()
        balance = 0
        for item in Package.objects.filter(user= request.user, expired=False):
            balance = balance + item.amount
        return Response(balance)
        #main
        plans = [100000,200000,800000]
        if not request.data['amount'] in plans:
            return Response('Invalid input')
        data = {
            "MerchantID": MERCHANT,
            "Amount": request.data['amount'],
            "Description": 'Limoo',
            "CallbackURL": CALL_BACK,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                pre = Pretrans(amount= request.data['amount'], code= str(response['Authority']), user=request.user)
                pre.save()
                if response['Status'] == 100:
                    return Response(ZP_API_STARTPAY + str(response['Authority']))
                else:
                    return Response({'status': False, 'code': str(response['Status'])})
            return response
        
        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}


def verify(authority):
    pre = Pretrans.objects.get(code = authority)
    data = {
        "MerchantID": MERCHANT,
        "Amount": pre.amount,
        "Authority": authority,
    }
    data = json.dumps(data)
    headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
    response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

    if response.status_code == 200:
        response = response.json()
        if response['Status'] == 100:
            if pre.amount == 100000:
                charge = Package(user=pre.user, amount = 50)
                charge.save()
            elif pre.amount == 200000:
                charge = Package(user=pre.user, amount = 150)
                charge.save()
            elif pre.amount == 800000:
                charge = Package(user=pre.user, amount = 1000)
                charge.save()
            trans = Transaction(user = pre.user, amount = pre.amount)
            trans.save()
            balance = 0
            for item in Package.objects.filter(user= pre.user, expired=False):
                balance = balance + item.amount
            return redirect('http://localhost:8080/success')
            return {'status': True, 'RefID': response['RefID']}
        else:
            return {'status': False, 'code': str(response['Status'])}
    return response
# Create your views here.

class GetUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query = User.objects.get(id = request.user.id)
        serializer = UserSerializer(query)
        return Response(serializer.data)

class Imagine(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, format=None):
        balance = 0
        wals = Package.objects.filter(user=request.user , expired = False)
        for item in wals:
            balance = balance + item.amount
        if balance == 0:
            return Response(status = status.HTTP_402_PAYMENT_REQUIRED)
        wal = wals.first()
        wal.amount = wal.amount - 1
        wal.save()
        url = "https://api.thenextleg.io/v2/imagine"

        payload = json.dumps({
        "msg": request.data['text'],
        "ref": "",
        "webhookOverride": "", 
        "ignorePrefilter": "false"
        })
        headers = {
        'Authorization': 'Bearer 3c64be29-a698-4a52-976f-b2dfb9ca08b0',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.json()['messageId']:
            imagine = ImagineOrder(user=request.user,text = request.data['text'], code=response.json()['messageId'])
            imagine.save()
            serializer = ImagineOrderSerializer(imagine)
            return Response(serializer.data)        
        return Response(status=status.HTTP_400_BAD_REQUEST)    
                    
class ImagineResult(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, ids):
        query = ImagineOrder.objects.filter(code = ids)
        if len(query):
            if query.last().image:
                serializer = ImagineOrderSerializer(query.last())
                return Response(serializer.data)
        else:
            item = query.last()
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
                item.result = response['response']['imageUrls']
                item.image = response['response']['imageUrl']
                item.done = True
                item.percent = response['progress']
            item.save()
            serializer = ImagineOrderSerializer(item)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST) 


class ImagineResult(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, ids):
        query = ImagineOrder.objects.filter(code = ids)
        if len(query):
            if query.last().image:
                serializer = ImagineOrderSerializer(query.last())
                return Response(serializer.data)
        item = query.last()
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
            item.result = response['response']['imageUrls']
            item.image = response['response']['imageUrl']
            item.done = True
            item.bid =response['response']['buttonMessageId']
            item.percent = response['progress']

            item.buttons = response['response']['buttons']
        item.save()
        serializer = ImagineOrderSerializer(item)
        return Response(serializer.data)

class Button(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        balance = 0
        wals = Package.objects.filter(user=request.user , expired = False)
        for item in wals:
            balance = balance + item.amount
        if balance == 0:
            return Response(status = status.HTTP_402_PAYMENT_REQUIRED)
        wal = wals.first()
        wal.amount = wal.amount - 1
        wal.save()
        url = "https://api.thenextleg.io/v2/button"

        payload = json.dumps({
        "buttonMessageId": f"{request.data['code']}",
        "button": f"{request.data['btn']}",
        "ref": "",
        "webhookOverride": ""
        })
        headers = {
        'Authorization': 'Bearer 3c64be29-a698-4a52-976f-b2dfb9ca08b0',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        if response.json()['messageId']:
            order= ImagineOrder.objects.get(bid = request.data['code'])
            if order.order:
                order = order.order
            imagine = ImagineOrder(user=request.user,text = order.text, code=response.json()['messageId'], order=order , act = request.data['act'])
            imagine.save()
            serializer = ImagineOrderSerializer(imagine)
            return Response(serializer.data)        
        return Response(status=status.HTTP_400_BAD_REQUEST)

class MyImagine(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query = ImagineOrder.objects.filter(user = request.user, order=None)
        serializer = ImagineOrderSerializer(query, many=True)
        return Response(serializer.data)


class Charge(APIView):
    def get(self, request, format=None):
        balance = 0
        for item in Package.objects.filter(user= request.user, expired=False):
            balance = balance + item.amount
        return Response(balance)


class Images(APIView):
    queryset = Image.objects.order_by('-id')
    serializer_class = ImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer= ImageSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors)
        return Response(serializer.data)


