from django.contrib import admin

# Register your models here.
from .models import BotUser, Genre, Film, Ad

class FilmAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating')
    fields = ['name', 'description', 'genre', 'year_published', 'rating', 'likes', 'dislikes', 'image', 'trailler_link', 'link_to_film']

class BotAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'date_started', 'last_day_active')
    list_filter = ('nickname', 'date_started', 'last_day_active')

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')

class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'link')

admin.site.register(BotUser, BotAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Film, FilmAdmin)
admin.site.register(Ad, AdAdmin)
admin.site.site_header = "Films Bot Admin"
admin.site.site_title = "Films Bot Admin"
admin.site.index_title = "Films Bot Control Panel"