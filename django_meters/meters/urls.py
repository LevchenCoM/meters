from .views import home, meter_page, meter_delete, meter_add, meter_delete_records
from django.urls import path

urlpatterns = [
    path('', home),
    path('meters/<meter_id>', meter_page),
    path('add', meter_add),
    path('meters/<meter_id>/delete', meter_delete),
    path('meters/<meter_id>/delete-data', meter_delete_records),

]
