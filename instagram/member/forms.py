from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'username'

            }
        )
    )

    email = forms.EmailField(
        widget = forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'email'
            }
        )
    )

    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type':'password',
                'placeholder':'password'

            }
        )
    )

class SignInForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'username'

            }
        )
    )

    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'type':'password',
                'placeholder':'password'

            }
        )
    )

