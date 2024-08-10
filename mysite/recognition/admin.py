from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Face, FacePredict, FaceTraining
class FaceTraningAdmin(admin.TabularInline):
    model = FaceTraining
    fields = ['image']
    readonly_fields = ['face_encoding']
    min_num = 3
    extra = 0
    
@admin.register(Face)
class FacesAdmin(admin.ModelAdmin): 
    list_display = ( 'image_tag','name', 'created_at' ,'status' )
    inlines= [FaceTraningAdmin]
    
    def image_tag(self, obj):
        face = FaceTraining.objects.filter(face_id=obj.id).first()
        if face:
            return format_html("""<img src="{}" style="    width: 100px;
                    height: 100px;
                    object-fit: cover;
                    border-radius: 100%;"/>""".format(face.image.url))

    image_tag.short_description = 'Image'


@admin.register(FacePredict)
class FacesAdmin(admin.ModelAdmin): 
    list_display = ( 'image_tag', 'created_at','found_face', 'face' ,'client' )
    def image_tag(self, obj):
       
        if obj.image:
            return format_html("""<img src="{}" style="    width: 100px;
                    height: 100px;
                    object-fit: cover;
                    border-radius: 100%;"/>""".format(obj.image.url))

    image_tag.short_description = 'Image'
    pass