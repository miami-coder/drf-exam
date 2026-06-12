from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cars.models import Car

from .services import get_price_stats, get_view_stats, record_view


class CarStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({'error': 'No ads found.'}, status=404)

        record_view(car_id)

        if car.owner != request.user:
            return Response({'error': 'Statistics are available only to the owner'}, status=403)

        if request.user.account_type != 'premium':
            return Response({
                'error': 'Statistics are only available for Premium accounts.',
                'upgrade_url': '/pricing/upgrade/'
            }, status=403)

        view_stats = get_view_stats(car_id)
        price_stats = get_price_stats(car_id)

        return Response({
            'car_id': car_id,
            'views': view_stats,
            'pricing': price_stats,
        })


class RecordViewPublicView(APIView):

    permission_classes = [permissions.AllowAny]

    def post(self, request, car_id):
        record_view(car_id)
        return Response({'recorded': True})