from django import forms
from django.contrib.auth import get_user_model

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

    # clean_<field_name> method for username field
    def clean_username(self):
        # 바인딩된 form에서 username을 가져와, 해당 username가 데이터베이스에 존재하는지 검사
        data = self.cleaned_data['username']
        # 이미 존재 할 경우 ValidationError 발생, 없을 경우 data 리턴
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("중복된 사용자 이름 입니다.")
        else:
            return data

    # clean_<field_name> method for email field
    def clean_email(self):
        # 바인딩된 form에서 email을 가져와, 해당 email가 데이터베이스에 존재하는지 검사
        data = self.cleaned_data['email']
        # 이미 존재 할 경우 ValidationError 발생, 없을 경우 data 리턴
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError(f'다른 계정에서 {data}를 사용하고 있습니다.')
        else:
            return data


class SignInForm(forms.Form):
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
