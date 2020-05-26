from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('user/reg', views.user_reg),
    path('user/reg/success', views.user_registration_success),
    path('user/login', views.user_login),
    path('user/login/success', views.user_login_success),
    path('user/logout', views.user_logout),
    path('getout', views.getout),
]
