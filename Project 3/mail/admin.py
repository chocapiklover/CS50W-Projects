from django.contrib import admin
from .models import User, Email
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(User, UserAdmin)

class EmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'timestamp', 'read', 'archived')
    list_filter = ('read', 'archived')
    search_fields = ('subject', 'sender__username', 'recipient__username')

admin.site.register(Email, EmailAdmin)
