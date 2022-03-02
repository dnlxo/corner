from django.urls import path
from . import views

urlpatterns = [

    # /posts/home&order=new
    path('/home', views.home_view.as_view()),
    # /posts POST요청
    path('', views.post_create.as_view()),

    # /posts/3 DELETE요청 (3번 게시물 삭제)
    # /posts/3 GET요청 (3번 게시물 보기)
    # /posts/3 PUT요청 (3번 게시물 수정)
    path('/<int:post_id>', views.post_rud.as_view()),

    # /posts/3/likes POST요청 (3번 게시물 좋아요 누르기, 좋아요 취소)
    path('/<int:post_id>/likes', views.post_like.as_view()),

    # /posts/3/comments POST요청 (3번 게시물에 댓 달기)
    path('/<int:post_id>/comments', views.comment_cd.as_view()),

    # /posts/comments/12 DELETE요청 (12번 id를 가진 댓글 삭제)
    path('/comments/<int:comment_id>', views.comment_cd.as_view()),

    # /posts/comments/12/recomments POST요청 (12번 id를 가진 댓글에 대댓글 추가)
    path('/comments/<int:comment_id>/recomments', views.recomment_cd.as_view()),

    # /posts/recomments/12 DELETE요청 (12번 id를 가진 대댓글 삭제)
    path('/recomments/<int:recomment_id>', views.recomment_cd.as_view()),
]
