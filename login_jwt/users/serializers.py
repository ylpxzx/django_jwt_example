import re
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from .models import LoginUser
from django.core.cache import cache


def re_phone(phone):
    ret = re.match(r"^1[1-8]\d{9}$", phone)
    if ret:
        return True
    return False

class SmsSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)

    class Meta:
        model = LoginUser
        fields = ('phone',)

    def validate_phone(self,phone):
        '''
        手机号验证
        :return:
        '''

        if LoginUser.objects.filter(phone_numbers=phone).count():
            raise ValidationError('手机号码已经注册')

        if not re_phone(phone):
            raise ValidationError('手机号码格式错误')

        return phone

class RegisterSerializer(serializers.ModelSerializer):
    phone_numbers = serializers.CharField(required=True)
    pwd2 = serializers.CharField(max_length=256,min_length=4,write_only=True)
    code = serializers.CharField(required=True)

    class Meta:
        model = LoginUser
        fields = ('username', 'password', 'pwd2', 'phone_numbers', 'code')

    def validate(self, attrs):
        print(attrs['code'])
        if not re_phone(attrs['phone_numbers']):
            raise ValidationError('手机号码格式错误')

        sms_code = cache.get(attrs['phone_numbers'])
        print('从redis取出的code:',sms_code)
        if str(sms_code) != attrs['code']:
            raise ValidationError('验证码错误或过期')
        if attrs['pwd2'] != attrs['password']:
            raise ValidationError('两次密码输入不一致')
        del attrs['pwd2']
        del attrs['code']
        attrs['password'] = make_password(attrs['password'])
        return attrs


# class LoginSerializer(serializers.ModelSerializer):
#     phone_numbers = serializers.CharField(required=True)
#     password = serializers.CharField(required=True)
#     class Meta:
#         model = LoginUser
#         fields = ('phone_numbers', 'password')
#     def validate(self, attrs):
#         user = LoginUser.objects.filter(phone_numbers=attrs['phone_numbers']).first()
#         print(user)
#         if not user:
#             raise ValidationError('该手机号未注册')
#         if not user.check_password(attrs['password']):
#             raise ValidationError('密码不正确')
#         return attrs


class OrderSerializer(serializers.Serializer):
    title = serializers.CharField()
    name = serializers.CharField()