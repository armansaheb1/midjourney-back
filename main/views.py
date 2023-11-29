from django.shortcuts import render
from .models import ImagineOrder, Package, Pretrans, Image, Transaction, FaceSwaped, Plan, Bonus, Coupon, UsedBonus
from django.contrib.auth.models import User
import requests
import json
from rest_framework.views import APIView 
from rest_framework.response import Response
from .serializers import UserSerializer, ImagineOrderSerializer, ImageSerializer, FaceSwapedSerializer, PlanSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
import requests
import json
from django.shortcuts import redirect
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from PIL import Image as IM
import uuid
from io import BytesIO
from shopbot.settings import ROOT
from base64 import b64decode
from django.http import HttpResponse
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from django.http import JsonResponse
import base64
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created

from openai import OpenAI
gpt_client = OpenAI(api_key= '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')





@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key),
        'token' : reset_password_token.key
    }

    # render email text
    email_html_message = render_to_string('email/password_reset_email.html', context)
    email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

MERCHANT = '96e3a7b9-66ef-4abb-9c7b-8f699d4237bc'
ZP_API_REQUEST = "https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/"
CALL_BACK = "http://limoo.ai/api/verify"

class vpn(APIView):
    permission_classes = [AllowAny]


    def get(self, request, ss):
        with open('/midjourney-back/main/a.csv','r') as myfile:
            response = HttpResponse(myfile, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=a.csv'
            return response

class vpn2(APIView):
    permission_classes = [AllowAny]


    def get(self, request, ss):
        passed = str(base64.b64decode("Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTplMDVCVFkwcG8ya3o3ckplTTJWRVdn"))
        passed = passed.replace("b'", "").replace("'", "")
        passeds = passed.split(':')
        return JsonResponse({
            
            "server": "nl.xray.services",
            "server_port": 18781,
            "password": passeds[1],
            "method": passeds[0]
            })



class send_request(APIView):
    def post(self, request, format=None):
        if not len(Plan.objects.filter(id = request.data['amount'] )):
            return Response('Invalid input')
        plan = Plan.objects.get(id = request.data['amount'] )
        data = {
            "MerchantID": MERCHANT,
            "Amount": plan.price,
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
                pre = Pretrans(amount= plan.price, code= str(response['Authority']), user=request.user)
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

class verify(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        Authority = request.GET.get('Authority', '')
        pre = Pretrans.objects.get(code = Authority)
        data = {
            "MerchantID": MERCHANT,
            "Amount": pre.amount,
            "Authority": Authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                if not len(Plan.objects.filter(price = pre.amount )):
                    return Rsponse('invalid transaction')
                else:
                    plan = Plan.objects.get(price = pre.amount )
                    charge = Package(user=pre.user, amount = plan.coin)
                    charge.save()
                    trans = Transaction(user = pre.user, amount = pre.amount)
                    trans.save()
                    return redirect('https://limoo.ai/success')
            else:
                return Response({'status': False, 'code': str(response['Status'])})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)  
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
        wals = Package.objects.filter(user=request.user , expired = False, amount__gte=1)
        for item in wals:
            balance = balance + item.amount
        if balance == 0:
            return Response('موجودی شما کافی نیست',status = status.HTTP_402_PAYMENT_REQUIRED)
        if balance == 1:
            if len(ImagineOrder.objects.filter(user = request.user, done= False)):
                return Response('You Have A Pending order And موجودی شما کافی نیست for Another One',status = status.HTTP_402_PAYMENT_REQUIRED)
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



class Gpt(APIView):
    permission_classes = [IsAuthenticated]

    def get_text(text, model="text-embedding-ada-002"):
            client.completions.create(
            model="gpt-4.5-turbo-instruct",
            prompt="Write a tagline for an ice cream shop."
        )
    
    def post(self, request, format=None):
        balance = 0
        wals = Package.objects.filter(user=request.user , expired = False, amount__gte=1)
        for item in wals:
            balance = balance + item.amount
        if balance == 0:
            return Response('موجودی شما کافی نیست',status = status.HTTP_402_PAYMENT_REQUIRED)
        if balance == 1:
            if len(ImagineOrder.objects.filter(user = request.user, done= False)):
                return Response('You Have A Pending order And موجودی شما کافی نیست for Another One',status = status.HTTP_402_PAYMENT_REQUIRED)
        
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.json()['messageId']:
            imagine = ImagineOrder(user=request.user,text = request.data['text'], code=response.json()['messageId'])
            imagine.save()
            serializer = ImagineOrderSerializer(imagine)
            return Response(serializer.data)        
        return Response(status=status.HTTP_400_BAD_REQUEST)   



class ImagineArs(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
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
        return Response(response.json()['messageId'])   



class FaceSwap(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ids):
        query = FaceSwaped.objects.get(fsid = ids)
        serializer = FaceSwapedSerializer(query)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        balance = 0
        wals = Package.objects.filter(user=request.user , expired = False, amount__gte=4)
        for item in wals:
            balance = balance + item.amount
        if balance < 4:
            return Response('موجودی شما کافی نیست',status = status.HTTP_402_PAYMENT_REQUIRED)
        else:
            url = "https://api.thenextleg.io/face-swap"

            payload = json.dumps({
            "sourceImg": request.data['text'][0],
            "targetImg": request.data['text'][1],
            })
            
            headers = {
            'Authorization': 'Bearer 3c64be29-a698-4a52-976f-b2dfb9ca08b0',
            'Content-Type': 'application/json'
            }
            img = Image()
            filename = str(uuid.uuid4())
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.status_code == 200:
                wal = wals.first()
                wal.amount = wal.amount - 4
                wal.save()
                response = response.content
                image = IM.open(BytesIO(response))
                image.save('/midjourney-back/media/fs/' + filename + '.jpg') 

                swaped = FaceSwaped(user = request.user, image = ROOT + '/media/fs/' + filename + '.jpg')
                swaped.save()
                serializer = FaceSwapedSerializer(swaped)

                return Response(serializer.data)    
            else:
                return Response(response.content,status=status.HTTP_400_BAD_REQUEST) 
                    


class ImagineResult(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, ids):
        wals = Package.objects.filter(user=request.user , expired = False, amount__gte=1)
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
        if not 'imageUrl' in response['response']:
            item.percent = response['progress']
            item.progress = response['progress']
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
            item.progress = 'Incomplete'
            item.done = True
        item.save()
        serializer = ImagineOrderSerializer(item)
        return Response(serializer.data)

class ImagineResultArs(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, ids):

        url = "https://api.thenextleg.io/v2/message/"
        headers = {
        'Authorization': 'Bearer 3c64be29-a698-4a52-976f-b2dfb9ca08b0',
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url + ids, headers=headers)
        response = response.json()
        if 'imageUrls' in response['response']:
            return Response(response['response']['imageUrls'])
        else:
            return Response(response['progress'])

class Button(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, format=None):
        balance = 0
        wals = Package.objects.filter(user=request.user , expired = False)
        for item in wals:
            balance = balance + item.amount
        if balance == 0:
            return Response('موجودی شما کافی نیست',status = status.HTTP_402_PAYMENT_REQUIRED)
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
            imagine = ImagineOrder(user=request.user,text = order.text, code=response.json()['messageId'], order=order , act = request.data['act'], type=request.data['btn'])
            imagine.save()
            serializer = ImagineOrderSerializer(imagine)
            return Response(serializer.data)        
        return Response(status=status.HTTP_400_BAD_REQUEST)

class MyImagine(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query = ImagineOrder.objects.filter(user = request.user, order=None).order_by('-id')
        serializer = ImagineOrderSerializer(query, many=True)
        return Response(serializer.data)

class MyFaceSwap(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query = FaceSwaped.objects.filter(user = request.user).order_by('-date')
        serializer = FaceSwapedSerializer(query, many=True)
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


class Plans(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = Plan.objects.all().order_by('price')
        serializer = PlanSerializer(query, many=True)
        return Response(serializer.data)



class CheckBonus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, token):
        query = Bonus.objects.filter(code = token)
        if not len(query):
            return Response('Invalid Code', status= status.HTTP_400_BAD_REQUEST)
        if query.last().user:
            if query.last().user != request.user:
                return Response('This Code Is For Another User', status= status.HTTP_400_BAD_REQUEST)
        if len(UsedBonus.objects.filter(user = request.user, bonus = query.last())):
            return Response('You Used This Coupon Before', status= status.HTTP_400_BAD_REQUEST)
        return Response(query.last().amount)


class GetBonus(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data['token']
        query = Bonus.objects.filter(code = token)
        if not len(query):
            return Response('Invalid Code', status= status.HTTP_400_BAD_REQUEST)
        if query.last().user:
            if query.last().user != request.user:
                return Response('This Code Is For Another User', status= status.HTTP_400_BAD_REQUEST)
        if len(UsedBonus.objects.filter(user = request.user, bonus = query.last())):
            return Response('You Used This Coupon Before', status= status.HTTP_400_BAD_REQUEST)
        charge = Package(user=request.user, amount = query.last().amount)
        charge.save()
        ub = UsedBonus(user= request.user, bonus = query.last())
        ub.save()
        balance = 0
        for item in Package.objects.filter(user= request.user, expired=False):
            balance = balance + item.amount
        return Response(balance)
