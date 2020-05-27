from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from users.models import UserToken

# 实现自定义的认证类
class Authtication(BaseAuthentication):

    def authenticate(self, request):
            print('自定义认证')
            print(request.META.get('HTTP_TOKEN', None))
            print(request._request.GET.get('token'))

            # token = request._request.GET.get('token')  # 将token放置在GET请求参数
            token = request.META.get('HTTP_TOKEN', None) # 将token放置在请求头
            if token:
                    # 检查用户的 token 是否合法
                    token_obj = UserToken.objects.filter(token=token).first()
                    if not token_obj:
                            raise exceptions.AuthenticationFailed('用户认证失败')

                    # 在 rest_framework 内部会将这两个字段赋值给request以供后续调用
                    return (token_obj.user, token_obj)
            else:
                    raise exceptions.AuthenticationFailed('请求头未设置token')