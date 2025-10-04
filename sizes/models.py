from django.db import models

# Create your models here.

class Size(models.Model):
    
    code = models.AutoField(primary_key=True, db_column='size_code')
    name = models.CharField(max_length=40, blank=True, null=True, db_column='size_desc')
    size_length = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='sizelength')
    size_width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='sizewidth')
    unit_code = models.CharField(max_length=4, blank=True, null=True)
    length_in_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='length')
    width_in_mm = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, db_column='width')
    active = models.CharField(db_column='ACT', max_length=1, blank=True, null=True)
    
    class Meta:
        db_table = 'sizes'
        ordering = ['code']
        
        
    def __str__(self):
        return f"{self.name}({self.code})"

    
