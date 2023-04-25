from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display=['name','description','active'] 
    
@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display=['title','storyline','active','created'] 
    
@admin.register(Streamplatform)
class StreamplatformAdmin(admin.ModelAdmin):
    list_display=['name','website','about'] 
    
# @admin.register(Review)
# class StreamplatformAdmin(admin.ModelAdmin):
#     list_display=['rating','description','watchlist'] 
admin.site.register(Review)