from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from datetime import datetime, date
from login_app.models import User
from shows_app.models import Wlist, Show, Network, Genre, Review
from django.db.models import Avg, Max, Min, Sum, Count
import bcrypt
import random
from random import sample


def index(request):
    if('logged_in' not in request.session):
        context = {
            'default_date': datetime.now().strftime("%Y-%m-%d")
        }
        return render(request, "index.html", context)
    else:
        return redirect("/user/login/success")


def user_reg(request):
    if 'email' not in request.POST:
        return render(request, "getout.html")

    emailExists = User.objects.filter(email=request.POST['email'])
    postData = {}

    for key, value in request.POST.items():
        postData[key] = value

    postData['email_exists'] = True if emailExists else False
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
    user = User.objects.filter(email=request.POST['email'])
    if request.POST['email'] == "" or request.POST['password'] == "" or len(user) == 0:
        return redirect("/getout")
    if(bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode())):
        request.session['user_id'] = user[0].id
        request.session['user'] = user[0].email
        request.session['logged_in'] = True
        return redirect("/user/login/success")
    else:
        return redirect("/getout")


def user_login_success(request):
    if('logged_in' not in request.session):
        return redirect("/getout")

    user = User.objects.get(id=request.session['user_id'])
    this_list = Wlist.objects.get(user=user)


# Sets the amount of movies/shows to be displayed in the watchlist
    if(user.photo):
        request.session['avatar'] = user.photo.name
    else:
        request.session['avatar'] = "avatars/00_avatar.png"
    countShow = 12
    countAllMYShows = this_list.show.all().count()
    countMaxShows = countAllMYShows if countAllMYShows < countShow else countShow

# Gets a list of 'random' shows in the user's watchlist
    aList = []
    for i in this_list.show.all():
        aList.append(i.id)
    random.shuffle(aList)
    random_shows = Show.objects.filter(id__in=aList[:countMaxShows])

# Gets the movies/shows with the most starts
    reviews = Review.objects.all().values('show_id').annotate(total=Sum('score')).order_by('-total')[0:10]
    popularList = []
    for review in reviews.all():
        popularList.append(review['show_id'])
    context = {
        'user': user,
        'watchlist': random_shows,
        'user_reviews': Review.objects.filter(user=user).all().order_by('-created_at')[0:3],
        'popular_shows': Show.objects.filter(id__in=popularList).annotate(avg=Avg('reviews__score')).annotate(total=Sum('reviews__score')).annotate(count=Count('reviews__score')).order_by('-reviews__show_id').order_by('-total'),
    }
    print(context['popular_shows'])
    return render(request, "user_login_success.html", context)


def user_logout(request):
    request.session['logged_in'] = False
    request.session.clear()
    return redirect("/")


def avatar_add_db(request):
    user = User.objects.get(id=request.session['user_id'])
    user.image = request.POST['image']
    user.save()
    user.cache()
    return redirect("/user/login/success")


def getout(request):
    return render(request, "getout.html")
