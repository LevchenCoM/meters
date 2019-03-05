from django.db import models


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

    class Meta:
        verbose_name = "Meter"
        verbose_name_plural = "Meters"


class Records(models.Model):
    meter = models.ForeignKey(Meters, null=True, on_delete=models.SET_NULL)
    date = models.DateField(blank=False, null=False)
    record = models.FloatField()
    consumption = models.FloatField()

    class Meta:
        get_latest_by = 'date'

