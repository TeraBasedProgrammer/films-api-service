from django.contrib import admin

from .models import Film, Screenshot


class ScreenshotInline(admin.StackedInline):
    model = Screenshot
    extra = 1


class FilmAdmin(admin.ModelAdmin):
    inlines = [ScreenshotInline]


admin.site.register(Film, FilmAdmin)
   
