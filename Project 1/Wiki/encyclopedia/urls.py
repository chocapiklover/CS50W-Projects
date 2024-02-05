from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"), # New path for the entry page using the converted html title 
    path("search/", views.search, name="search"), # New path for the search
    path("newentry/", views.newentry, name="newentry"), # New path for creating a new entry page
    path("edit/<str:title>/", views.edit, name="edit"), # New path for edit page
    path("random/", views.random_entry, name="random_entry") # New path 
]
