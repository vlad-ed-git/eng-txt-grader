from django import forms
from .models import WordLists, InputTexts


class WordListsForm(forms.ModelForm):
    class Meta:
        model = WordLists
        fields = ('word_lists',)


class InputTextsForm(forms.ModelForm):
    class Meta:
        model = InputTexts
        fields = ('input_txts',)
