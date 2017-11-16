import filecmp
import tempfile
from random import randint

import io

import os
from django.contrib.auth import get_user_model
from django.core.files import File
from django.test import RequestFactory
from django.urls import resolve
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient

from config import settings
from member.models import User
from post.apis import PostList
from post.models import Post

User = get_user_model()


class PostListViewTest(APITestCase):
    URL_API_POST_LIST_NAME = 'api-post'
    URL_API_POST_LIST = '/api/post/'
    VIEW_CLASS = PostList

    @staticmethod
    def create_user(username='dummy'):
        return User.objects.create_user(username=username, age=0)

    @staticmethod
    def create_post(author=None):
        return Post.objects.create(author=author, photo=File(io.BytesIO()))

    def test_post_list_url_name_reverse(self):
        url = reverse(self.URL_API_POST_LIST_NAME)
        self.assertEqual(url, self.URL_API_POST_LIST)

    def test_post_list_resolve(self):
        resolver_match = resolve(self.URL_API_POST_LIST)
        self.assertEqual(resolver_match.url_name, self.URL_API_POST_LIST_NAME)

        # factory = APIRequestFactory()
        # user = User.objects.get(username='namwoo')
        # view = PostList.as_view()
        #
        # request = factory.get('/api/post/')
        # force_authenticate(request, user=user)
        # response = view(request)

    def test_get_post_list(self):
        user = self.create_user()
        num = randint(0, 20)
        for i in range(num):
            self.create_post(author=user)
        url = reverse(self.URL_API_POST_LIST_NAME)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), num)
        self.assertEqual(len(response.data), num)

        for i in range(num):
            cur_post_data = response.data[i]
            self.assertIn('id', cur_post_data)
            self.assertIn('author', cur_post_data)
            self.assertIn('photo', cur_post_data)
            self.assertIn('created_date', cur_post_data)

    def test_get_post_list_exclude_author_is_none(self):
        user = self.create_user()
        num_author_none_posts = randint(1, 10)
        num_posts = randint(11, 20)
        for i in range(num_author_none_posts):
            self.create_post()
        for i in range(num_posts):
            self.create_post(author=user)

        response = self.client.get(self.URL_API_POST_LIST)
        self.assertEqual(len(response.data), num_posts)

    def test_create_post(self):
        user = self.create_user()
        # 유저를 client로 강제로 인증
        self.client.force_authenticate(user=user)
        path = os.path.join(settings.STATIC_DIR, 'test', 'MB2.JPG')
        with open(path, 'rb') as photo:
            response = self.client.post('/api/post/', {
                'photo': photo,
            })
        # response 상태 코드가 201인지 확인한다.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 생성된 post가 1개인지 확인한다.
        self.assertEqual(Post.objects.count(), 1)
        # 두 파일이 같은지 확인한다.
        post = Post.objects.get(pk=response.data['id'])  # id로 생성된 포스트를 가져온다.
        # path에 있는 기존 파일과 저장된 파일을 filecmp로 비교한다.
        self.assertTrue(filecmp.cmp(path, post.photo.file.name))  # FieldFile.name에 파일 경로가 저장되어 있다.
