from .views import *
from django.urls import path
from django.views.decorators.cache import cache_page

urlpatterns = [
    path("",HomeNews.as_view(),name = "home"),
    path("contact",contact_us,name = "contact"),
    path("logout",user_logout,name = "logout"),
    path("register",user_register,name= 'register'),
    path("login",user_login,name='login'),
    path("news/add-news",AddNews.as_view(),name = "add-news"),
    path("category/<slug:slug_category>",GetCategory.as_view(),name = "category"),
    path("news/<slug:slug_news>",GetNews.as_view(),name = "news"),
]
