from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [

    # /api/posts/home 홈피드 보여주기 (order=&limit=&page=)
    path('/home', views.home_view.as_view()),
    #path('/home2', views.home_view2.as_view()),
    path('/likes_view', views.personal_view.as_view()),



    # /api/posts POST요청
    path('', views.post_create.as_view()),

    # /api/posts/3 DELETE요청 (3번 게시물 삭제)
    # /api/posts/3 GET요청 (3번 게시물 보기)
    # /api/posts/3 PUT요청 (3번 게시물 수정)
    path('/<int:post_id>', views.post_rud.as_view()),

    # /api/posts/3/likes POST요청 (3번 게시물 좋아요 누르기, 좋아요 취소)
    path('/<int:post_id>/likes', views.post_like.as_view()),

    # /api/posts/3/comments POST요청 (3번 게시물에 댓 달기)
    path('/<int:post_id>/comments', views.comment_cd.as_view()),

    # /api/posts/comments/12 DELETE요청 (12번 id를 가진 댓글 삭제)
    path('/<int:post_id>/comments/<int:comment_id>', views.comment_cd.as_view()),

    # /api/posts/comments/12/recomments POST요청 (12번 id를 가진 댓글에 대댓글 추가)
    path('/<int:post_id>/comments/<int:comment_id>/recomments', views.recomment_cd.as_view()),

    # /api/posts/recomments/12 DELETE요청 (12번 id를 가진 대댓글 삭제)
    path('/<int:post_id>/recomments/<int:recomment_id>', views.recomment_cd.as_view()),
    #path('/<int:post_id>/comments/<int:comment_id>/recomments/<int:recomment_id>', views.recomment_cd.as_view()),

]
