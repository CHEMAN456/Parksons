from django.contrib import admin
from django.urls import path,include
from .views import SizeListPageView,SizeDetailPageView

urlpatterns = [

    path('sizes/', SizeListPageView.as_view(),name="size-list-page"),
    path('sizes/detail/<int:code>/',SizeDetailPageView.as_view(),name="size-detail-page"),
   
]
