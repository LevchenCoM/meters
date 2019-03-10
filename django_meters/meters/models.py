from django.db import models
from datetime import date

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
            last_record = Records.objects.filter(date__lt=start_date.date).order_by('date').last().record
        except:
            last_record = 0

        for record in records_list:
            if last_record == 0:
                last_record = record.record
            record.consumption = record.record - last_record
            record.save()
            last_record = record.record


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






