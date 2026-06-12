from rest_framework import generics, permissions

from apps.moder.services import moderate_car
from apps.price.services import convert_price, get_today_rates
from apps.stats.services import record_view

from .models import Car, CarModel, Make
from .permissions import IsOwnerOrManagerOrAdmin, IsSellerOrAdmin
from .serializers import CarModelSerializer, CarSerializer, MakeSerializer


class MakeListView(generics.ListAPIView):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer
    permission_classes = [permissions.AllowAny]


class CarModelListView(generics.ListAPIView):
    serializer_class = CarModelSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        make_id = self.kwargs.get('make_id')
        return CarModel.objects.filter(make_id=make_id)


class CarListCreateView(generics.ListCreateAPIView):
    serializer_class = CarSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [IsSellerOrAdmin()]

    def get_queryset(self):
        return Car.objects.filter(status='active').select_related('make', 'model', 'owner')

    def perform_create(self, serializer):
        rates = get_today_rates()
        price = serializer.validated_data.get('price')
        currency = serializer.validated_data.get('currency', 'USD')
        converted = convert_price(price, currency, rates)
        car = serializer.save(owner=self.request.user, **converted)
        moderate_car(car.id)


class CarDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsOwnerOrManagerOrAdmin]

    def retrieve(self, request, *args, **kwargs):
        record_view(kwargs.get('pk'))
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        car = self.get_object()
        updated_car = serializer.save(edit_count=car.edit_count + 1)
        moderate_car(updated_car.pk)
