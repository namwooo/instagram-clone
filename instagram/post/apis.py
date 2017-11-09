from django.http import Http404
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post
from .serializer import PostSerializer


class PostList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):  # 상속 순서는 오른쪽 부터 왼쪽 방향이다. 베이스가 되는 부모 클래스를 오른쪽에 배치해주자.
    queryset = Post.objects.all()  # queryset 이란 변수 이름은 GenericAPIView에 정의되어 있기 떄문에 굳이 바꿔 주진 말자.
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # self.create 안에 정의 되어 있는 save()를 오버라이드 한다.
        # author에 요청을 보낸 유저를 할당한다.
        serializer.save(author=self.request.user)


# class PostList(APIView):
#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
