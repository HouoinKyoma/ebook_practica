from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .models import Ebook, Favorite
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUserCreationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BookSearchForm

def index(request):
    query = request.GET.get('query', '')  
    if query:
        ebooks = Ebook.objects.filter(title__icontains=query)  
    else:
        ebooks = Ebook.objects.all()  
    return render(request, 'ebook/index.html', {'ebooks': ebooks, 'query': query})

def book_detail(request, id):
    ebook = get_object_or_404(Ebook, id=id)
    return render(request, 'ebook/book_detail.html', {'ebook': ebook})

def favourites(request):
    return render(request, 'ebook/favourites.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'ebook/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
    else:
        form = AuthenticationForm()
    return render(request, 'ebook/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')   

def ebook_search(request):
    form = BookSearchForm(request.GET or None)
    ebooks = Ebook.objects.all()
    if form.is_valid():
        query = form.cleaned_data.get('query', '')
        if query:
            ebooks = ebooks.filter(title__icontains=query)  
    return render(request, 'ebook/index.html', {'form': form, 'ebooks': ebooks})

@login_required
def add_to_favorites(request, ebook_id):
    ebook = get_object_or_404(Ebook, id=ebook_id)
    if request.user.is_authenticated:
        favorite, created = Favorite.objects.get_or_create(user=request.user, ebook=ebook)
        if created:
            messages.success(request, 'Книга добавлена в избранное!')
        else:
            messages.info(request, 'Эта книга уже в вашем списке избранных!')
    else:
        messages.error(request, 'Пожалуйста, войдите в систему, чтобы добавить книгу в избранное.')
    return redirect('favorites')


@login_required
def favorite_books(request):
    favorites = Favorite.objects.filter(user=request.user)
    ebooks = [favorite.ebook for favorite in favorites]
    
    return render(request, 'ebook_app/favorite_books.html', {'ebooks': ebooks})