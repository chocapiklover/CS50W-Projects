from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.creatlisting, name="createnewlisting"),
    path("category", views.categoryview, name="category"),
    path("listings/<int:listing_id>", views.listingview, name="listingview"),
    path("add_to_watchlist/<int:listing_id>", views.addtowatchlist, name="add_to_watchlist"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("bid/<int:listing_id>/", views.bid, name='bid'),
    path('add_comment/<int:listing_id>/', views.add_comment, name='add_comment'),

]
