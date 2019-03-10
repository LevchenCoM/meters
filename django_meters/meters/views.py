from django.shortcuts import render, redirect
from .models import Meters, Records
from .forms import MetersForm, CSVUploadForm
from django.shortcuts import get_object_or_404
from datetime import date
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
            data = csv.DictReader(request.FILES['file'].read().decode('utf-8').splitlines())
            start_date = date(2200,1,1)
            for row in data:
                date_record = row['DATE'].split('-')  # [0 - year, 1 - month, 2 - day]
                dt = date(int(date_record[0]), int(date_record[1]), int(date_record[2]))

                try:
                    db_record = Records.objects.get(meter__id=meter_id, date=dt)
                    db_record.record = float(row['VALUE'])
                    db_record.save()
                except:
                    db_record = Records(
                        meter = meter,
                        date  = dt,
                        record = float(row['VALUE'])
                    )
                    db_record.save()
                if dt < start_date:
                    start_date = dt

            meter.consumptions_recalculation(start_date) #perform recalculation of consumptions

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
