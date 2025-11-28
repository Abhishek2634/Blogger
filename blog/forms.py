from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-control-lg', 
                'placeholder': 'Enter an engaging title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 8, 
                'placeholder': 'Write your story here...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': '3'
            }),
        }
        help_texts = {
            'tags': 'Hold "Ctrl" (or "Cmd" on Mac) to select multiple tags.'
        }
