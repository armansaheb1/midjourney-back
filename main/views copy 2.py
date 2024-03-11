from django.shortcuts import render
from .models import ImagineOrder, Package, Pretrans, Image, Transaction, FaceSwaped, Plan, Bonus, Coupon, UsedBonus, GPTChatRoom, GPTMessages, ImageDetail, AddDetail, Mimic, Parameter, Size, Post, Permissions, Phone
from django.contrib.auth.models import User
import requests
import json
from rest_framework.views import APIView 
from rest_framework.response import Response
from .serializers import UserSerializer, ImagineOrderSerializer, ImageSerializer, FaceSwapedSerializer, PlanSerializer, GPTMessagesSerializer, GPTChatRoomSerializer, OptionSerializer, ParamSerializer, PostSerializer
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
import random
from ippanel import Client
from django_rest_passwordreset.signals import reset_password_token_created
import random
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from openai import OpenAI
#from langchain.llms import HuggingFacePipeline
#from transformers import AutoTokenizer, AutoModelForCausalLM

def sms(phone , vcode , pattern = 'nqdr0ifi03fapdu'):
    sms = Client("J2dm_5aAB4OjTEAWGSs5JFm5aNKJDs_e0G2uTMu8bRk=")
    pattern_values = {
        "verification-code": f"{vcode}",
    }

    bulk_id = sms.send_pattern(
        pattern,
        "+983000505",
        f"+98{phone}",
        pattern_values,
    )

    sms.get_message(bulk_id)
    return True

from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex, LLMPredictor, ServiceContext, StorageContext, load_index_from_storage, PromptHelper

import os
os.environ['OPENAI_API_KEY'] = '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'

