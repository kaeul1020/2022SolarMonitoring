# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ThModuleMinute(models.Model):
    sl_id = models.SmallIntegerField()
    item_no = models.SmallIntegerField()
    create_date = models.DateTimeField(primary_key=True)
    dc_vol1 = models.FloatField(blank=True, null=True)
    dc_cur1 = models.FloatField(blank=True, null=True)
    dc_kw1 = models.FloatField(blank=True, null=True)
    dc_vol2 = models.FloatField(blank=True, null=True)
    dc_cur2 = models.FloatField(blank=True, null=True)
    dc_kw2 = models.FloatField(blank=True, null=True)
    dc_vol3 = models.FloatField(blank=True, null=True)
    dc_cur3 = models.FloatField(blank=True, null=True)
    dc_kw3 = models.FloatField(blank=True, null=True)
    dc_vol4 = models.FloatField(blank=True, null=True)
    dc_cur4 = models.FloatField(blank=True, null=True)
    dc_kw4 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        app_label = 'powgen'
        db_table = 'th_module_minute'
