import self as self
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.Email import SendBookingInformation
from accounts.models import Account
from accounts.permission import IsOwner, IsUser, IsAdmin
from futsal.models import Futsal, Booking, UserBooking, Trainings, Membership, Tournaments
from futsal.serializer import FutsalSerializer, CreateFutsalSerializer, BookingFutsalSerializer, \
    UserBookingFutsalSerializer, ListMyBookingSerializer, OwnerBookingFutsalSerializer, \
    TrainingSerializer, FutsalMembership, ShowMembers, TournamentSerializer


class FutsalView(CreateAPIView):
    # queryset = Futsal.objects.all
    def get_queryset(self):
        return Futsal.objects.all()

    serializer_class = CreateFutsalSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class OwnerFutsalView(ListAPIView):
    def get_queryset(self):
        return Futsal.objects.filter(owner=self.request.user)

    serializer_class = FutsalSerializer
    permission_classes = []


class ListAllFutsal(ListAPIView):
    def get_queryset(self):
        return Futsal.objects.all()

    serializer_class = FutsalSerializer
    permission_classes = []
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['futsal_name', 'location', 'futsal_rate']


class List5AFutsalView(ListAPIView):
    def get_queryset(self):
        return Futsal.objects.filter(fut_type="5A")

    serializer_class = FutsalSerializer
    permission_classes = []


class List7AFutsalView(ListAPIView):
    def get_queryset(self):
        return Futsal.objects.filter(fut_type="7A")

    serializer_class = FutsalSerializer
    permission_classes = []


class List5A7AFutsalView(ListAPIView):
    def get_queryset(self):
        return Futsal.objects.filter(fut_type="5A/7A")

    serializer_class = FutsalSerializer
    permission_classes = []


class AdminCount(APIView):
    def get(self, request):
        AllUser = Account.objects.filter(user_role='USER').count()
        AllOwner = Account.objects.filter(user_role='OWNER').count()
        AllFutsal = Futsal.objects.all().count()
        return Response({"TotalUser": AllUser, "TotalFutsalOwner": AllOwner, "TotalFutsal": AllFutsal})


class FutsalDetail(RetrieveAPIView):
    queryset = Futsal.objects.all()
    serializer_class = FutsalSerializer


class EditFutsalDetails(RetrieveUpdateAPIView):
    def get_queryset(self):
        return Futsal.objects.filter(owner=self.request.user)

    serializer_class = FutsalSerializer
    permission_classes = []


class BookingView(CreateAPIView):
    def get_queryset(self):
        return Booking.objects.all()

    serializer_class = BookingFutsalSerializer
    permission_classes = []


class UserBookingView(CreateAPIView):
    def get_queryset(self):
        return UserBooking.objects.all()

    serializer_class = UserBookingFutsalSerializer
    permission_classes = [IsUser]

    def perform_create(self, serializer):
        serializer.save(booked_by=self.request.user)


class EditUserBookingView(RetrieveUpdateAPIView):
    def get_queryset(self):
        return UserBooking.objects.filter(futsal__owner=self.request.user)

    serializer_class = UserBookingFutsalSerializer


class AdminBookingView(ListAPIView):
    def get_queryset(self):
        return UserBooking.objects.all()

    serializer_class = ListMyBookingSerializer
    permission_classes = [IsAdmin]


class AdminBookingStat(APIView):
    def get(self, request):
        TotalBookings = UserBooking.objects.filter(status="Pending").count()
        TotalCancelledBookings = UserBooking.objects.filter(status="Cancelled").count()
        TotalValidBookings = UserBooking.objects.filter(status="Approved").count()
        return Response(
            {"TotalBookings": TotalBookings, "TotalCancelledBookings": TotalCancelledBookings,
             "TotalValidBookings": TotalValidBookings})


class FutsalRateView(APIView):
    def post(self, request):
        futsal_id = request.data["futsal_id"]
        price = Futsal.objects.filter(id=futsal_id).values('futsal_rate')[0]["futsal_rate"]
        user = self.request.user
        member = Membership.objects.filter(member=user, futsal__id=futsal_id)

        if member:
            member_type = member.values("member_type")[0]["member_type"]
            discount = 0
            total = 0
            print(member_type)
            if member_type == 'Gold':
                discount = 5
            elif member_type == 'Platinum':
                discount = 10
            elif member_type == 'Diamond':
                discount = 15

            return Response(
                {"member_type": member_type, "price": price, "discount": discount,
                 "Total": round((price - ((discount / 100) * price)))})

        return Response({"price": price, "discount": 0, "Total": price})