gpt_client = OpenAI(api_key= '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')

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key),
        'token' : reset_password_token.key
    }

    
    email_html_message = render_to_string('email/password_reset_email.html', context)
    email_plaintext_message = render_to_string('email/password_reset_email.txt', context)

    msg = EmailMultiAlternatives(
        
        "Password Reset for {title}".format(title="Some website title"),
        
        email_plaintext_message,
        
        "noreply@somehost.local",
        
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
'''
MERCHANT = '96e3a7b9-66ef-4abb-9c7b-8f699d4237bc'
ZP_API_REQUEST = "https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/"
CALL_BACK = "http://limoo.ai/api/verify"
'''


'''
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
'''

PP_MERCHANT = 'CPgw7kQ75fjMZ496hkROyEiX_ki9aeonPKErbOlzqRQ'
PP_API_REQUEST = "https://api.payping.ir/v2/pay"
PP_API_VERIFY = "https://api.payping.ir/v2/pay/verify"
PP_API_STARTPAY = "https://api.payping.ir/v2/pay/gotoipg/"
PP_CALL_BACK = "https://limoo.ai/api/verify"

class send_request(APIView):
    def post(self, request, format=None):
        if not len(Plan.objects.filter(id = int(request.data['amount']) )):
            return Response('Invalid input')
        plan = Plan.objects.get(id = request.data['amount'] )
        rand = random.randint(123456, 999999)
        data = {
            "amount": plan.price,
            "returnUrl": PP_CALL_BACK,
            "clientRefId": rand
        }
        data = json.dumps(data)
        
        headers = {'content-type': 'application/json', 'content-length': str(len(data)), "Authorization":'Bearer ' + PP_MERCHANT}
        try:
            response = requests.post(PP_API_REQUEST, data=data,headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                pre = Pretrans(amount= plan.price, code= rand, user=request.user)
                pre.save()
                return Response(PP_API_STARTPAY + str(response['code']))
            return Response({'status': False, 'code': 'timeout'})
        
        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}


class SMSVerify(APIView):
    permission_classes = [AllowAny]

    def get(self, request, phone):
        phone, _ = Phone.objects.get_or_create(number = phone)
        phone.code = random.randint(123456, 999999)
        phone.save()
        if phone.verify:
            return Response()
        else:
            phone.code = random.randint(123456, 999999)
            phone.save()    
            try:
                sms(phone.number , phone.code)
            except:
                pass
            return Response(status = 401)

    def post(self, request, phone):
        phone = Phone.objects.get(number = phone)
        if phone.code == int(request.data['code']):
            phone.verify = True
            phone.save()
            return Response(True)
        return Response(status = 401)
        
    def put(self, request, phone):
        phone = Phone.objects.get(number = phone)
        if not request.user.is_authenticated:
            user = User.objects.get(username = request.data['username'])
        else:
            user = request.user
        phone.user = user
        phone.save()
        return Response()


class CheckVerify(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        phone= Phone.objects.filter(user = request.user)
        if len(phone):
            if phone.last().verify:
                return Response()
        return Response(status= 401)

class SMSVerifyUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, phone):
        phone, _ = Phone.objects.get_or_create(number = phone)
        phone.code = random.randint(123456, 999999)
        phone.save()
        if phone.verify:
            return Response()
        else:
            phone.code = random.randint(123456, 999999)
            phone.save()    
            try:
                sms(phone.number , phone.code)
            except:
                pass
            return Response(status = 401)

    def post(self, request, phone):
        phone = Phone.objects.get(number = phone)
        if phone.code == int(request.data['code']):
            phone.verify = True
            phone.save()
            return Response(True)
        return Response(status = 401)
        
    def put(self, request, phone):
        phone = Phone.objects.get(number = phone)
        user = User.objects.get(id = request.user.id)
        phone.user = user
        phone.save()
        return Response()

        
class verify(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        Authority = request.data['clientrefid']
        pre = Pretrans.objects.get(code = Authority)
        plan = Plan.objects.get(price = pre.amount )
        data = {
            "refId": request.data['refid'],
            "amount": plan.price,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)), "Authorization":'Bearer ' + PP_MERCHANT}
        response = requests.post(PP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            if not len(Plan.objects.filter(price = pre.amount )):
                return Rsponse('invalid transaction')
            else:
                
                charge = Package(user=pre.user, amount = plan.coin)
                charge.save()
                trans = Transaction(user = pre.user, amount = pre.amount)
                trans.save()
                return redirect('https://limoo.ai/success')
        else:
            return Response(response,status=status.HTTP_400_BAD_REQUEST)  


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
        url = "https://api.mymidjourney.ai/api/v1/midjourney/imagine"
        payload = json.dumps({
        "prompt": request.data['text'],
        })
        headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ODQwMSwiZW1haWwiOiJsbGltb29haUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImxsaW1vb2FpQGdtYWlsLmNvbSIsImlhdCI6MTcwNTYwOTY3NH0.V17JuXug9v8klMenrpw6OGTiVsU8LANrHPBpD9IoCjI',
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        try:
            if response.json()['success']:
                imagine = ImagineOrder(user=request.user,text = request.data['text'], code=response.json()['messageId'])
                imagine.save()
                serializer = ImagineOrderSerializer(imagine)
                return Response(serializer.data)      
            else:
                return Response(response,status=status.HTTP_400_BAD_REQUEST)  
        except Exception as inst:
            return Response(response,status=status.HTTP_400_BAD_REQUEST)



class Gpt(APIView):
    permission_classes = [IsAuthenticated]

    def get_text(self, text):
            return gpt_client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=text)

    def get(self, text, ids):
        room = GPTChatRoom.objects.get(id = ids)
        query = GPTMessages.objects.filter(room = room)
        serializer = GPTMessagesSerializer(query, many=True)
        
        return Response({'result': serializer.data, 'id': ids}) 
    
    def post(self, request, format=None):
        balance = 0
        wals = Package.objects.filter(user=request.user , expired = False, amount__gte=1)
        for item in wals:
            balance = balance + item.amount
        if balance == 0:
            return Response('موجودی شما کافی نیست',status = status.HTTP_402_PAYMENT_REQUIRED)
        if balance == 1:
            if len(ImagineOrder.objects.filter(user = request.user, done= False)):
                return Response('You Have A Pending order And  Your Balance Is Not Enough for Another One',status = status.HTTP_402_PAYMENT_REQUIRED)
        per, create = Permissions.objects.get_or_create(user = request.user)
        if not per.gpt:
            return Response('This Is Not Enable For You',status = status.HTTP_402_PAYMENT_REQUIRED)
        lists = [{"role": "system", "content": "You are a helpful assistant."}]
        if not 'id' in request.data:
            room = GPTChatRoom(user= request.user, first_message = request.data['text'])
            room.save()
        else:
            room = GPTChatRoom.objects.get(id= request.data['id'])
        message = GPTMessages(room = room, message = request.data['text'], role = 'user')
        message.save()
        for item in GPTMessages.objects.filter(room = room):
            lists.append( {"role": item.role, "content": item.message})
        lists.append({"role": 'user', "content": request.data['text']})
        try:
            result = self.get_text(lists)
            message = GPTMessages(room = room, message = result.choices[0].message.content, role = result.choices[0].message.role)
            message.save()
            wal = wals.first()
            if (result.usage.total_tokens/ 1000 > wal.amount):
                return Response(status=status.HTTP_400_BAD_REQUEST)
            wal.amount = wal.amount - (result.usage.total_tokens/ 1000)
            wal.save()
            query = GPTMessages.objects.filter(room = room)
            serializer = GPTMessagesSerializer(query, many=True)
            
            return Response(result.choices[0].message.content) 
        except Exception as error:
            return Response(str(error),status=status.HTTP_400_BAD_REQUEST)   

