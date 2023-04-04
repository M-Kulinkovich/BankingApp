from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('account/', AccountPage.as_view(), name='account'),
]