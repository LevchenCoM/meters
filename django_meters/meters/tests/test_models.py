from django.test import TestCase
from meters.models import Meters, Records, ResourceType
from datetime import date
import pandas as pd


class ResourceTypeTest(TestCase):

    def create_resource_type(self):
        return ResourceType.objects.create(name='Water')

    def test_resource_creation(self):
        test_resource_type = self.create_resource_type()

        self.assertTrue(isinstance(test_resource_type, ResourceType))
        self.assertEqual(test_resource_type.__str__(), test_resource_type.name)


class MetersTest(TestCase):

    def setUp(self):
        self.test_resource = ResourceType.objects.create(name='Water')
        self.test_meter = Meters.objects.create(name='Office',
                                                resource_type=self.test_resource,
                                                unit='m3')

    def test_meter_creation(self):
        """ Checking object creation"""
        self.assertTrue(isinstance(self.test_meter, Meters))

    def test_meter_absolute_url(self):
        """ Checking absolute url fuctions"""
        self.assertEqual(self.test_meter.get_absolute_url(), "/meters/{}".format(self.test_meter.id))

    def test_meter_str(self):
        """ Checking __str__ function"""
        self.assertEqual(self.test_meter.__str__(), self.test_meter.name)


class RecordsTest(TestCase):

    def setUp(self):
        self.test_resource = ResourceType.objects.create(name='Water')
        self.test_meter = Meters.objects.create(name='Office',
                                                resource_type=self.test_resource,
                                                unit='m3')
        self.test_first_record = Records.objects.create(meter=self.test_meter,
                                                        date=date(2019,1,1),
                                                        record=1)
        self.test_second_record = Records.objects.create(meter=self.test_meter,
                                                         date=date(2019, 1, 2),
                                                         record=10)
        self.test_third_record = Records.objects.create(meter=self.test_meter,
                                                        date=date(2019, 1, 3),
                                                        record=25)



    def test_record_creation(self):
        """ Checking objects creation"""
        self.assertTrue(isinstance(self.test_first_record, Records))
        self.assertTrue(isinstance(self.test_second_record, Records))
        self.assertTrue(isinstance(self.test_third_record, Records))

    def test_last_reading_function(self):
        """ Check receipt last reading functionality"""
        self.assertEqual(self.test_meter.get_last_reading().id, self.test_third_record.id)

    def test_consumptions_recalculation(self):
        """ Check consumption recalculation functionality """

        """ First consumption recalculation """
        self.test_meter.consumptions_recalculation()

        test_first_record = Records.objects.get(pk=self.test_first_record.id)
        test_second_record = Records.objects.get(pk=self.test_second_record.id)
        test_third_record = Records.objects.get(pk=self.test_third_record.id)

        self.assertEqual(test_first_record.consumption, 0)
        self.assertEqual(test_second_record.consumption, 9.0)
        self.assertEqual(test_third_record.consumption, 15.0)

        """ Now we will update records and perform recalculating again """
        test_second_record.record = 12.0
        test_second_record.save()
        test_third_record.record = 33.0
        test_third_record.save()

        self.test_meter.consumptions_recalculation()

        test_first_record = Records.objects.get(pk=self.test_first_record.id)
        test_second_record = Records.objects.get(pk=self.test_second_record.id)
        test_third_record = Records.objects.get(pk=self.test_third_record.id)

        self.assertEqual(test_first_record.consumption, 0)
        self.assertEqual(test_second_record.consumption, 11.0)
        self.assertEqual(test_third_record.consumption, 21.0)

    def test_readings_import(self):
        """ Checking readings import functional """

        """ Create new DateFrame with new records"""
        data_dict = {'DATE': [date(2019, 1, 4),
                              date(2019, 1, 5),
                              date(2019, 1, 6)],
                    'VALUE': [35, 45, 60]}
        records_table = pd.DataFrame(data_dict)

        self.test_meter.import_readings(records_table)

        queryset = Records.objects.filter(date__in=data_dict['DATE']).order_by('date')

        self.assertEqual(list(queryset.values_list('date', flat=True)), data_dict['DATE'])
        self.assertEqual(list(queryset.values_list('record', flat=True)), data_dict['VALUE'])

        self.assertEqual(list(queryset.values_list('consumption', flat=True)), [10.0, 10.0, 15.0])














