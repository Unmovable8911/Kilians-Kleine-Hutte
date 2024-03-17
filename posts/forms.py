from django import forms
from .models import Post, Topic

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title", "topic", "cover",
            # "body"
        ]

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["name"]