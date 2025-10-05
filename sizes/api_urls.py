from django.urls import path
from .views import SizeListView,SizeDetailView


urlpatterns = [
    path("sizes/",SizeListView.as_view(),name="size-list"),    
    path("sizes/<int:code>/",SizeDetailView.as_view(),name="size-detail")
]
