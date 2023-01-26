from django import forms
# from froala_editor.widgets import FroalaEditor
from tinymce.widgets import TinyMCE
from blogapp.models import Category, Post

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'body']


class PostForm(forms.Form):

    title = forms.CharField(max_length = 250, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    desc = forms.CharField(max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'Description'}), label='Description')
    # body = forms.CharField(widget=FroalaEditor())
    body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
