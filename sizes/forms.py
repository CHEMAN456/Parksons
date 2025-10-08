from django import forms
from .models import Size

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = [
            'code',
            'name',
            'size_length',
            'size_width',
            'unit_code',
            'length_in_mm',
            'width_in_mm',
            'active',
        ]
        widgets = {
            'code': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'size_length': forms.NumberInput(attrs={'class': 'form-control'}),
            'size_width': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit_code': forms.TextInput(attrs={'class': 'form-control'}),
            'length_in_mm': forms.NumberInput(attrs={'class': 'form-control'}),
            'width_in_mm': forms.NumberInput(attrs={'class': 'form-control'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }