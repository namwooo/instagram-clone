from rest_framework import mixins, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserSerializer
from post.paginator import StandardResultSetPagination
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
    pagination_class = StandardResultSetPagination

# class PostDetail(APIView):
#     """
#     Retrieve, update, delete a post.
#
#     * Allow author to perform any request.
#     * Only safe method is available for who is not author.
#     """
#     permission_classes = (IsAuthorOrReadOnly,)
#
#     def get(self, request, *args, **kwargs):
#         post = Post.objects.filter(pk=self.kwargs['pk'])
#         serializer = PostSerializer(post)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, *args, **kwargs):
#         post = Post.objects.filter(pk=self.kwargs['pk'])
#         serializer = PostSerializer(post)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, *args, **kwargs):
#         post = Post.objects.filter(pk=self.kwargs['pk'])
#         self.delete(post)
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class PostDetail(mixins.RetrieveModelMixin,
#                  mixins.UpdateModelMixin,
#                  mixins.DestroyModelMixin,
#                  generics.GenericAPIView):
#     """
#     Retrieve, update, delete a post.
#
#     * Allow author to perform any request.
#     * Only safe method is available for who is not author.
#     """
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (IsAuthorOrReadOnly,)
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, delete a post.

    * Allow author to perform any request.
    * Only safe method is available for who is not author.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class PostLikeToggle(generics. GenericAPIView):
    """
    Toggle to mark 'like' on a post.
    """
    queryset = Post.objects.all()

    # Designate a group name from url to lookup post object.
    # lookup_url_kwarg = '<group_name>' ex) 'pk'

    def post(self, request, *args, **kwargs):
        # get an object looking up with 'pk' from queryset.
        obj = self.get_object()
        user = request.user
        # if the post exists in user's like_post list,
        # remove it from the list and put False to like_status
        if user.like_posts.filter(pk=obj.pk):
            user.like_posts.remove(obj)
            like_status = False
        else:
            user.like_posts.add(obj)
            like_status = True
        data = {
            'user': UserSerializer(user).data,
            'post': PostSerializer(obj).data,
            'result': like_status,
        }
        return Response(data)
