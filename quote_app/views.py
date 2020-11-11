from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from .models import *

# Create your views here.
def index(request):
    if 'user_id' in request.session:
        return redirect('/quotes')
    else:
        return render(request, 'home.html')

def logout(request):
    list(messages.get_messages(request))
    request.session.flush()
    request.session.clear()
    return redirect ('/')

def create_user(request):
    if request.method == 'POST':
        errors = User.objects.user_validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect('/')
        else:
            unsecure_password = request.POST['password']
            secure_password = bcrypt.hashpw(unsecure_password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(first_name = request.POST['first_name'], last_name= request.POST['last_name'], email = request.POST['email'], password = secure_password)
            request.session['user_id'] = new_user.id
            request.session['user_first_name'] = new_user.first_name
            request.session['user_last_name'] = new_user.last_name
            return redirect('/quotes')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        logged_user = User.objects.filter(email=request.POST['login_email'])
        if logged_user:
            logged_user = logged_user[0]
            if bcrypt.checkpw(request.POST['login_password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                request.session['user_first_name'] = logged_user.first_name
                request.session['user_last_name'] = logged_user.last_name
                return redirect ('/quotes')
            else:
                request.session['fail'] = "You either did not type in anything or your credentials don't match!"
                return redirect('/')
        else:
            request.session['fail'] = "You either did not type in anything or your credentials don't match!"
            return redirect('/')
    else:
        request.session['fail'] = "You either did not type in anything or your credentials don't match!"
        return redirect('/')

def quotes(request):
    if 'thank_you' in request.session:
        request.session['thank_you'] = ""
    context = {
        'all_quotes' : Quote.objects.all()
    }
    return render(request, 'quotes.html', context)

def create_quote(request):
    if request.method == 'POST':
        errors_1 = Quote.objects.quote_validator(request.POST)
        if errors_1:
            for a_error in errors_1:
                print(errors_1[a_error])
                messages.error(request, errors_1[a_error])
            return redirect('/quotes')
        else:
            new_quote = Quote.objects.create(author = request.POST['author'], quote = request.POST['quote'], user = User.objects.get(id=request.POST['user_posting']))
            return redirect ('/quotes')
    else:
        return redirect('/quotes')

def profile(request, user_id):
    if 'thank_you' in request.session:
        request.session['thank_you'] = ""
    context = {
        'this_user' : User.objects.get(id=user_id)
    }
    return render(request, 'profile.html', context)

def my_account(request, user_id):
    context = {
        'my_account' : User.objects.get(id=user_id),
    }
    return render(request, 'my_account.html', context)

def update(request):
    user_id_up = request.POST['user_id_updating']
    if request.method == 'POST':
        errors_2 = User.objects.edit_validator(request.POST)
        if errors_2:
            for one_error in errors_2:
                messages.error(request, errors_2[one_error])
            return redirect(f'/my_account/{user_id_up}')
        else:
            update_user = User.objects.get(id=request.POST['user_id_updating'])
            update_user.first_name = request.POST['updated_first_name']
            update_user.last_name = request.POST['updated_last_name']
            update_user.email = request.POST['updated_email']
            update_user.save()
            request.session['thank_you'] = "Thank you for updating your account. All is saved!"
            return redirect(f'/my_account/{user_id_up}')
    else:
        return redirect(f'/my_account/{user_id_up}')

def delete(request, comm_id):
    Quote.objects.get(id=comm_id).delete()
    return redirect ('/quotes')

def delete_quote (request, comm_id):
    Quote.objects.get(id=comm_id).delete()
    profile_id = request.session['user_id']
    return redirect (f'/profile/{profile_id}')

def like(request):
    filtered_user = User.objects.get(id=request.POST['user_liking_id'])
    quote_liked = Quote.objects.get(id=request.POST['quote_id'])
    liked_quote = Like_quote.objects.filter(user=filtered_user, quote=quote_liked)
    if liked_quote:
        return redirect('/quotes')
    else:
        a_like = Like_quote.objects.create(like=request.POST['like'], quote=Quote.objects.get(id=request.POST['quote_id']), user= User.objects.get(id=request.POST['user_liking_id']))
        return redirect ('/quotes')