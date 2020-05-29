from django.shortcuts import render, redirect, HttpResponse
from shows_app.models import *
from django.utils import timezone
from django.contrib import messages
from django.db.models import Avg, Max, Min, Sum
from datetime import datetime
from .models import User


def index(request):

    return render(request, "index.html")


def show_list(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    this_list = Wlist.objects.get(user_id=request.session['user_id'])
    context = {
        'this_user': logged_in_user,
        'user_list': Show.objects.filter(watchlist=this_list),
        'shows': Show.objects.all().order_by('title'),
    }
    return render(request, 'show_list.html', context)


def show_view(request, show_num):
    stars = Review.objects.filter(show=Show.objects.get(id=show_num)).aggregate(Avg('score'))['score__avg'] if Review.objects.filter(
        show=Show.objects.get(id=show_num)).aggregate(Avg('score'))['score__avg'] else 0
    this_list = Wlist.objects.get(user_id=request.session['user_id'])
    logged_in_user = User.objects.get(id=request.session['user_id'])
    context = {
        'this_user': logged_in_user,
        'user_list': Show.objects.filter(watchlist=this_list),
        'show': Show.objects.get(id=show_num),
        'reviews': Review.objects.filter(show=Show.objects.get(id=show_num)),
        'intStars': round(stars),
        'stars': round(stars, 2),
    }
    print("*"*50)
    print(Show.objects.get(id=show_num).photo)
    print("*"*50)
    return render(request, 'show_view.html', context)


def show_add(request):
    if('logged_in' not in request.session):
        return redirect("/getout")
    context = {
        'networks': Network.objects.all().order_by('name'),
        'genres': Genre.objects.all().order_by('name'),
        'default_date': datetime.now().strftime('%Y-%m-%d'),
    }
    return render(request, 'show_add.html', context)


def show_edit(request, show_num):
    if('logged_in' not in request.session):
        return redirect("/getout")
    context = {
        'show': Show.objects.get(id=show_num),
        'genres': Genre.objects.all().order_by('name'),
        'networks': Network.objects.all().order_by('name'),
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
            'medium': request.POST['medium'],
            'genres': Genre.objects.all(),
            'seasons': request.POST['seasons'],
            'episodes': request.POST['episodes'],
            'runtime': request.POST['runtime'],
            'release_date': request.POST['release_date'],
            'description': request.POST['description'],
            'image': request.POST['image'],
            'networkSelected': int(request.POST['network']),
            'networks': Network.objects.all(),
            'default_date': datetime.now().strftime('%Y-%m-%d'),
        }
        return render(request, 'show_add.html', context)
    else:
        lastShowAdded = Show.objects.create(title=request.POST['title'],
                                            image=request.POST['image'],
                                            medium=request.POST['medium'],
                                            runtime=int(request.POST['runtime']) if request.POST['runtime'] else 0,
                                            release_date=request.POST['release_date'],
                                            description=request.POST['description'],
                                            network=Network.objects.get(id=request.POST['network']),
                                            user_id=request.session['user_id'],
                                            total_seasons=int(request.POST['seasons']) if request.POST['seasons'] else 0,
                                            total_episodes=int(request.POST['episodes']) if request.POST['episodes'] else 0)

        # print(request.POST)
        lastShowAdded.cache()
        # lastShowAdded = Show.objects.last()
        for genre in Genre.objects.all():
            if (f"genre{genre.id}" in request.POST):
                lastShowAdded.genre.add(Genre.objects.get(id=genre.id))
        return redirect(f"/shows/view/{lastShowAdded.id}")


def show_edit_db(request):
    errors = Show.objects.basicValidator(request.POST)
    if (len(errors) > 0):
        for kay, value in errors.items():
            messages.error(request, value)
        context = {
            'id': request.POST['id'],
            'title': request.POST['title'],
            'medium': request.POST['medium'],
            'genres': Genre.objects.all(),
            'seasons': request.POST['seasons'],
            'episodes': request.POST['episodes'],
            'runtime': request.POST['runtime'],
            'release_date': request.POST['release_date'],
            'description': request.POST['description'],
            'image': request.POST['image'],
            'networkSelected': int(request.POST['network']),
            'networks': Network.objects.all(),
            'default_date': datetime.now().strftime('%Y-%m-%d'),
        }
        return render(request, 'show_edit.html', context)
    else:
        aShow = Show.objects.get(id=request.POST['id'])

        aShow.title = request.POST['title']
        aShow.medium = request.POST['medium']
        aShow.total_seasons = int(request.POST['seasons']) if request.POST['seasons'] else 0
        aShow.total_episodes = int(request.POST['episodes']) if request.POST['episodes'] else 0
        aShow.runtime = int(request.POST['runtime']) if request.POST['runtime'] else 0
        aShow.release_date = request.POST['release_date']
        aShow.description = request.POST['description']
        aShow.image = request.POST['image']
        aShow.network = Network.objects.get(id=request.POST['network'])
        aShow.modified_at = datetime.now()
        aShow.save()
        aShow.cache()

        for genre in Genre.objects.all():
            if (f"genre{genre.id}" in request.POST):
                aShow.genre.add(Genre.objects.get(id=genre.id))
            else:
                aShow.genre.remove(Genre.objects.get(id=genre.id))
        return redirect(f"/shows/view/{aShow.id}")


def show_delete_db(request, show_num):
    Show.objects.get(id=show_num).delete()
    return redirect(f"/shows/list")


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
        aGenre = Genre.objects.get(id=request.POST['id'])

        aGenre.name = request.POST['name']
        aGenre.save()
        return redirect(f"/shows/genre/list")


def genre_delete_db(request, genre_num):
    Genre.objects.get(id=genre_num).delete()
    return redirect(f"/shows/genre/list")


def watchlist_view(request):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    this_list = Wlist.objects.get(user_id=request.session['user_id'])
    context = {
        'this_user': logged_in_user,
        'watchlist': Show.objects.filter(watchlist=this_list),
    }
    return render(request, 'watchlist.html', context)


def watchlist_add(request, show_num):
    logged_in_user = User.objects.get(id=request.session['user_id'])
    show_to_add = Show.objects.get(id=show_num)
    User.objects.get(id=request.session['user_id']).watchlist.show.add(show_to_add)
    this_list = Wlist.objects.get(user_id=request.session['user_id'])
    context = {
        'this_user': logged_in_user,
        'watchlist': Show.objects.filter(watchlist=this_list),
    }
    return render(request, 'watchlist.html', context)


def watchlist_remove(request, show_num):
    User.objects.get(id=request.session['user_id']).watchlist.show.remove(Show.objects.get(id=show_num))
    return redirect('/shows/watchlist/view')


def review_add_db(request):
    if('logged_in' not in request.session):
        return redirect("/getout")

    Review.objects.create(user=User.objects.get(id=request.session['user_id']), show=Show.objects.get(id=request.POST['show_id']),
                          title=request.POST['review_title'], review=request.POST['review_text'], score=request.POST['review_score'])
    return redirect(f"/shows/view/{request.POST['show_id']}")


def getout(request):
    return render(request, "getout.html")
