from django.shortcuts import render, redirect
from .models import Meters, Records
from .forms import MetersForm, CSVUploadForm
from django.shortcuts import get_object_or_404
from datetime import date
import numpy as np
import pandas as pd
import csv


def home(request):
    return render(request, 'home.html', {'objects': Meters.objects.all()})


def meter_page(request, meter_id):
    form = CSVUploadForm()
    meter = get_object_or_404(Meters, pk=meter_id)
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            """ Reading CSV file """
            readings_table = pd.read_csv(request.FILES['file'],
                                         sep=",",
                                         encoding='utf-8',
                                         parse_dates=['DATE'])
            meter.import_readings(readings_table)


            # data = csv.DictReader(request.FILES['file'].read().decode('utf-8').splitlines())
            # records_list = np.array()
            # # obj_list = []  # list of obj to bulk_create in the end of function
            # # dates_list = []  # list of dates to filter and delete previous records before bulk_create
            #
            # for row in data:
            #     date_record = row['DATE'].split('-')  # [0 - year, 1 - month, 2 - day]
            #     dt = date(int(date_record[0]), int(date_record[1]), int(date_record[2]))
            #     records_list.append([dt, float(row['VALUE']), 0])
            #
            #     # dates_list.append(dt)
            #     # db_record = Records(
            #     #     meter=meter,
            #     #     date=dt,
            #     #     record=float(row['VALUE'])
            #     # )
            #     # obj_list.append(db_record)
            #
            #
            # # Records.objects.filter(date__in=dates_list).delete() # delete previous records
            # # Records.objects.bulk_create(obj_list)                # create multiple object in one call to DB
            # # meter.consumptions_recalculation(min(dates_list))    # perform recalculation of consumptions


    records = Records.objects.filter(meter__id=meter_id)
    records_list = []  # list of lists with consumption and date - for chart
    for i in records:
        records_list.append([i.date.isoformat(), i.consumption])

    last_reading = meter.get_last_reading()
    if last_reading is not None:
        last_reading_date = last_reading.date.isoformat()
        last_reading_record = last_reading.record
    else:
        last_reading_date, last_reading_record = None, None

    context = {'form': form,
               'object': meter,
               'records_data': records_list,
               'last_reading_date': last_reading_date,
               'last_reading_record': last_reading_record}
    return render(request, 'meter_page.html', context)


def meter_add(request):
    form = MetersForm()
    context = {'form': form}
    if request.method == "POST":
        form = MetersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    return render(request, 'meter_add.html', context)


def meter_delete(request, meter_id):
    meter = get_object_or_404(Meters, pk=meter_id)
    meter.delete()
    return redirect("/")


def meter_delete_records(request, meter_id):
    meter = get_object_or_404(Meters, pk=meter_id)
    if request.method == "POST":
        """Delete all records for meter"""
        Records.objects.filter(meter_id=meter_id).delete()
        return redirect(meter.get_absolute_url())
