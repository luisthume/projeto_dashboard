# Generated by Django 3.1.6 on 2021-02-05 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20210201_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nfe',
            name='venc_dates',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
