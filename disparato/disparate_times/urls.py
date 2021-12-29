from django.urls import path
from . import views

urlpatterns = [
    path('test_route/<str:word>', views.test_route, name='test_route'),
    path('related_words/<str:word1>/<str:word2>/data.json', views.related_words, name="related_words"),
    path('', views.index, name='index')

    
]
