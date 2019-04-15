from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .forms import LoginForm
import requests


def book_list(request):
    if request.session.get('mybook_user'):
        url = 'https://mybook.ru/api/bookuserlist/'
        session = request.session.get('mybook_user')
        books = get_books_from_url(url, session)     
        return render(request, 'book_list/index.html', {'books': books})
    else:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                r = requests.post('https://mybook.ru/api/auth/',
                                  json={"email": email,
                                        "password": password})
                if r.status_code /100 == 2:
                    session = r.cookies.get_dict()['session']
                    request.session['mybook_user'] = session
                else:
                    messages.error(request, 'Проверьте правильность введенных Вами даных: {}'.format(email))
                return redirect('book_list:book_list')
        else:
            form = LoginForm()
            return render(request, 'book_list/index.html', {'form': form})

def get_books_from_url(url, session):
    r = requests.get(url, cookies={'session':session})
    books = []
    current_page = True
    while current_page:
        for book in r.json()['objects']:
            books.append({'book_name': book['book']['name'],
                          'author': book['book']['main_author']['cover_name'],
                          'cover_img': 'https://i4.mybook.io/c/256x426/' + book['book']['default_cover'],
                          'book_url': book['book']['share_url']})
        current_page = r.json()['meta']['next']
        if current_page:
            url = 'https://mybook.ru' + current_page
            r = requests.get(url, cookies={'session':session})
    return books

def clear_session(request):
    if request.session.get('mybook_user'):
        del request.session['mybook_user']
    return redirect('book_list:book_list')

