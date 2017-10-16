from django import forms


class PostForm(forms.Form):
    photo = forms.ImageField(required=True)
    # text = forms.CharField(max_length=100)
