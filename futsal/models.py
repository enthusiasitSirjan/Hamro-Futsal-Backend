from django.db import models

# Create your models here.
from accounts.models import Account


class Futsal(models.Model):
    futsal_type = [
        ('7A', '7A'),
        ('5A', '5A'),
        ('5A/7A', '5A/7A'),
    ]
    futsal_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    fut_type = models.CharField(max_length=10, choices=futsal_type)
    location = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    contact_email = models.EmailField(null=True)
    fut_phone = models.CharField(max_length=100)
    futsal_rate = models.PositiveIntegerField(default=0)
    fut_image = models.ImageField(width_field=None, height_field=None, null=True)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    fut_map = models.CharField(max_length=300)


class Booking(models.Model):
    futsal_book_type = [
        ('7A', '7A'),
        ('5A', '5A')
    ]
    user_name = models.CharField(max_length=100)
    user_phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    book_date = models.DateField()
    book_time = models.TimeField()
    book_fut_type = models.CharField(max_length=2, choices=futsal_book_type)


class UserBooking(models.Model):
    user_fut_type = [
        ('7A', '7A'),
        ('5A', '5A'),
        ('5A/7A', '5A/7A'),

    ]
    user_book_time_slot = [
        ('6 AM -7 AM', '6 AM -7 AM'),
        ('7 AM -8 AM', '7 AM -8 AM'),
        ('8 AM -9 AM', '8 AM -9 AM'),
        ('9 AM -10 AM', '9 AM -10 AM'),
        ('10 AM -11 AM', '10 AM -11 AM'),
        ('11 AM -12 PM', '11 AM -12 PM'),
        ('12 PM -1 PM', '12 PM -1 PM'),
        ('1 PM -2 PM', '1 PM -2 PM'),
        ('2 PM -3 PM', '2 PM -3 PM'),
        ('3 PM -4 PM', '3 PM -4 PM'),
        ('4 PM -5 PM', '4 PM -5 PM'),
        ('5 PM -6 PM', '5 PM -6 PM'),
        ('6 PM -7 PM', '6 PM -7 PM'),
        ('7 PM -8 PM', '7 PM -8 PM'),
        ('8 PM -9 PM', '8 PM -9 PM'),

    ]
    booked_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user_book_date = models.DateField()
    user_book_time = models.CharField(max_length=20, choices=user_book_time_slot)
    user_book_fut_type = models.CharField(max_length=7, choices=user_fut_type)
    futsal = models.ForeignKey(Futsal, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default="Pending")


class Trainings(models.Model):
    t_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    t_date = models.CharField(max_length=100)
    t_location = models.CharField(max_length=100)
    t_price = models.PositiveIntegerField()
    t_age = models.CharField(max_length=100)
    t_sessions = models.CharField(max_length=200)
    t_photo = models.ImageField(null=True)
    t_contact_phone = models.CharField(max_length=200)
    t_email = models.EmailField(null=True)


class Membership(models.Model):
    mem_type = [
        ('Gold', 'Gold'),
        ('Platinum', 'Platinum'),
        ('Diamond', 'Diamond')
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    member_type = models.CharField(max_length=20, choices=mem_type)
    member = models.ForeignKey(Account, on_delete=models.CASCADE)
    futsal = models.ForeignKey(Futsal, on_delete=models.CASCADE)
    pay_status = models.CharField(max_length=30, default="Pending")


class Tournaments(models.Model):
    tourno_photo = models.ImageField(null=True)
    tourno_name = models.CharField(max_length=100)
    tourno_location = models.CharField(max_length=100)
    tourno_date = models.CharField(max_length=200)
