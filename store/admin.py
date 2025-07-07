from django.contrib import admin
from django.utils.html import format_html
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'prod_name', 'category', 'price', 'short_description', 'image_tag')
    list_filter = ('category',)
    search_fields = ('prod_name', 'category', 'description')
    readonly_fields = ('image_tag',)
    fieldsets = (
        (None, {
            'fields': ('prod_name', 'category', 'price', 'description', 'image', 'image_tag')
        }),
    )

    def short_description(self, obj):
        return (obj.description[:75] + "...") if obj.description and len(obj.description) > 75 else obj.description
    short_description.short_description = 'Description'

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; border-radius: 5px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image Preview'

admin.site.site_header = "Captain Mart Admin"
admin.site.site_title = "Captain Mart Admin Portal"
admin.site.index_title = "Welcome to Captain Mart Backend"