class MyGPT(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        query = GPTChatRoom.objects.filter(user = request.user).order_by('-id')
        serializer = GPTChatRoomSerializer(query, many=True)
        return Response(serializer.data)


class Support(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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
        response = index.as_query_engine().query(request.data['text'])
        return Response(response.response) 

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
            url = "https://api.mymidjourney.ai/api/v1/midjourney/faceswap"

            payload = json.dumps({
            "source": request.data['text'][0],
            "target": request.data['text'][1],
            })
            
            headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ODQwMSwiZW1haWwiOiJsbGltb29haUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImxsaW1vb2FpQGdtYWlsLmNvbSIsImlhdCI6MTcwNTYwOTY3NH0.V17JuXug9v8klMenrpw6OGTiVsU8LANrHPBpD9IoCjI',
            'Content-Type': 'application/json'
            }
            filename = str(uuid.uuid4())
            response = requests.request("POST", url, headers=headers, data=payload)
            if response.json()['success']:            
                swaped = FaceSwaped(user = request.user, code=response.json()['messageId'])
                swaped.save()
                serializer = FaceSwapedSerializer(swaped)
                return Response(serializer.data)    
            else:
                return Response(response,status=status.HTTP_400_BAD_REQUEST) 
                    
class FaceSwapResult(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, ids):
        if not request.user.is_authenticated:
            query = FaceSwaped.objects.filter(code = ids)
            item = query.last()
            url = "https://api.mymidjourney.ai/api/v1/midjourney/message/"
            headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ODQwMSwiZW1haWwiOiJsbGltb29haUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImxsaW1vb2FpQGdtYWlsLmNvbSIsImlhdCI6MTcwNTYwOTY3NH0.V17JuXug9v8klMenrpw6OGTiVsU8LANrHPBpD9IoCjI',
            'Content-Type': 'application/json'
            }

            response = requests.request("GET", url + ids, headers=headers)
            response = response.json()
            return Response(response)
        wals = Package.objects.filter(user=request.user , expired = False, amount__gte=1)
        query = FaceSwaped.objects.filter(code = ids)
        item = query.last()
        url = "https://api.mymidjourney.ai/api/v1/midjourney/message/"
        headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ODQwMSwiZW1haWwiOiJsbGltb29haUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImxsaW1vb2FpQGdtYWlsLmNvbSIsImlhdCI6MTcwNTYwOTY3NH0.V17JuXug9v8klMenrpw6OGTiVsU8LANrHPBpD9IoCjI',
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url + item.code, headers=headers)
        response = response.json()
        if not 'uri' in response:
            return Response(response,status=status.HTTP_400_BAD_REQUEST) 
        wal = wals.first()
        wal.amount = wal.amount - 4
        wal.save()
        item.image = response['uri']
        item.save()
        serializer = FaceSwapedSerializer(item)
        return Response(serializer.data)

