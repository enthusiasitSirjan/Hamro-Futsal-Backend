# Generated by Django 3.1.7 on 2021-04-03 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('futsal', '0024_auto_20210402_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='futsal',
            name='fut_map',
            field=models.CharField(default=2, max_length=300),
            preserve_default=False,
        ),
    ]
