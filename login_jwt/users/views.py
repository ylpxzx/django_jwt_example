import random
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
# from .models import UserToken
from rest_framework_jwt.settings import api_settings
from conf.aliyun_api import AliYunSms

class SmsView(APIView):
    '''
    发送验证码
    '''
    authentication_classes = []
    permission_classes = []
    def post(self,request, *args, **kwargs):
        serializer = SmsSerializer(data=request.data)
        if serializer.is_valid():
            code = (random.randint(1000, 100000))

            response = {
                'msg':'手机号格式正确，已发送验证码，注意查收',
                'next_url':{
                    'url':'api/register',
                    'methond':'POST',
                    'form-data':{
                        'username':'用户名',
                        'phone':'手机号',
                        'password':'密码',
                        'password2':'确认密码',
                        'code':'验证码'
                    }
                }
            }
            phone = serializer.data['phone']
            response['phone'] = phone
            response['code'] = code

            cache.set(phone, code, 150)

            # # 发送短信验证
            # params = "{'code':%d}" % code
            # sms_obj = AliYunSms(phone, params)
            # res_obj = sms_obj.send()
            # print('发送结果：',res_obj)

            return Response(response,status=200)
        return Response(serializer.errors,status=400)


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self,request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # phone_numbers = serializer.validated_data['phone_numbers']
            # user = LoginUser.objects.get(phone_numbers=phone_numbers)
            # jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            # jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # # 往添加token的数据
            # payload = jwt_payload_handler(user)  # 这里需要修改为自己的数据
            # # 生成对token进行加密
            # token = jwt_encode_handler(payload)
            # UserToken.objects.update_or_create(user=user, defaults={'token': token})
            response = {
                'msg':'用户注册成功',
                'next_url':{
                    'url':'api/api-jwt-auth/',
                    'form-data':{
                        'username': '用户名',
                        'password': '密码'
                    }
                }
            }
            return Response(response,status=200)
        return Response(serializer.errors,status=400)

# 也可以自定义登录视图
# class LoginView(APIView):
#     authentication_classes = []
#     permission_classes = []
#     def post(self,request, *args, **kwargs):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = LoginUser.objects.get(phone_numbers=serializer.data['phone_numbers'])
#             jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#             jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#             # 往添加token的数据
#             payload = jwt_payload_handler(user)  # 这里需要修改为自己的数据
#             # 生成对token进行加密
#             token = jwt_encode_handler(payload)
#             UserToken.objects.update_or_create(user=user, defaults={'token': token})
#             response = {
#                 'msg':'登录成功,认证令牌token',
#                 'token':token
#             }
#             return Response(response,status=200)
#         return Response(serializer.errors,status=400)

class Order(APIView):
    def get(self, request):
        ret = {'code': 1000, 'msg': '成功GET进来了', 'data': None}
        ret['data'] = '欢迎使用本系统'
        return Response(ret)

    def post(self,request):
        order = OrderSerializer(data=request.data)
        if order.is_valid():
            print(order)
            ret = {'code': 1000, 'msg': '成功POST进来了', 'data': order.data}
            return Response(ret)
        return Response(order.errors,status=400)

# 采用JWT的JSONWebTokenAuthentication认证时，访问Order视图时时，要加上请求头，请求头的键为：authorization，值为：jwt空格token
# 采用自定义认证Authtication时，访问Order时，要加上请求头，请求头键为：token,值为：获取到的token