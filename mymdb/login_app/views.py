from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from datetime import datetime, date
from login_app.models import User
from shows_app.models import Wlist
import bcrypt


def index(request):
    context = {
        'default_date': datetime.now().strftime("%Y-%m-%d")
    }
    return render(request, "index.html", context)


def user_reg(request):
    if 'email' not in request.POST:
        return render(request, "getout.html")

    emailExists = User.objects.filter(email=request.POST['email'])
    postData = {}

    for key, value in request.POST.items():
        postData[key] = value

    postData['email_exists'] = True if emailExists else False
    print("*"*50)
    print(postData['email_exists'])
    print("*"*50)
    errors = User.objects.basic_validator(postData)

    if(len(errors) > 0):
        for key, value in errors.items():
            messages.error(request, value)
        context = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'birthday': request.POST['birthday']
        }
        return render(request, "index.html", context)
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], birthday=request.POST['birthday'], email=request.POST['email'], password=pw_hash)
        aUser = User.objects.filter(email=request.POST['email'])

        request.session['id'] = aUser[0].id
        request.session['user'] = aUser[0].email
        request.session['success'] = True

        Wlist.objects.create(list_name=f"{new_user.first_name}'s Watch List", user=new_user)
        return redirect('/user/reg/success')


def user_registration_success(request):
    if('success' not in request.session):
        return redirect("/getout")
    user = User.objects.get(id=request.session['id'])

    context = {
        'uid': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, "user_registration_success.html", context)


def user_login(request):
    if request.POST['email'] == "" or request.POST['password'] == "":
        return redirect("/getout")
    user = User.objects.get(email=request.POST['email'])

    if(bcrypt.checkpw(request.POST['password'].encode(), user.password.encode())):
        request.session['user_id'] = user.id
        request.session['user'] = user.email
        request.session['logged_in'] = True
        return redirect("/user/login/success")
    else:
        return redirect("/getout")


def user_login_success(request):
    if('logged_in' not in request.session):
        return redirect("/getout")

    user = User.objects.get(id=request.session['user_id'])

    context = {
        'uid': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }
    return render(request, "user_login_success.html", context)


def user_logout(request):
    request.session['logged_in'] = False
    request.session.clear()
    return redirect("/")


def getout(request):
    return render(request, "getout.html")
