from rest_framework import permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.cars.models import Car
from apps.cars.serializers import CarSerializer

from .models import ModerationLog
from .services import moderate_car


class ModerationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModerationLog
        fields = ['id', 'car', 'status', 'flagged_words', 'comment', 'created_at']


class ModerateCarView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, car_id):
        if request.user.role not in ['manager', 'admin']:
            return Response(
                {'error': 'Only managers can moderate ads'},
                status=403
            )

        result = moderate_car(car_id)
        return Response(result)


class CarModerationLogsView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, car_id):
        if request.user.role not in ['manager', 'admin']:
            return Response({'error': 'Access is denied'}, status=403)

        logs = ModerationLog.objects.filter(car_id=car_id)
        serializer = ModerationLogSerializer(logs, many=True)
        return Response(serializer.data)


class PendingCarsView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role not in ['manager', 'admin']:
            return Response({'error': 'Access is denied'}, status=403)

        pending_cars = Car.objects.filter(
            status__in=['pending', 'flagged']
        ).select_related('owner', 'make', 'model')

        serializer = CarSerializer(pending_cars, many=True)
        return Response(serializer.data)