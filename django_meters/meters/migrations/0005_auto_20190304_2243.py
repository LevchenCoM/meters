# Generated by Django 2.1.7 on 2019-03-04 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meters', '0004_auto_20190303_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='records',
            name='consumption',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='records',
            name='record',
            field=models.FloatField(),
        ),
    ]