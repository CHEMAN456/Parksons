from django.urls import path
from .views import SizeListView


urlpatterns = [
    path("sizes/",SizeListView.as_view(),name="size-list"),    
    
]
