from member.models import User


class FacebookLoginBackend(object):
    def authenticate(self, request, facebook_user_id):
        try:
            user = User.objects.get(username=f'fb_{facebook_user_id}')
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
