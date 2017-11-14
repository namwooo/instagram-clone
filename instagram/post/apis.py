from rest_framework import mixins, generics, permissions
from rest_framework.response import Response

from member.serializers import UserSerializer
from utils.permissions import IsAuthorOrReadOnly
from .models import Post
from .serializer import PostSerializer


class PostList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):  # 상속 순서는 오른쪽 부터 왼쪽 방향이다. 베이스가 되는 부모 클래스를 오른쪽에 배치해주자.
    queryset = Post.objects.all()  # queryset 이란 변수 이름은 GenericAPIView에 정의되어 있기 떄문에 굳이 바꿔 주진 말자.
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

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
