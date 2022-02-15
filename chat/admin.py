from django.contrib import admin

# Register your models here.
from chat.models import User, Message

admin.site.register(User)


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Message)


class MessageAdmin(admin.ModelAdmin):
    pass