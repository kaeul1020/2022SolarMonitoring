# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ModuleData(models.Model):
    addr = models.CharField(max_length=100)
    site_name = models.CharField(max_length=50)
    kwp = models.DecimalField(max_digits=7, decimal_places=2)
    sl_id = models.IntegerField()
    item_no = models.IntegerField()
    dt = models.CharField(max_length=10)
    dt_hour = models.IntegerField()
    dc_vol1 = models.DecimalField(max_digits=10, decimal_places=3)
    dc_cur1 = models.DecimalField(max_digits=10, decimal_places=3)
    dc_kw1 = models.DecimalField(max_digits=10, decimal_places=3)
    dc_vol2 = models.DecimalField(max_digits=10, decimal_places=3)
    dc_cur2 = models.DecimalField(max_digits=10, decimal_places=3)
    dc_kw2 = models.DecimalField(max_digits=10, decimal_places=3)
    dc_vol3 = models.DecimalField(max_digits=10, decimal_places=3)
    dc_cur3 = models.DecimalField(max_digits=10, decimal_places=3)
    dc_kw3 = models.DecimalField(max_digits=10, decimal_places=3)
    dc_vol4 = models.DecimalField(max_digits=10, decimal_places=3)
    dc_cur4 = models.DecimalField(max_digits=10, decimal_places=3)
    dc_kw4 = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        managed = False
        app_label = "test1"
        db_table = 'module_data'

class MonitoringDataset(models.Model):
    date = models.DateTimeField()
    year = models.IntegerField()
    month = models.IntegerField()
    day = models.IntegerField()
    hour = models.IntegerField()
    y = models.DecimalField(db_column='Y', max_digits=20, decimal_places=15)  # Field name made lowercase.
    pred_y = models.DecimalField(db_column='pred_Y', max_digits=20, decimal_places=15)  # Field name made lowercase.
    facility_utilization_rate = models.DecimalField(db_column='Facility_utilization_rate', max_digits=20, decimal_places=15)  # Field name made lowercase.
    error_rate = models.DecimalField(max_digits=20, decimal_places=15)

    class Meta:
        managed = False
        app_label = "test1"
        db_table = 'monitoring_dataset'