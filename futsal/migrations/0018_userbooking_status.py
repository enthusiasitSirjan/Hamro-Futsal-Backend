# Generated by Django 3.1.7 on 2021-03-29 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('futsal', '0017_auto_20210329_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='userbooking',
            name='status',
            field=models.CharField(default='Pending', max_length=30),
        ),
    ]
