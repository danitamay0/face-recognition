


from rest_framework import routers

from .api_views.recognition_svm import recognition_svm
from .api_views.recognition import recognition
from .api_views.recognition_knn import recognition_knn
# Serializers define the API representation.
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

# Routers provide an easy way of automatically determining the URL conf.
""" router = routers.DefaultRouter()
router.register(r'face', recognition) """

urlpatterns = [
    path('recognition/', recognition, name='recognition'),
    path('recognition-svm/', recognition_svm, name='recognition_svm'),
    path('recognition-knn/', recognition_knn, name='recognition_knn'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
