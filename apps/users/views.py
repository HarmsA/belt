from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def login(request):
    return render(request, 'users/loginbase_login.html')

def register(request):
    return render(request, 'users/loginbase_register.html')

def logged_in(request):
    print(request.POST)
    print('in logged_in')
    if 'user_id' not in request.session:
        return redirect('/login')
    name = User.objects.get(id=request.session['user_id'])
    context = {
        'name':name.f_name
    }
    return render(request, 'users/logged_in.html', context)

def process_login(request):
    print(request.POST)
    if User.objects.validate(request.POST):
        user = User.objects.get(email=request.POST['email'])
        print(user.f_name)
        print('8'*80)
        request.session['user_id'] = user.id
    else:
        error = 'Email or password is incorrect, please verify or register.'
        messages.error(request, error)
        return redirect('/login')
    return redirect('/users/logged_in')

def process_register(request):
    errors = User.objects.register_validate(request.POST)

    if errors:
        for error in errors:
            messages.error(request, error)
    else:
        user =User.objects.create_user(request.POST)
        print(user.f_name)
        print('8'*80)
        request.session['user_id'] = user.id
        return redirect('/users/logged_in')

    return redirect('/register')


def logout(request):
    pass