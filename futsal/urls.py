from django.urls import path

from futsal.views import *

urlpatterns = [
    path('create_futsal/', FutsalView.as_view()),
    path('all_futsal/', ListAllFutsal.as_view()),
    path('booking/', BookingView.as_view()),
    path('booking_futsal/', UserBookingView.as_view()),
    path('my_booking/', MyBookingsView.as_view()),
    path('bookings/', OwnerBookingFutsalView.as_view()),
    path('<pk>', FutsalDetail.as_view()),
    path('add_training/', AddTrainings.as_view()),
    path('all_trainings/', ListAllTrainings.as_view()),
    path('become_member/', BecomeMember.as_view()),
    path('members/', ListOfAllMembers.as_view()),
    path('edit_futsal/<pk>', EditFutsalDetails.as_view()),
    path('futsal_rate/', FutsalRateView.as_view()),
    path('my_futsal/', OwnerFutsalView.as_view()),
    path('add_tournaments/', AddTournaments.as_view()),
    path('all_tournaments/', ListAllTournaments.as_view()),
    path('member_stat/', FutsalMemberStat.as_view()),
    path('booking_stat/', FutsalBookingStat.as_view()),
    path('total_stat/', AdminCount.as_view()),
    path('allbooking/stat/', AdminBookingStat.as_view()),
    path('booking/<pk>', BookingStatus.as_view()),
    path('membership/<pk>', MembershipStatus.as_view()),
    path('all_booking/', AdminBookingView.as_view()),
    path('5A/', List5AFutsalView.as_view()),
    path('7A/', List7AFutsalView.as_view()),
    path('5A/7A/', List5A7AFutsalView.as_view()),
    path('edit_member/<pk>',EditMembership.as_view())

]
