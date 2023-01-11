from django.contrib import admin
from .models import User, FollowRelation
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    DefaultUserAdmin.list_display += ('img_tag', )
    DefaultUserAdmin.fieldsets[1][1]['fields'] += ('img', 'bio')


@admin.register(FollowRelation)
class FollowRelationAdmin(admin.ModelAdmin):
    pass