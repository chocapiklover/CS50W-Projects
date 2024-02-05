from django.contrib import admin
from .models import User, Post, Follow, Like

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('creator', 'content', 'time')
    search_fields = ('creator__username', 'content')
    list_filter = ('time',)

class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'timestamp')  # Customize the displayed fields in the admin list view
    search_fields = ('user__username', 'post__content')  # Add search functionality for specific fields

admin.site.register(User)
admin.site.register(Like,)
admin.site.register(Post, PostAdmin,)
admin.site.register(Follow, FollowAdmin)
