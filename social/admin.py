from django.contrib import admin
from .models import Post, Comment, Like

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('trunc_title', 'user','thumbnail', 'like_count', 'created')
    search_fields = ('title', 'body')
    readonly_fields = ('like_count', )
    sortable_by = ('like_count', 'created', 'user',)
    prepopulated_fields = {'slug': ('title', )}
    raw_id_fields = ('user', )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post','is_reply', 'created')
    sortable_by = ('user', 'post', 'is_reply', 'created', )
    raw_id_fields = ('user', 'post')

admin.site.register(Like)