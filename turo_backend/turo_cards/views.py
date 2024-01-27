# from django.shortcuts import render,redirect
from django.http import HttpResponse

from .serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import *
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from django.db.models import Q

import time
# Create your views here.


@api_view(['GET'])
def Home(request):
    return Response({"msg":"success"})


@api_view(['POST'])
@permission_classes([])
def createUser(request):
    print(request.data)

    serializer = UserSerializer(data=request.data)
    print("Hello")
    if not serializer.is_valid():
        print(serializer.errors)
        return Response({'error':400 , 'error' : 'Someting went wrong'})
    else:
        serializer.save()
        return Response({'success':200,'msg':'user created successfully'})


@api_view(['POST'])
@permission_classes([])
def loginUser(request):
    try:
        serializer = LoginSerializer(data=request.data)
        if  serializer.is_valid():
            email = serializer.data['email']
            password=serializer.data['password']            

            print(1)
            temp = User.objects.get(email=email)
            print(temp.username)
            if temp:
                user=authenticate(username=temp.username,password=password)
                print(2)
                refresh = RefreshToken.for_user(user)
                print(3)
                return Response({
                    'user':serializer.data['email'],
                    'success':200,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({"error":"Invalid Credentials"})
        
        else:
            return Response({
                'status':400,
                'error':'Invalid Credentials'
            })
    except Exception as e:
        return Response({'error':e})
    

class turoCards(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        abc=request.user
        print(abc)
        userdata=User.objects.get(username=request.user)
        id=userdata.id
        print(id)
        data1=TuroCards.objects.filter(user_id=id).values()
        data2=TuroCards.objects.filter(~Q(user_id=id)).values()
        print(data1)
        print(type(data1),data1)
        # if data and data !=-1:
        #     serializer = TuroCardsSerializer(data=data,many=True)
            # print(type(serializer))
            # if not serializer.is_valid(partial=True):
            #     print(serializer.data)
            #     print(serializer.errors)
            #     return Response({'error':400 , 'msg' :'something went wrong' })
            # else:
            #     print(serializer.data)
            #     print(serializer.errors)
            #     return Response({'success':200,'data':serializer.data})
       
        return Response({"data1":data1,"data2":data2,"user":request.user.username})
            # data['user']=request.user
            # return Response({'data':data, 'abc':abc})

            
    
    def post(self, request):
        print(request.data)
        userdata=User.objects.get(username=request.user)
        id=userdata.id
        formData=request.data
        if formData:
            data = TuroCards.objects.create(user_id =userdata ,username=formData['username'],title=formData['title'],description=formData['description'],card_no = formData['card_no'],status=formData['status'],image=formData['image'])

            if(data):
                return Response({"success":200,"msg":"Created Successfully"})
            else:
                return Response({"error":400,"msg":"Something went wrong"})
        else:
            return Response({
                'status':400,
                'error':'Invalid Credentials'
            })

@api_view(['POST'])
def likeStatus(request):
    usr=str(request.user.username)
    print(usr)
    card=TuroCards.objects.get(id=request.data['card_id'])
    like=eval(card.likes)
    if usr in like:
        like.remove(usr)
        card.likes_count -= 1
    else:
        like.append(usr)
        card.likes_count += 1
    
    card.likes=like
    print(card.likes)
    card.save()
    return Response({"success":200})

@api_view(['GET'])
def commentCard(request,id):
    card=TuroCards.objects.filter(id=id).values()
    temp=card[0]
    list_of_users=eval(temp['likes'])
    return Response({"card":card,"users":list(list_of_users),"user":request.user.username})



@api_view(['POST'])
def addComment(request):
    usr=request.user.username
    userdata=User.objects.get(username=request.user)
    id=userdata.id
    card=TuroCards.objects.get(id=int(request.data['card_id']))
    comments=eval(card.comments)
    
    obj={"username":usr,"comment" : request.data['comment'],"time": int(time.time())}
    comments.insert(0,obj)

    card.comments=comments
    print(card.comments)
    card.save()
    return Response({"success":200})



@api_view(['POST'])
def RegisterSwapRequest(request):
    print(request.data)
    sender=TuroCards.objects.get(id=int( request.data['sender']))
    reciever=TuroCards.objects.get(id=int( request.data['receiver']))
    print(reciever)
    print(sender)
    print(reciever.username)
    if SwappingRequest.objects.filter(senderCard=request.data['sender'],receiverCard=request.data['receiver']).exists():
        return Response({"Error":"This request is already made."})
    else:
        SwappingRequest.objects.create(senderUser=sender.username,receiverUser=reciever.username,senderCard=request.data['sender'],receiverCard=request.data['receiver'])
        return Response({"status":200,"msg":"request made successfully"})
    
@api_view(['GET'])
def AllSwapRequests(request):
    username=request.user.username
    print(username)
    data1 = SwappingRequest.objects.filter(senderUser=username).values()
    print(data1)
    data2 = SwappingRequest.objects.filter(receiverUser=username).values()
    print(data2)
    return Response({"send":data1,"receive":data2})

@api_view(['POST'])  
def SwapCardDetails(request):
    card1=TuroCards.objects.filter(id=request.data['senderCard']).values()
    card2=TuroCards.objects.filter(id=request.data['receiverCard']).values()
    return Response({"senderCard":card1,"receiverCard":card2})

@api_view(['POST'])  
def CancelSwapRequest(request):
    print(request.data['id'])
    try:
        res=SwappingRequest.objects.filter(id=request.data['id']).delete()
        return Response({"success":200})
    except:
        return Response({"error":"Something went wrong"})
    
@api_view(['POST'])     
def AcceptSwapRequest(request):
    print(request.data)
    swap=SwappingRequest.objects.get(id=request.data['id'])
    suser=User.objects.get(username=swap.senderUser)
    ruser=User.objects.get(username=swap.receiverUser)

    data1=TuroCards.objects.get(id=swap.senderCard)
    data1.user_id=ruser
    data1.username=swap.receiverUser
    data1.save()

    data2=TuroCards.objects.get(id=swap.receiverCard)
    data2.user_id=suser
    data2.username=swap.senderUser
    data2.save()

    SwappingRequest.objects.filter(id=request.data['id']).delete()
    return Response({"msg":"successfully swapped the card"})