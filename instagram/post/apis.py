from rest_framework import mixins, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserSerializer
from utils.permissions import IsAuthorOrReadOnly
from .models import Post
from .serializer import PostSerializer


# class PostList(APIView):
#     """
#     List all posts or create a new post.
#
#     * Allow authenticated user to perform any request.
#     * Only safe methods are available for unauthenticated user.
#     """
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def get(self, request, *args, **kwargs):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request, *args, **kwargs):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostList(mixins.ListModelMixin,
#                mixins.CreateModelMixin,
#                generics.GenericAPIView):  # Order of inheritance is from right to left.
#     """
#     List all posts or create a new post.
#
#     * Allow authenticated user to perform any request.
#     * Only safe methods are available for unauthenticated user.
#     """
#     queryset = Post.objects.all()  # Keep the variable name, queryset.
#     serializer_class = PostSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def perform_create(self, serializer):
#         # Override perform_create() in CreateModelMixin.
#         # Assign user from request to author.
#         serializer.save(author=self.request.user)


class PostList(generics.ListCreateAPIView):
    """
    List all posts or create a new post.

    * Allow authenticated user to perform any request.
    * Only safe methods are available for unauthenticated user.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# class PostDetail(APIView):
#     """
#     Retrieve, update, delete a post in database
#
#     * Allow author to perform any request.
#     * Only safe method is available for who is not author.
#     """
#     permission_classes = (IsAuthorOrReadOnly,)
#
#     def get(self, request, *args, **kwargs):
#         post = Post.objects.get(pk=self.kwargs['pk'])
#         serializer = PostSerializer(post)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, *args, **kwargs):
#         post = Post.objects.get(pk=self.kwargs['pk'])
#         serializer = PostSerializer(post)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, *args, **kwargs):
#         post = Post.objects.get(pk=self.kwargs['pk'])
#         self.delete(post)
#         return Response(status=status.HTTP_204_NO_CONTENT)


class PostDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostLikeToggle(generics.GenericAPIView):
    queryset = Post.objects.all()

    # url 패턴에서 특정 포스트 객체를 가져오기 위한 그룹명을 지정한다.
    # lookup_url_kwarg = 'pk'

    def post(self, request, *args, **kwargs):
        # queryset에서 pk값으로 객체를 가져온다.
        obj = self.get_object()
        user = request.user
        # 유저의 좋아요 목록에 현재 포스트가 존재하는 경우, 해당 포스트를 제거한다.
        # like_status로 좋아요 상태를 표시한다.
        if user.like_posts.filter(pk=obj.pk):
            user.like_posts.remove(obj)
            like_status = False
        # 좋아요 포스트 목록에 없을 경우, 좋아요 목록에 추가한다.
        else:
            user.like_posts.add(obj)
            like_status = True
        # 유저와 포스트 그리고 유저가 포스트를 좋아하는지에 대한 정보를 JSON 형태로 응답한다.
        data = {
            'user': UserSerializer(user).data,
            'post': PostSerializer(obj).data,
            'result': like_status,
        }
        return Response(data)
