from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe


class JobsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'salary')
    list_editable = ('category',)
    list_filter = ('category',)
    search_fields = ('name', 'deman', 'salary', 'category')
    list_display_links = ('name',)

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text')
    search_fields = ('author',)
    list_filter = ('author',)
    list_display_links = ('author',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'addres', 'phone', 'email', 'get_photo')
    search_fields = ('user',)
    list_display_links = ('user',)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.photo.url if obj.photo else None}" width="75">')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_photo')
    list_display_links = ('name',)


    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.photo.url if obj.photo else None}" width="75">')

class CallBackAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'text')
    list_display_links = ('author',)
    search_fields = ('author',)


admin.site.register(Jobs, JobsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(UserProfile, UserAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(CallBack, CallBackAdmin)