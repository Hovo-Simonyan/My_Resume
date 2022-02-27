from django.contrib import admin
from django.forms import Textarea, TextInput
from django.utils.safestring import mark_safe

from .models import *


# Register your models here.

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'position', 'email', 'phone_number', 'get_photo',
                    'is_published')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_update')
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" widht="75" height="75"')
        else:
            return 'No photo'


class LanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'get_photo')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

    def get_photo(self, obj):
        if obj.photo_language:
            return mark_safe(f'<img src="{obj.photo_language.url}" widht="75" height="75"')
        else:
            return 'No photo'


admin.site.register(Resume, ResumeAdmin)
admin.site.register(Language, LanguageAdmin)
