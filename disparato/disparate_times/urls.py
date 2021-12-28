from django.urls import path
from . import views

urlpatterns = [
    path('related_words/<str:word>', views.related_words, name="related_words"),
    path('', views.index, name='index')
    
]