# User Booked Futsal
class MyBookingsView(ListAPIView):
    def get_queryset(self):
        return UserBooking.objects.filter(booked_by=self.request.user)

    serializer_class = ListMyBookingSerializer
    permission_classes = []


# Owner My futsal booking
class OwnerBookingFutsalView(ListAPIView):
    def get_queryset(self):
        return UserBooking.objects.filter(futsal__owner=self.request.user)

    serializer_class = OwnerBookingFutsalSerializer
    permission_classes = []


class BookingStatus(RetrieveUpdateAPIView):
    def get_queryset(self):
        return UserBooking.objects.filter(futsal__owner=self.request.user)

    serializer_class = OwnerBookingFutsalSerializer
    permission_classes = []


class FutsalBookingStat(APIView):
    def get(self, request):
        AllBookings = UserBooking.objects.filter(futsal__owner=self.request.user, status="Pending").count()
        CancelledBookings = UserBooking.objects.filter(futsal__owner=self.request.user, status="Cancelled").count()
        ValidBookings = UserBooking.objects.filter(futsal__owner=self.request.user, status="Approved").count()
        return Response(
            {"PendingBookings": AllBookings, "CancelledBookings": CancelledBookings, "ValidBookings": ValidBookings})


class AddTrainings(CreateAPIView):
    queryset = Trainings.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = []


class ListAllTrainings(ListAPIView):
    queryset = Trainings.objects.all()
    serializer_class = TrainingSerializer
    permission_classes = []


class AddTournaments(CreateAPIView):
    queryset = Tournaments.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = []


class ListAllTournaments(ListAPIView):
    queryset = Tournaments.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = []


class BecomeMember(CreateAPIView):
    def get_queryset(self):
        return Membership.objects.all()

    serializer_class = FutsalMembership
    permission_classes = [IsUser]

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)


class EditMembership(RetrieveUpdateAPIView):
    def get_queryset(self):
        return Membership.objects.all()

    serializer_class = FutsalMembership
    permission_classes = [IsOwner]


class ListOfAllMembers(ListAPIView):
    def get_queryset(self):
        # my_futsal=Futsal.objects.filter(owner=self.request.user)
        # print(my_futsal[0])
        # return UserBooking.objects.filter(futsal=my_futsal[0])
        return Membership.objects.filter(futsal__owner=self.request.user)

    serializer_class = ShowMembers
    permission_classes = []


class MembershipStatus(RetrieveUpdateAPIView):
    def get_queryset(self):
        return Membership.objects.filter(futsal__owner=self.request.user)

    serializer_class = ShowMembers
    permission_classes = []


class FutsalMemberStat(APIView):
    def get(self, request):
        AllMembers = Membership.objects.filter(futsal__owner=self.request.user, pay_status="Pending").count()
        CancelledMembers = Membership.objects.filter(futsal__owner=self.request.user, pay_status="Cancelled").count()
        ValidMembers = Membership.objects.filter(futsal__owner=self.request.user, pay_status="Approved").count()
        return Response(
            {"PendingMembers": AllMembers, "CancelledMembers": CancelledMembers, "ValidMembers": ValidMembers})




# class SearchFutsalName(APIView):
#     def post(self, request):
#         searched_futsal = request.data['searched_futsal']
#         if Futsal.objects.filter(futsal_name=searched_futsal):
#             results = Futsal.objects.filter(futsal_name=searched_futsal).values()
#             print("Results", results)
#             return Response(results)
#         return Response({"error_msg": "No Futsal Data"})
#
#
# class SearchFutsalLocation(APIView):
#     def post(self, request):
#         searched_futsal = request.data['searched_futsal']
#         if Futsal.objects.filter(location=searched_futsal):
#             results = Futsal.objects.filter(location=searched_futsal).values()
#             print("Results", results)
#             return Response(results)
#         return Response({"error_msg": "No Futsal Data"})

# class NextFutsalView(APIView):
#
#     def post(self, request):
#         print(request, request.data)
#         data = request.data
#         user = self.request.user
#         if Futsal.objects.filter(owner=user):
#             return Response({'Success': False, 'error_msg': "User has already created futsal"})
#         Futsal.objects.create(
#             futsal_name=data['futsal_name'],
#             phn_number=data['phn_number'],
#             fut_type=data['fut_type'],
#             location=data['location'],
#             description=data['description'],
#             contact_email=data['contact_email'],
#             owner=user
#
#         )
#         # print(data)
#         # data['user'] = user.id
#         # serializer = FutsalSerializer(data=data)
#         #
#         # if serializer.is_valid():
#         #     print ("Success")
#         # else:
#         #     data = serializer.errors
#         #     return Response({"success":False})
#         #     print(data)
#
#         return Response({'Success': True})
