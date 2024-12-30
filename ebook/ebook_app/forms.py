from django import forms
from .models import Favorite

class BookSearchForm(forms.Form):
    query = forms.CharField(label='Назва книги', max_length=200, required=False)

class AddToFavoritesForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = ['ebook']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        favourite = super().save(commit=False)
        favourite.user = self.user
        if commit:
            favourite.save()
        return favourite