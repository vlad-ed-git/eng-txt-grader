from django import forms
from .models import InputTexts


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
