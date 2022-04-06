from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from posts.views import mypages, user_pages

urlpatterns = [
    path('login', views.main.as_view()),
    path('logout', auth_views.LogoutView.as_view()),
    path('signup', views.signup.as_view()),
    # /api/users/15/follow
    path('users/<int:user_id>/follow', views.user_follow.as_view()),
    # /api/users/15     GET방식 15번 유저페이지로
    path('users/<int:user_id>', user_pages.as_view()),
    # /api/mypages       GET방식 마이페이지로 이동
    path('mypages', mypages.as_view()),
    path('users/search', views.search_user.as_view()),
    path('<int:user_id>/username_edit', views.username_edit.as_view()),
    path('<int:user_id>/preferlocation_edit', views.preferlocation_edit.as_view()),
    path('withdrawal', views.withdrawal.as_view())

]