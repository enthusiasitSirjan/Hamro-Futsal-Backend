from django.contrib import admin

# Register your models here.
from futsal.models import Futsal, UserBooking, Trainings, Membership, Tournaments

admin.site.register(Futsal)
# admin.site.register(Booking)
admin.site.register(UserBooking)
admin.site.register(Trainings)
admin.site.register(Membership)
admin.site.register(Tournaments)