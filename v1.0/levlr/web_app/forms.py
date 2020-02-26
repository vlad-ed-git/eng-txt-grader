from django import forms
from .models import InputTexts
from django.contrib.auth.models import User

class InputTextsForm(forms.ModelForm):
    class Meta:
        model = InputTexts
        fields = ('input_txts', 'created_by')
        labels = {
            'input_txts': ' My Document',
            'created_by': '*My Uploder Id'
        }
        widgets = {
            'created_by': forms.TextInput(attrs={'disabled': 'disabled'}),
        }

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta():
        model = User
        fields = ('password',)