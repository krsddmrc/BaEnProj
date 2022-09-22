from django.shortcuts import render
from requests import request
from .serializers import FlightSerializer, ReservationSerializer, StaffFlightSerializer
from .models import Flight, Passenger, Reservation
from rest_framework import viewsets
from .permission import IsStafforReadOnly
from datetime import datetime, date
from django.db.models import Q


class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsStafforReadOnly,)

    def get_serializer_class(self):        #! iki serializer yazdık logic ile hangisini seçeceğini belirlemek için yazdık
        serializer = super().get_serializer_class()
        if self.request.user.is_staff:
            return StaffFlightSerializer
        return serializer

    def get_queryset(self):  #! staff'ların   güncel saaten sonraki uçuşları görmesi için
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        today = date.today()
        print(current_time)

        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            return Flight.objects.filter(Q(date_of_departure__gte=today) | Q(date_of_departure=today, etd__gt=current_time))
        #! aşağıdaki else aynı görevi yapıyor.
        #else:
        #    queryset = Flight.objects.filter(date_of_departure__gt=today)
        #    if Flight.objects.filter(date_of_departure=today):
        #        today_qs = Flight.objects.filter(date_of_departure=today).filter(etd__gt=current_time)
        #        queryset = queryset.union(today_qs)  #! iki queryset'i birleştirmek
        #    return queryset

class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = Reservation.objects.all()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)
