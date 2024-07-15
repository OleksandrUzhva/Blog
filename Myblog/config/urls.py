
from django.contrib import admin
from django.urls import path
from user.api import UserAPI, UserRetrieveAPI
from blog.api import PostCreateAPIView, CommentCreateAPIView
from rest_framework_simplejwt.views import token_obtain_pair 


urlpatterns = [
    path('admin/', admin.site.urls),
    #users
    path("user/", UserAPI.as_view()),
    path("user/<int:id>", UserRetrieveAPI.as_view()),
    #posts
    path('posts/', PostCreateAPIView.as_view()),
    #comments
    path('comments/', CommentCreateAPIView.as_view()),
    #auth
    path("auth/token/", token_obtain_pair),
]
