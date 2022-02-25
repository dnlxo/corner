from importlib.resources import contents
from xml.etree.ElementTree import Comment
from django.http import QueryDict
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from users.models import User
from . import models, serializers

# /posts/
# 로그인 되어있다면? 홈화면 보여준다. (ex_인스타 메인 피드.. (내가 팔로우하는 사람들 게시물이 뜬다.))
# 우리는 ?
'''
class main(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            comment_form = CommentForm()

            user = get_object_or_404(user_model, pk=request.user.id)
            following = user.following.all()
            posts = models.Post.objects.filter(
                Q(author__in=following) | Q(author=user)
            ).order_by("-create_at")

            serializer = serializers.PostSerializer(posts, many=True)
            print(serializer.data)

            return render(
                request,
                'posts/main.html',
                {"posts": serializer.data, "comment_form": comment_form}
            )
'''

# /posts/3
class post_ru(APIView):
    def get(self, request, post_id):
        posts = models.Post.objects.filter(id = post_id)
        if posts:
            serializer = serializers.PostSerializer(posts, many=True)
            return Response(serializer.data)
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
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
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
                )
                new_post.save()
                post = models.Post.objects.latest('id')
                for i in before_save:
                    new_postimg = models.PostImage(
                        posts = post,
                        image = i,
                    )
                    new_postimg.save()
                return Response(status=status.HTTP_201_CREATED)
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
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, comment_id):
        if request.user.is_authenticated:
            comment = get_object_or_404(models.Comment, pk=comment_id)
            if request.user == comment.author:
                comment.delete()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)