from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login

User = get_user_model()


class SignUpForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이름'

            }
        )
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '성'

            }
        )
    )

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '사용자 이름'

            }
        )
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이메일'
            }
        )
    )

    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': '비밀번호'

            }
        )
    )

    password2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': '비밀번호'

            }
        )
    )

    # username 필드에 대한 clean_<field_name> 메소드를 정의한다.
    def clean_username(self):
        # 바인딩된 form에서 username을 가져와 data에 할당한다.
        data = self.cleaned_data['username']
        # 데이터베이스에 해당 username이 존재하는지 검사한다. 이미 존재 할 경우 ValidationError가 발생한다.
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("중복된 사용자 이름 입니다.")
        # 존재 하지 않을 경우 data 리턴한다.
        else:
            return data

    # email 필드에 대한 clean_<field_name> 메소드를 정의한다.
    def clean_email(self):
        # 바인딩된 form에서 email을 가져와 data에 할당한다.
        data = self.cleaned_data['email']
        # 데이터베이스에 해당 email이 존재하는지 검사한다. 이미 존재 할 경우 ValidationError가 발생한다.
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError(f'다른 계정에서 {data}를 사용하고 있습니다.')
        # 존재 하지 않을 경우 data를 리턴한다.
        else:
            return data

    def __init__(self, *args, **kwargs):
        # super()로 forms의 __init__ 메소드를 호출 한다.
        super().__init__(*args, **kwargs)
        # self.user를  None으로 할당하여, user에 값이 없을 때 생기는 에러를 방지한다.
        self.user = None

    def clean(self):
        if self.is_valid():
            setattr(self, 'signup', self._signup)
        return self.cleaned_data

    def _signup(self):
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']

        new_user = User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            username=username,
                                            password=password,
                                            email=email, )
        return new_user

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise forms.ValidationError('비밀번호가 일치 하지 않습니다.')
        return password2


class LoginForm(forms.Form):
    """

    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '사용자 이름'

            }
        )
    )

    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': '비밀번호'

            }
        )
    )

    def __init__(self, *args, **kwargs):
        # super()로 forms의 __init__ 메소드를 호출 한다.
        super().__init__(*args, **kwargs)
        # self.user를  None으로 할당하여, user에 값이 없을 때 생기는 에러를 방지한다.
        self.user = None

    def clean(self):
        # cleaned_data로
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data['username']
        password = cleaned_data['password']

        # authenticate 인증에 실패 하면 ValidationError를 발생 시킨다.
        self.user = authenticate(username=username, password=password)
        if not self.user:
            raise forms.ValidationError('로그인 정보가 틀렸습니다.')
        # user가 인증에 성공 했을 떄, setattr은 login이란 이름의 _login메소드를 동적으로 추가한다.
        else:
            setattr(self, 'login', self._login)

    def _login(self, request):
        """

        :param request: django.contrib
        :return: None
        """
        django_login(request, self.user)
