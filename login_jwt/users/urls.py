from django.urls import path
from django.conf.urls import url
from django.urls import include
from .views import *
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
urlpatterns = [
        url(r'^sms/',SmsView.as_view()),
        url(r'^register/',RegisterView.as_view()),
        # url(r'^login/',LoginView.as_view()),
        url(r'^index/',Order.as_view()),
        url(r'^api-jwt-auth/',obtain_jwt_token),  # jwt的认证接口（路径可自定义任意命名）
]