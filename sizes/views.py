from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, BooleanFilter
from .models import Size
from .serializers import SizeSerializer

# Custom pagination
class SizePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

# FilterSet with global search and individual field filters
class SizeFilter(FilterSet):
    global_search = CharFilter(method='filter_global', label='Global Search')
    code = CharFilter(lookup_expr='icontains')
    name = CharFilter(lookup_expr='icontains')
    size_length = CharFilter(lookup_expr='icontains')
    size_width = CharFilter(lookup_expr='icontains')
    length_in_mm = CharFilter(lookup_expr='icontains')
    width_in_mm = CharFilter(lookup_expr='icontains')
    unit_code = CharFilter(lookup_expr='icontains')
    active = BooleanFilter(method='filter_active')

    def filter_global(self, queryset, name, value):
        return queryset.filter(
            Q(code__icontains=value) |
            Q(name__icontains=value) |
            Q(size_length__icontains=value) |
            Q(size_width__icontains=value) |
            Q(unit_code__icontains=value)
        )
    def filter_active(self, queryset, name, value):
        """Convert boolean true/false to Y/N for filtering"""
        if value is True:
            return queryset.filter(active="Y")
        elif value is False:
            return queryset.filter(active="N")
        # If value is None (tristate empty), return all records
        return queryset    

    class Meta:
        model = Size
        fields = ['code', 'name', 'size_length', 'size_width', 'length_in_mm', 'width_in_mm', 'unit_code', 'active', 'global_search']
   
    
class SizeListView(ListAPIView):
    serializer_class = SizeSerializer
    pagination_class = SizePagination
    filterset_class = SizeFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = "__all__"

    def get_queryset(self):
        return Size.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        # Pagination
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page or queryset, many=True)

        # Prepare distinct filter values from the filtered queryset
        distinct_filters = {
            "code": list(queryset.values_list("code", flat=True).distinct().order_by('code')),
            "unit_code": list(queryset.values_list("unit_code", flat=True).distinct().order_by('unit_code')),
            "active": list(queryset.values_list("active", flat=True).distinct().order_by('active')),
        }

        # Return paginated response if page exists
        if page is not None:
            response = self.get_paginated_response(serializer.data)
            response.data["filters"] = distinct_filters
            return response

        # Non-paginated response fallback
        return Response({
            "results": serializer.data,
            "filters": distinct_filters
        })
                
        
class SizeListPageView(TemplateView):
    template_name = "size_list.html"