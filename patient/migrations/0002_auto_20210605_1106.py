# Generated by Django 3.1.7 on 2021-06-05 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]