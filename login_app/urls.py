from . import views
from django.urls import path

urlpatterns = [
    path('signup/', views.signup_view, name = 'signup'),
    path('', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('user/', views.user_view, name = 'user'),
    path('other/', views.other_view, name = 'other'),
    path('main/',views.main_view, name = 'main'),
    path('<int:article_id>/',views.content_view, name = 'content')
]