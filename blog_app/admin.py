from django.contrib import admin

from .models import Post, Subscribe


class PostAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'text',
                    'user',
                    'created_at'
                    )


class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post')


admin.site.register(Post, PostAdmin)
admin.site.register(Subscribe, SubscribeAdmin)
