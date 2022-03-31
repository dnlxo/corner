from importlib.resources import contents
from xml.etree.ElementTree import Comment
from django.http import QueryDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q

from users.models import User, PreferLocation
from . import models, serializers
from django.core.paginator import Paginator

# /posts/home
class home_view(APIView):       #new/best_view
    def get(self, request):
        limit = request.GET.get('limit', None)
        order = request.GET.get('order', None)
        page = request.GET.get('page', None)
        if order == 'new' :
            posts = models.Post.objects.all().order_by("-create_at")
        elif order == 'best' :
            posts = models.Post.objects.all().order_by("-like_count", "-create_at")
        else :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if limit != None :
            paginator = Paginator(posts, limit)
            posts = paginator.get_page(page)
            serializer = serializers.PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
'''
class home_view2(APIView):      #prefer_location_view
     def get(self, request):
        limit = request.GET.get('limit', None)
        #order = request.GET.get('order', None)
        page = request.GET.get('page', None)
        user = get_object_or_404(User, pk=request.user.id)
        locaton = user.user_location
        #user.user_location.all()
        posts = models.Post.objects.filter(location=models.Post.district)
        #if user.user_location == district
        #posts = models.Post.objects.filter(district__in = prefer_location).order_by("-create_at")
        if limit != None :
            paginator = Paginator(posts, limit)
            posts = paginator.get_page(page)
        serializer = serializers.PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
'''

class home_view2(APIView):      #prefer_location_view
     def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        location = user.user_location.values('location')
        location = list(location)
        print(location)
        temp = []
        for i in location :
            temp.append(i['location'])
        print(temp)
        limit = request.GET.get('limit', None)
        order = request.GET.get('order', None)
        page = request.GET.get('page', None)
        if order == 'new' :
            posts = models.Post.objects.filter(district__in = temp).order_by("-create_at")
        elif order == 'best' :
            posts = models.Post.objects.filter(district__in = temp).order_by("-like_count", "-create_at")
        else :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if limit != None :
            paginator = Paginator(posts, limit)
            posts = paginator.get_page(page)
        serializer = serializers.PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class personal_view(APIView):       #following/likes_view
    def get(self, request):
        limit = request.GET.get('limit', None)
        order = request.GET.get('order', None)
        page = request.GET.get('page', None)
        user = get_object_or_404(User, pk=request.user.id)
        if order == 'following' :
            following = user.following.all()
            posts = models.Post.objects.filter(author__in = following).order_by("-create_at")
        elif order == 'likes' :
            likes = user.post_likes.all()
            posts = likes.order_by("-create_at")
        else :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if limit != None :
            paginator = Paginator(posts, limit)
            posts = paginator.get_page(page)
            serializer = serializers.PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class search_view(APIView):
    def post(self, request):
        search_word = request.data['search_word']
        posts = models.Post.objects.filter(Q(description__icontains=search_word) | Q(district__icontains=search_word) | Q(road_address__icontains=search_word)).distinct()
        serializer = serializers.PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# /posts/mypages
class mypages(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, pk=request.user.id)
            user.post_author.order_by("-create_at")
            serializer = serializers.MyPageAccountSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
       

class user_pages(APIView):
    def get(self, request, user_id):
        if request.user.is_authenticated:
            user = get_object_or_404(User, pk=user_id)
            user.post_author.order_by("-create_at")
            serializer = serializers.MyPageAccountSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


# /posts/3
class post_rud(APIView):
    def get(self, request, post_id):
        posts = models.Post.objects.filter(id = post_id)
        if posts:
            serializer = serializers.PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else : 
            return Response(request.data, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, post_id): # 넘겨줄거 (글)
        if request.user.is_authenticated:
            post = get_object_or_404(models.Post, pk=post_id)
            if request.user == post.author:
                serializer = serializers.PostValidSerializer(data=request.data)
                if serializer.is_valid():
                    post.description = serializer.data['description']
                    post.save()
                    #return Response(status=status.HTTP_200_OK)
                    serializer = serializers.PostSerializer(post)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, post_id):
        if request.user.is_authenticated:
            post = get_object_or_404(models.Post, pk=post_id)
            if request.user == post.author:
                post.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)        
            

# /posts
# 게시글 작성 시 넘겨줄 데이터 : (이미지,이미지,이미지,..., 글)
class post_create(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            user = get_object_or_404(User, pk=request.user.id)
            serializer = serializers.PostValidSerializer(data=request.data)
            if serializer.is_valid():
                description = serializer.data['description']
                latitude = serializer.data['latitude']
                longitude = serializer.data['longitude']
                road_address = serializer.data['road_address']
                district = serializer.data['district']
                alias = serializer.data['alias']
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            before_save = []
            imglist = request.data.getlist('image')
            q = QueryDict.copy(request.data)
            for img in imglist:
                q.__setitem__('image', img)
                serializer = serializers.PostImageSerializer(data=q)
                if serializer.is_valid():
                    before_save.append(img)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                new_post = models.Post(
                    author = user,
                    description = description,
                    latitude = latitude,
					longitude = longitude,
					road_address = road_address,
                    district = district,
					alias = alias
                )
                new_post.save()
                post = models.Post.objects.latest('id')
                for i in before_save:
                    new_postimg = models.PostImage(
                        posts = post,
                        image = i,
                    )
                    new_postimg.save()
                serializer = serializers.PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
                #return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class comment_cd(APIView):
    def post(self, request, post_id):
        if request.user.is_authenticated:
            post = get_object_or_404(models.Post, pk=post_id)
            serializer = serializers.CommentValidSerializer(data=request.data)
            if serializer.is_valid():
                contents = serializer.data['contents']
                new_comment = models.Comment(
                    author = request.user,
                    posts = post,
                    contents = contents
                )
                new_comment.save()
                serializer = serializers.PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, post_id, comment_id):
        if request.user.is_authenticated:            
            comment = get_object_or_404(models.Comment, pk=comment_id)
            post = get_object_or_404(models.Post, pk=post_id)
            if request.user == comment.author:
                comment.delete()
                serializer = serializers.PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class recomment_cd(APIView):
    def post(self, request, post_id, comment_id):
        if request.user.is_authenticated:
            comment = get_object_or_404(models.Comment, pk=comment_id)
            serializer = serializers.CommentValidSerializer(data=request.data)
            if serializer.is_valid():
                contents = serializer.data['contents']
                new_recomment = models.ReComment(
                    author = request.user,
                    comment = comment,
                    contents = contents
                )
                new_recomment.save()
                post = get_object_or_404(models.Post, pk=post_id)
                serializer = serializers.PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, post_id, recomment_id):
        if request.user.is_authenticated:
            recomment = get_object_or_404(models.ReComment, pk=recomment_id)
            post = get_object_or_404(models.Post, pk=post_id)
            if request.user == recomment.author:
                recomment.delete()
                serializer = serializers.PostSerializer(post)
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class post_like(APIView):
    def post(self, request, post_id):
        if request.user.is_authenticated:
            post = get_object_or_404(models.Post, pk=post_id)
            if post.likes.filter(pk = request.user.pk).exists():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            post.like_count = post.likes.count()
            post.save()
            #return Response(status=status.HTTP_200_OK)
            serializer = serializers.PostSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, post_id):
        posts = models.Post.objects.filter(id = post_id)
        if posts:
            serializer = serializers.LikeListSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else : 
            return Response(status=status.HTTP_404_NOT_FOUND)