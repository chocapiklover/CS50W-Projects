
from django.urls import path
from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.your_view, name="index"),# was previously index
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post , name="newpost"),
    path('profile/<int:user_id>', views.profile_view, name="profile"),
    path('unfollow/<int:user_id>', views.unfollow, name="unfollow"),
    path('follow/<int:user_id>', views.follow, name="follow"),
    path('following', views.following_page, name="following_page"),

    #apis 
    path('api/post/<int:post_id>/', views.get_post, name='get_post'),
    path('api/post/<int:post_id>/update/', views.update_post, name='update_post'),
    path('api/like/<int:post_id>', views.like_post, name='like_post'), 
    path('api/unlike/<int:post_id>', views.unlike_post, name='unlike_post'),

]  