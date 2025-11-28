from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            widget = self.fields[field].widget
            if hasattr(widget, 'input_type') and widget.input_type == 'select':
                 widget.attrs.update({'class': 'form-select'})
            else:
                 widget.attrs.update({'class': 'form-control'})
