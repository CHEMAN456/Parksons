from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from django.contrib import messages
from django.views.generic import UpdateView,TemplateView
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, CharFilter, BooleanFilter
from django.urls import reverse_lazy
from .models import Size
from .forms import SizeForm
from .serializers import SizeSerializer

# Custom pagination
class SizePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

class SizeDetailView(RetrieveUpdateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    lookup_field = "code"
    
# FilterSet with global search and individual field filters
class SizeFilter(FilterSet):
    global_search = CharFilter(method='filter_global', label='Global Search')
    code = CharFilter(lookup_expr='icontains')
    name = CharFilter(lookup_expr='icontains')
    size_length = CharFilter(lookup_expr='exact')  # Changed to exact
    size_width = CharFilter(lookup_expr='exact')   # Changed to exact
    length_in_mm = CharFilter(lookup_expr='exact') # Changed to exact
    width_in_mm = CharFilter(lookup_expr='exact')  # Changed to exact
    unit_code = CharFilter(lookup_expr='icontains')
    active = CharFilter(method='filter_active')
    
    def filter_active(self, queryset, name, value):
        value_str = str(value).lower()
        if value_str in ['true', '1']:
            return queryset.filter(active=True)
        elif value_str in ['false', '0']:
            return queryset.filter(active=False)
        return queryset

    def filter_global(self, queryset, name, value):
        val_lower = str(value).lower()
        if val_lower in ['true', '1']:
            active_val = True
        elif val_lower in ['false', '0']:
            active_val = False
        else:
            active_val = None

        q = (
            Q(code__icontains=value) |
            Q(name__icontains=value) |
            Q(size_length__icontains=value) |
            Q(size_width__icontains=value) |
            Q(unit_code__icontains=value)
        )

        if active_val is not None:
            queryset = queryset.filter(active=active_val)

        return queryset.filter(q)

        
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
            "name": list(queryset.values_list("name", flat=True).distinct().order_by('name')),
            "size_length": [str(v) for v in queryset.values_list("size_length",flat = True).distinct().order_by('size_length') if v],
            "size_width": [str(v) for v in queryset.values_list("size_width",flat = True).distinct().order_by('size_width') if v],
            "length_in_mm": [str(v) for v in queryset.values_list("length_in_mm",flat = True).distinct().order_by('length_in_mm') if v],
            "width_in_mm": [str(v) for v in queryset.values_list("width_in_mm",flat = True).distinct().order_by('width_in_mm') if v],
            "unit_code": list(queryset.values_list("unit_code", flat=True).distinct().order_by('unit_code')),
            "active": [
                {"value": True, "label": "Active"},
                {"value": False, "label": "Inactive"}
            ]
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

class SizeDetailPageView(UpdateView):
    model = Size
    form_class = SizeForm
    template_name = "size_detail.html"
    pk_url_kwarg = "code"
    success_url = reverse_lazy("size-list-page")  
    
    def form_valid(self,form):
        messages.success(self.request,f"Code {form.instance.code} updated successfully!") 
        return super().form_valid(form)
    
    