class ImagineResult(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, ids):
        if not request.user.is_authenticated:
            query = ImagineOrder.objects.filter(code = ids)
            item = query.last()
            url = "https://api.mymidjourney.ai/api/v1/midjourney/message/"
            headers = {
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ODQwMSwiZW1haWwiOiJsbGltb29haUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImxsaW1vb2FpQGdtYWlsLmNvbSIsImlhdCI6MTcwNTYwOTY3NH0.V17JuXug9v8klMenrpw6OGTiVsU8LANrHPBpD9IoCjI',
            'Content-Type': 'application/json'
            }

            response = requests.request("GET", url + item.code, headers=headers)
            response = response.json()
            return Response(response)
        wals = Package.objects.filter(user=request.user , expired = False, amount__gte=1)
        query = ImagineOrder.objects.filter(code = ids)
        if len(query) and query.last().progress == 100:
            if query.last().image:
                serializer = ImagineOrderSerializer(query.last())
                return Response(serializer.data)
        item = query.last()
        url = "https://api.mymidjourney.ai/api/v1/midjourney/message/"
        headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ODQwMSwiZW1haWwiOiJsbGltb29haUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImxsaW1vb2FpQGdtYWlsLmNvbSIsImlhdCI6MTcwNTYwOTY3NH0.V17JuXug9v8klMenrpw6OGTiVsU8LANrHPBpD9IoCjI',
        'Content-Type': 'application/json'
        }

        response = requests.request("GET", url + item.code, headers=headers)
        response = response.json()
        if not 'uri' in response:
            if 'error' in response:
                item.progress = 'incomplete'
                item.done = True
            elif 'progress' in response:
                item.percent = response['progress']
        else:
            if response['progress'] == 100:
                wal = wals.first()
                wal.amount = wal.amount - 1
                wal.save()
            item.result = [response['uri']]
            item.image = response['uri']
            if response['progress'] == 100:
                item.done = True
            item.bid =response['messageId']
            item.percent = response['progress']
            if 'buttons' in response:
                item.buttons = response['buttons']
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
            return Response('موجودی شما کافی نیست',status = status.HTTP_402_PAYMENT_REQUIRED)
        url = "https://api.mymidjourney.ai/api/v1/midjourney/button"

        payload = json.dumps({
        "messageId": f"{request.data['code']}",
        "button": f"{request.data['btn']}",
        })
        headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ODQwMSwiZW1haWwiOiJsbGltb29haUBnbWFpbC5jb20iLCJ1c2VybmFtZSI6ImxsaW1vb2FpQGdtYWlsLmNvbSIsImlhdCI6MTcwNTYwOTY3NH0.V17JuXug9v8klMenrpw6OGTiVsU8LANrHPBpD9IoCjI',
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

    def get(self, request, page):
        query = ImagineOrder.objects.filter(user = request.user, order=None).order_by('-id')[((int(page)-1)*5):(int(page) * 5)]
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


class ImageDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = ImageDetail.objects.all()
        serializer = OptionSerializer(query, many=True)
        return Response(serializer.data)


class AddDetails(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = AddDetail.objects.all()
        serializer = OptionSerializer(query, many=True)
        return Response(serializer.data)


class Mimics(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = Mimic.objects.all()
        serializer = OptionSerializer(query, many=True)
        return Response(serializer.data)


class Parameters(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = Parameter.objects.all()
        serializer = ParamSerializer(query, many=True)
        return Response(serializer.data)


class Sizes(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = Size.objects.all()
        serializer = OptionSerializer(query, many=True)
        return Response(serializer.data)


class Posts(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        query = Post.objects.all()
        for item in query:
            if len(item.content) > 1500:
                item.content = item.content[:1500] + ' ...'
        serializer = PostSerializer(query, many=True)
        return Response(serializer.data)
    
    def post(self, request, id):
        query = Post.objects.get(id = id)
        serializer = PostSerializer(query)
        return Response(serializer.data)