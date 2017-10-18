from django import forms


class PostForm(forms.Form):
    """
    이미지 파일을 업로드 받는다.
    """
    photo = forms.ImageField(
        required=True,  # 파일 없음이 허용 되지 않는다.
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class CommentForm(forms.Form):
    """
    사용자로부터 댓글을 입력 받는다.
    """
    comment = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
