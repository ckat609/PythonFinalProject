from django.urls import path
from . import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('list', views.show_list),
    path('add', views.show_add),
    path('add/create', views.show_add_db),
    path('edit/<int:show_num>', views.show_edit),
    path('edit/update', views.show_edit_db),
    path('view/<int:show_num>', views.show_view),
    path('delete/<int:show_num>', views.show_delete_db),
    path('network/add', views.network_add),
    path('network/list', views.network_list),
    path('network/add/create', views.network_add_db),
    path('network/edit/<int:network_num>', views.network_edit),
    path('network/edit/update', views.network_edit_db),
    path('network/delete/<int:network_num>', views.network_delete_db),
    path('genre/add', views.genre_add),
    path('genre/list', views.genre_list),
    path('genre/add/create', views.genre_add_db),
    path('genre/edit/<int:genre_num>', views.genre_edit),
    path('genre/edit/update', views.genre_edit_db),
    path('genre/delete/<int:genre_num>', views.genre_delete_db),
    path('review/add/<int:show_num', views.review_add),
]
