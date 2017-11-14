from typing import NamedTuple

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

from member.models import User
from member.serializers import UserSerializer, SignupSerializer


# class Login(APIView):
#     '''
#     BasicAuthetication으로 사용자 인증 후, 로그인 한다.
#     '''
#
#     def post(self, request, *args, **kwargs):
#         # request 헤더를 통해 들어온 username과 password를 가져온다.
#         username = request.META.get('HTTP_USERNAME')
#         password = request.META.get('HTTP_PASSWORD')
#
#         # authenticate() 메소드는 인증에 성공하면 해당 User 객체를 반환한다.
#         user = authenticate(
#             username=username,
#             password=password,
#         )
#
#         # 인증에 성공한 경우, user를 serialize한 데이터와 200 status를 보낸다.
#         if user:
#             data = {
#                 'user': UserSerializer(user).data
#             }
#             return Response(data, status=status.HTTP_200_OK)
#
#         # 인증에 실패한 경우, 요청 받은 username과 password, 401 status를 보낸다.
#         data = {
#             'username': username,
#             'password': password,
#         }
#         return Response(data, status=status.HTTP_401_UNAUTHORIZED)

class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if user:
            token, token_created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'user': UserSerializer(user).data,
            }
            return Response(data, status=status.HTTP_200_OK)

        data = {
            'username': username,
            'password': password,
        }

        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


class Signup(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exist'})

        user = User.objects.create_user(
            username=username,
            password=password,
        )


class Signup(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class FacebookLogin(APIView):
    class AccessTokenInfo(NamedTuple):
        access_token: str
        token_type: str
        expires_in: int

    def post(self, request, *args, **kwargs):
        class DebugTokenInfo(NamedTuple):
            app_id: str
            application: str
            expires_at: int
            is_valid: bool
            issued_at: int
            scopes: list
            type: str
            user_id: str

        def get_debug_token_info(token):
            url_debug_token = 'https://graph.facebook.com/debug_token'
            params_debug_token = {
                'input_token': access_token,
                'access_token': app_access_token,
            }
            response = requests.get(url_debug_token, params_debug_token)

            return self.DebugTokenInfo(**response.json()['data'])
