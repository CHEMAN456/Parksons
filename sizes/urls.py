from django.contrib import admin
from django.urls import path,include
from .views import SizeListPageView

urlpatterns = [

    path('sizes/', SizeListPageView.as_view(),name="size-list-page"),
   
]
