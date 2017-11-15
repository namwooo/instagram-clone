from typing import NamedTuple

from django.contrib.sites import requests
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from member.models import User
from member.serializers import UserSerializer, SignupSerializer


class Login(APIView):
    """
    Create or get token for authenticated user.

    * Requires username and password.
    """

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response(
                {'error': "username/password are required!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if user:
            token, token_created = Token.objects.get_or_create(user=user)

            data = {
                'token': token.key,
                'user': UserSerializer(user).data
            }

            return Response(data, status=status.HTTP_200_OK)

        data = {
            'error': "Invalid credentials!",
        }

        return Response(data, status=status.HTTP_401_UNAUTHORIZED)


# class Signup(APIView):
#     """
#     Create a new user.
#
#     * Requires unique username, age and password confirmation.
#     """
#
#     def post(self, request, *args, **kwargs):
#         if not request.data:
#             return Response(
#                 {'error': "username/password are required!"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#
#         username = request.data['username']
#         password1 = request.data['password1']
#         password2 = request.data['password2']
#         age = request.data['age']
#
#         if User.objects.filter(username=username).exists():
#             return Response({'message': "username already exists!"})
#         elif    password1 != password2:
#             return Response({'message': "password doesn't match!"})
#
#         user = User.objects.create_user(
#             username=username,
#             password=password1,
#             age=age,
#         )
#
#         data = {
#             'user': UserSerializer(user).data
#         }
#
#         return Response(data, status=status.HTTP_201_CREATED)

class Signup(APIView):
    """
    Createa a new user using SignupSerializer.

    * Requires validation in SignupSerializer.
    """

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class FacebookLogin(APIView):
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
            app_id = settings.FACEBOOK_APP_ID
            app_secret_key = settings.FACEBOOK_SECRET_KEY
            app_access_token = f'{app_id}|{app_secret_key}'

            url_debug_token = 'https://graph.facebook.com/debug_token'
            params_debug_token = {
                'input_token': token,
                'access_token': app_access_token,
            }
            response = requests.get(url_debug_token, params_debug_token)

            return DebugTokenInfo(**response.json()['data'])

            # request.data로 전달된 access_token값을 페이스북API쪽에 debug요청, 결과를 받아옴

        debug_token_info = get_debug_token_info(request.data['access_token'])

        if debug_token_info.user_id != request.data['facebook_user_id']:
            raise APIException('페이스북 토큰의 사용자와 전달받은 facebook_user_id가 일치하지 않음')

        if not debug_token_info.is_valid:
            raise APIException('페이스북 토큰이 유효하지 않음')

        # FacebookBackend를 사용해서 유저 인증
        user = authenticate(facebook_user_id=request.data['facebook_user_id'])
        # 인증에 실패한 경우 페이스북유저 타입으로 유저를 만들어줌
        if not user:
            user = User.objects.create_user(
                username=f'fb_{request.data["facebook_user_id"]}',
                user_type=User.USER_TYPE_FACEBOOK,
            )
        data = {
            'user': UserSerializer(user).data,
            'token': user.token,
        }
        # 유저 시리얼라이즈 결과를 Response
        return Response(UserSerializer(user).data)
