# coding: utf-8
from django.contrib import admin
from models import Navigation, NavigationItem


class NavigationItemInline(admin.StackedInline):
    
    model = NavigationItem
    extra = 1
    classes = ('collapse-open',)
    fieldsets = (
        ('', {
            'fields': ('title', 'link', 'category',)
        }),
        ('', {
            'fields': ('groups', 'users',),
        }),
        ('', {
            'fields': ('order',),
        }),
    )
    filter_horizontal = ('users',)
    
    # Grappelli Options
    allow_add = True


class NavigationOptions(admin.ModelAdmin):
    
    # List Options
    list_display = ('order', 'title',)
    list_display_links = ('title',)
    # Fieldsets
    fieldsets = (
        ('', {
            'fields': ('title', 'order',)
        }),
    )
    # Misc
    save_as = True
    # Inlines
    inlines = [NavigationItemInline]
    # Grappelli Options
    order = 0


admin.site.register(Navigation, NavigationOptions)

