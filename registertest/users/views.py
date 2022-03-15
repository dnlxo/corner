from django.contrib.auth import authenticate, login
from django.http import QueryDict
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer, UserValidSerializer, PreferLocationSerializer
from .models import PreferLocation, User
from django.contrib.auth.hashers import make_password

class main(APIView):
    def get(self, request):
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(request.data, status=status.HTTP_200_OK)

        else:
            return Response(request.data, status=status.HTTP_403_FORBIDDEN)


class signup(APIView):
    def post(self, request):
        serializer = UserValidSerializer(data=request.data)
        if serializer.is_valid():
            print(request.data)
            if User.objects.filter(email=request.data['email']).exists():
                return Response({'message': 'USER_ALREADY_EXISTS'}, status=409)
            if User.objects.filter(username=request.data['username']).exists():
                return Response({'message': 'USER_ALREADY_EXISTS'}, status=409)
            else :
                email = serializer.data['email']
                username = serializer.data['username']
                password = make_password(serializer.data['password'])
            
            before_save = []
            locationlist = request.data.getlist('location')
            q = QueryDict.copy(request.data)
            for locations in locationlist:
                q.__setitem__('location', locations)
                serializer = PreferLocationSerializer(data=q)
                if serializer.is_valid():
                    before_save.append(locations)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                new_user = User(
                    email = email,
                    username = username,
                    password = password
                    )
            new_user.save()
            user = User.objects.latest('id')
            for i in before_save:
                new_location = PreferLocation(
                    user= user,
                    location = i
                    )
                new_location.save()
            return Response(request.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class user_follow(APIView):
    def post(self, request, user_id):
        if request.user.is_authenticated:
            logined_user = get_object_or_404(User, pk=request.user.id)
            user = get_object_or_404(User, pk=user_id)
            if logined_user != user :
                if logined_user.following.filter(pk = user.pk).exists() :
                    logined_user.following.remove(user)
                    user.followers.remove(logined_user)
                else:
                    logined_user.following.add(user)
                    user.followers.add(logined_user)

                logined_user.following_count = logined_user.following.count()
                logined_user.save()
                user.followers_count = user.followers.count()
                user.save()
                return Response(status=status.HTTP_200_OK)
            else :
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)