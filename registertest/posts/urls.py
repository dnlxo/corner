from django.urls import path
from . import views

urlpatterns = [
    # /posts
    # path('', views.main.as_view()),

    # /posts/create POST요청
    path('/create', views.post_create.as_view()),

    # /posts/3 GET요청 (3번 게시물 보기)
    path('/<int:post_id>', views.post_ru.as_view()),

    # /posts/3 PUT요청 (3번 게시물 수정)
    path('<int:post_id>', views.post_ru.as_view()),

    # /posts/3/comment POST요청 (3번 게시물에 댓 달기)
    path('/<int:post_id>/comment', views.comment_cd.as_view()),

    # /posts/comment/12 DELETE요청 (12번 id를 가진 댓글 삭제)
    path('/comment/<int:comment_id>', views.comment_cd.as_view()),
]