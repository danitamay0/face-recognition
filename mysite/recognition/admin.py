from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Face

@admin.register(Face)
class FacetAdmin(admin.ModelAdmin): 
    list_display = ( 'image_tag','name', 'created_at' ,'status' )

    def image_tag(self, obj):
# Suggested code may be subject to a license. Learn more: ~LicenseLog:3003890486.
        return format_html("""<img src="{}" style="    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 100%;"/>""".format(obj.image.url))

    image_tag.short_description = 'Image'
    pass