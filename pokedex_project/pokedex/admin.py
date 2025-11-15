from django.contrib import admin
from .models import Favorite, Tag

class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pokemon_id', 'notes', 'tag')
    list_filter = ('tag',)
    search_fields = ('pokemon_id', 'notes')

admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Tag)