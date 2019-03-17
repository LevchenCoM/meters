from django.db import models
from datetime import date
import pandas as pd

class ResourceType(models.Model):
    name = models.CharField(max_length=32, blank=False, null=False)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = "Resource type"
        verbose_name_plural = "Resource types"


class Meters(models.Model):
    name = models.CharField(max_length=64, unique=True, blank=False, null=False)
    resource_type = models.ForeignKey(ResourceType, null=True, on_delete=models.SET_NULL)
    unit = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return "{}".format(self.name)

    def get_absolute_url(self):
        return "/meters/{}".format(self.id)

    def get_last_reading(self):
        """ Return list of last reading data - record, date, consumption"""
        return Records.objects.filter(meter__id=self.id).last()

    def consumptions_recalculation(self, start_date=date(1970,1,1)):
        """ Function which perform recalculation of consuptions
            for records where date >= instance.date """

        records_list = Records.objects.filter(meter__id=self.id,
                                              date__gte=start_date).order_by('date')
        try:
            last_record = Records.objects.filter(date__lt=start_date).order_by('date').last().record
        except:
            last_record = 0

        obj_list = []
        for record in records_list:
            if last_record == 0:
                last_record = record.record
            record.consumption = record.record - last_record
            last_record = record.record
            obj_list.append(record)

        Records.objects.filter(date__in=records_list.values_list('date', flat=True)).delete()  # delete previous records
        Records.objects.bulk_create(obj_list)  # create multiple object in one call to DB

    def import_readings(self, readings_table):  #records_table - pandas DataFrame
        readings_table = readings_table.fillna(0)   # replace NaN with 0
        obj_list = []

        for index, row in readings_table.iterrows():
            obj_list.append(Records(meter=self,
                                    date=row.DATE,
                                    record=row.VALUE,
                                    consumption=0))

        Records.objects.filter(date__in=readings_table.DATE.tolist()).delete() # delete previous records
        Records.objects.bulk_create(obj_list)                                  # create multiple object in one call to DB
        self.consumptions_recalculation(readings_table.DATE.min())


        # readings_table = readings_table.sort_values(by=['DATE'], ascending=True) # Sorting values by date (ascending)
        # readings_table['CONSUMPTION'] = readings_table['VALUE'].diff()           # Performing of calculation consumptions

    class Meta:
        verbose_name = "Meter"
        verbose_name_plural = "Meters"


class Records(models.Model):
    meter = models.ForeignKey(Meters, null=True, on_delete=models.SET_NULL)
    date = models.DateField(blank=False, null=False)
    record = models.FloatField(default=0)
    consumption = models.FloatField(default=0)


    class Meta:
        ordering = ['date']
        get_latest_by = 'date'






