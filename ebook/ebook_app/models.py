from django.db import models
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class Ebook(models.Model):
    title = models.CharField('Назва', max_length=100)
    description = models.TextField()
    genres = models.TextField('Жанр')
    author = models.TextField('Автор')
    preview = models.ImageField(
        upload_to='previews',
    )
    book_file = models.FileField(
        upload_to='pdfs'
    )

    def __str__(self):
        return self.title
    
    @property
    def favorites_countr(self):
        return self.favorited_by.count()
    
class CustomUserCreationForm(UserCreationForm):
     class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
     class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.ebook.title}'