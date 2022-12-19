from django.forms import ModelForm, Textarea , TextInput
from .models import *





class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['user']



class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields=["body"]
        labels = {"body":""}
        widgets = {
            'body': Textarea(attrs={'class':'add_comment'}),
        }
        