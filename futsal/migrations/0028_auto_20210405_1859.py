# Generated by Django 3.1.7 on 2021-04-05 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('futsal', '0027_remove_tournaments_tourno_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbooking',
            name='user_book_time',
            field=models.CharField(choices=[('6 AM -7 AM', '6 AM -7 AM'), ('7 AM -8 AM', '7 AM -8 AM'), ('8 AM -9 AM', '8 AM -9 AM'), ('9 AM -10 AM', '9 AM -10 AM'), ('10 AM -11 AM', '10 AM -11 AM'), ('11 AM -12 PM', '11 AM -12 PM'), ('12 PM -1 PM', '12 PM -1 PM'), ('1 PM -2 PM', '1 PM -2 PM'), ('2 PM -3 PM', '2 PM -3 PM'), ('3 PM -4 PM', '3 PM -4 PM'), ('4 PM -5 PM', '4 PM -5 PM'), ('5 PM -6 PM', '5 PM -6 PM'), ('6 PM -7 PM', '6 PM -7 PM'), ('7 PM -8 PM', '7 PM -8 PM'), ('8 PM -9 PM', '8 PM -9 PM')], max_length=20),
        ),
    ]
