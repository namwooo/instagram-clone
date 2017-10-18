from django import forms
from django.contrib.auth import get_user_model, authenticate, login as django_login

User = get_user_model()


class SignUpForm(forms.Form):
    """
    회원가입에 필요한 사용자 정보를 SignUpForm클래스 안에 필드로 정의한다.
    정보의 종류에 따라 필드 타입, 위젯, 태그 속성을 입력한다.
    """
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
                'placeholder': '사용자 아이디'

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

    def clean(self):
        """
        form subclass 메소드이다. 유효성 검사를 통과 한 경우,
        setattr로 SignUpForm 인스턴스에 signup 메소드를 추가한다.
        :return: self.cleaned_data
        """
        if self.is_valid():
            setattr(self, 'signup', self._signup)
        return self.cleaned_data

    def _signup(self):
        """
        바인딩 된 form에서 cleaned_data로 회원가입에 필요한 정보를 가져와 새로운 사용자를 생성한다.
        :return: new_user
        """
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']

        new_user = User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            username=username,
                                            password=password,
                                            email=email)
        return new_user

    def clean_username(self):
        """
        바인딩된 form의 username과 데이터베이스의 username이 중복되는지 검사한다.
        :return: data
        """
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("사용할 수 없는 사용자 이름입니다. 다른 이름을 사용하세요.")
        else:
            return data

    def clean_email(self):
        """
        바인딩된 form의 email과 데이터베이스의 email이 중복되는지 검사한다.
        :return: data
        """
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exits():
            raise forms.ValidationError(f'다른 계정에서 {data}를 사용하고 있습니다.')
        else:
            return data

    def clean_password2(self):
        """
        회원가입시 비밀번호 재확인을 하기위해 password와 password2가 일치하는지 검사한다.
        :return: password2
        """
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise forms.ValidationError('비밀번호가 일치 하지 않습니다.')
        else:
            return password2


class LoginForm(forms.Form):
    """
    LoginForm 클래스에 로그인에 필요한 유저 이름과 비밀번호를 입력받는 필드를 정의한다.
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
        """
        cleaned_data로 가저온 사용자 이름과 비밀번호를 authenticate로 인증한다.
        인증에 실패하면 ValidationError 발생, 성공하면 해당 LoginForm 인스턴스에 login 함수를 추가한다.
        :return: None
        """
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        self.user = authenticate(username=username, password=password)
        if not self.user:
            raise forms.ValidationError('로그인 정보가 틀렸습니다.')
        else:
            setattr(self, 'login', self._login)  # setattr로 _login 메소드를 login이란 이름으로 동적으로 추가한다.

    def _login(self, request):
        """
        django.contrib.auth에 정의 되어 있는 built-in login 메소드를 사용한다.
        form login 메소드와 auth login 메소드를 구별하기 위해 auth login을 django_login으로 명명했다.
        :param request: login request from user
        :return: None
        """
        django_login(self.user, request)