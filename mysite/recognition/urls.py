


from rest_framework import routers

from .api_views.charge_faces_test import charge_face, charge_faces_test

from .api_views.recognition import recognition
from .api_views.recognition_knn import recognition_knn
# Serializers define the API representation.
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

# Routers provide an easy way of automatically determining the URL conf.
""" router = routers.DefaultRouter()
router.register(r'face', recognition) """

urlpatterns = [
    path('recognition', recognition, name='recognition'),
    path('recognition-knn', recognition_knn, name='recognition_knn'),
    path('charge-faces', charge_faces_test, name='recognition_knn'),
    path('charge-face', charge_face, name='recognition_knn'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
