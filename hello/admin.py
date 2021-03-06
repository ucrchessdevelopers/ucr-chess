from django.contrib import admin
from .models import *

admin.site.site_header = 'UCR Chess Backend'

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'rating', 'last_active']
    ordering = ['-rating']
    fields = ['lichessUser', 'firstname', 'lastname', 'rating']
    readonly_fields = ['last_active', 'rating_diff', 'wins', 'losses', 'draws']

admin.site.register(Player, PlayerAdmin)

def Increment_Order(modeladmin, request, queryset):
    for obj in queryset:
        if obj.order < 20:
            obj.order = obj.order + 1
            obj.save()
Increment_Order.short_description = "Increase order by one"

def Decrement_Order(modeladmin, request, queryset):
    for obj in queryset:
        if obj.order > 1:
            obj.order = obj.order - 1
            obj.save()
Decrement_Order.short_description = "Decrease order by one"

class CarouselAdmin(admin.ModelAdmin):
    list_display = ['order', 'picture_tag', 'description']
    ordering = ['order']
    actions = [Increment_Order, Decrement_Order]
    fields = ['order', 'description', 'picture', 'picture_edit_tag']
    readonly_fields = ['picture_edit_tag']

admin.site.register(CarouselImage, CarouselAdmin)

class OfficerAdmin(admin.ModelAdmin):
    list_display = ['name', 'picture_tag', 'position', 'email', 'order']
    ordering = ['order']
    actions = [Increment_Order, Decrement_Order]
    fields = ['order', 'picture', 'picture_edit_tag', 'name', 'position', 'email', 'about']
    readonly_fields = ['picture_edit_tag']

admin.site.register(Officer, OfficerAdmin)

# admin.site.register(VegaChessEntry)
