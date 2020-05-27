from django.shortcuts import render, redirect, HttpResponse
from shows_app.models import *
from django.utils import timezone
from django.contrib import messages
from datetime import datetime


def index(request):

    return render(request, "index.html")


def show_list(request):
    context = {
        'shows': Show.objects.all().order_by('title')
    }
    return render(request, 'show_list.html', context)


def show_view(request, show_num):
    context = {
        'show': Show.objects.get(id=show_num),
    }
    return render(request, 'show_view.html', context)


def show_add(request):
    if('logged_in' not in request.session):
        return redirect("/getout")
    context = {
        'networks': Network.objects.all(),
        'default_date': datetime.now().strftime('%Y-%m-%d'),
    }
    return render(request, 'show_add.html', context)


def show_edit(request, show_num):
    if('logged_in' not in request.session):
        return redirect("/getout")
    context = {
        'show': Show.objects.get(id=show_num),
        'networks': Network.objects.all(),
        'date': Show.objects.get(id=show_num).release_date.strftime('%Y-%m-%d')
    }
    return render(request, 'show_edit.html', context)


def show_add_db(request):
    errors = Show.objects.basicValidator(request.POST)
    if(len(errors) > 0):
        for key, value in errors.items():
            messages.error(request, value)
        context = {
            'title': request.POST['title'],
            'image': request.POST['image'],
            'runtime': request.POST['runtime'],
            'seasons': request.POST['seasons'],
            'episodes': request.POST['episodes'],
            'release_date': request.POST['release_date'],
            'default_date': datetime.now().strftime('%Y-%m-%d'),
            'description': request.POST['description'],
            'networkSelected': int(request.POST['network']),
            'networks': Network.objects.all(),
        }
        print("*"*35)
        print(datetime.now().strftime('%Y-%m-%d'))
        print("*"*35)
        return render(request, 'show_add.html', context)
    else:
        Show.objects.create(title=request.POST['title'], image=request.POST['image'], runtime=request.POST['runtime'], seasons=request.POST['seasons'], episodes=request.POST['episodes'],
                            release_date=request.POST['release_date'], description=request.POST['description'], network=Network.objects.get(id=request.POST['network']), user_id=request.session['id'])
        return redirect(f"/shows/view/{Show.objects.last().id}")


def show_edit_db(request):
    errors = Show.objects.basicValidator(request.POST)
    if (len(errors) > 0):
        for kay, value in errors.items():
            messages.error(request, value)
        context = {
            'id': request.POST['id'],
            'title': request.POST['title'],
            'image': request.POST['image'],
            'runtime': request.POST['runtime'],
            'seasons': request.POST['seasons'],
            'episodes': request.POST['episodes'],
            'release_date': request.POST['release_date'],
            'default_date': datetime.now().strftime('%Y-%m-%d'),
            'description': request.POST['description'],
            'networkSelected': int(request.POST['network']),
            'networks': Network.objects.all(),
        }
        return render(request, 'show_edit.html', context)
    else:
        print("*"*35)
        print(request.POST['id'])
        print("*"*35)
        aShow = Show.objects.get(id=request.POST['id'])

        aShow.title = request.POST['title']
        aShow.runtime = request.POST['runtime']
        aShow.seasons = request.POST['seasons']
        aShow.episodes = request.POST['episodes']
        aShow.description = request.POST['description']
        aShow.network = Network.objects.get(id=request.POST['network'])
        aShow.release_date = request.POST['release_date']
        aShow.image = request.POST['image']
        aShow.modified_at = datetime.now()
        aShow.save()
        return redirect(f"/shows/view/{aShow.id}")


def show_delete_db(request, show_num):
    Show.objects.get(id=show_num).delete()
    return redirect(f"/show/list")


def network_list(request):
    context = {
        'networks': Network.objects.all().order_by('name')
    }
    return render(request, 'network_list.html', context)


def network_add(request):
    if('logged_in' not in request.session):
        return redirect("/getout")

    return render(request, 'network_add.html')


def network_add_db(request):
    errors = Show.objects.basicValidator(request.POST)
    if(len(errors) > 0):
        for key, value in errors.items():
            messages.error(request, value)
        context = {
            'name': request.POST['name'],
            'image': request.POST['image'],
        }
        return render(request, 'network_add.html', context)
    else:
        Network.objects.create(name=request.POST['title'], image=request.POST['image'], user_id=request.session['user_id'])
        return redirect(f"/shows/network/list")


def network_edit(request, network_num):
    if('logged_in' not in request.session):
        return redirect("/getout")
    context = {
        'network': Network.objects.get(id=network_num),
    }
    return render(request, 'network_edit.html', context)


def network_edit_db(request):
    errors = Network.objects.basicValidator(request.POST)
    if (len(errors) > 0):
        for kay, value in errors.items():
            messages.error(request, value)
        context = {
            'id': request.POST['id'],
            'name': request.POST['title'],
            'image': request.POST['image'],
        }
        return render(request, 'network_edit.html', context)
    else:
        print("*"*35)
        print(request.POST['id'])
        print("*"*35)
        aNetwork = Network.objects.get(id=request.POST['id'])

        aNetwork.name = request.POST['name']
        aNetwork.image = request.POST['image']
        aNetwork.save()
        return redirect(f"/shows/network/list")


def network_delete_db(request, network_num):
    Network.objects.get(id=network_num).delete()
    return redirect(f"/shows/network/list")


def genre_list(request):
    context = {
        'genres': Genre.objects.all().order_by('name')
    }
    return render(request, 'genre_list.html', context)


def genre_add(request):
    if('logged_in' not in request.session):
        return redirect("/getout")

    return render(request, 'genre_add.html')


def genre_add_db(request):
    errors = Genre.objects.basicValidator(request.POST)
    if(len(errors) > 0):
        for key, value in errors.items():
            messages.error(request, value)
        context = {
            'genre': request.POST['genre'],
        }
        return render(request, 'genre_add.html', context)
    else:
        Genre.objects.create(name=request.POST['genre'], user_id=request.session['user_id'])
        return redirect(f"/shows/genre/list")


def genre_edit(request, genre_num):
    if('logged_in' not in request.session):
        return redirect("/getout")
    context = {
        'genre': Genre.objects.get(id=genre_num),
    }
    return render(request, 'genre_edit.html', context)


def genre_edit_db(request):
    errors = Genre.objects.basicValidator(request.POST)
    if (len(errors) > 0):
        for kay, value in errors.items():
            messages.error(request, value)
        context = {
            'id': request.POST['id'],
            'name': request.POST['title'],
        }
        return render(request, 'genre_edit.html', context)
    else:
        print("*"*35)
        print(request.POST['id'])
        print("*"*35)
        aGenre = Genre.objects.get(id=request.POST['id'])

        aGenre.name = request.POST['name']
        aGenre.save()
        return redirect(f"/shows/genre/list")


def genre_delete_db(request, genre_num):
    Genre.objects.get(id=genre_num).delete()
    return redirect(f"/shows/genre/list")


def review_add(request):
    if('logged_in' not in request.session):
        return redirect("/getout")

    return render(request, 'genre_add.html')


def getout(request):
    return render(request, "getout.html")
