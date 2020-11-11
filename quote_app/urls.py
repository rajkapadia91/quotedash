from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create_user', views.create_user),
    path('login', views.login),
    path('logout', views.logout),
    path('quotes', views.quotes),
    path('create_quote', views.create_quote),
    path('profile/<int:user_id>', views.profile),
    path('my_account/<int:user_id>', views.my_account),
    path('update', views.update),
    path('delete/<int:comm_id>', views.delete),
    path('delete_quote/<int:comm_id>', views.delete_quote),
    path('like', views.like),
]
