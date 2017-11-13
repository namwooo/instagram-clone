from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.compat import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserSerializer


class Login(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(
            username=username,
            password=password,
        )

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
