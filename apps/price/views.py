from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import fetch_rates_from_privatbank, get_today_rates


class CurrentRatesView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        rates = get_today_rates()
        return Response({
            'USD_to_UAH': rates.get('USD'),
            'EUR_to_UAH': rates.get('EUR'),
        })


class RefreshRatesView(APIView):
    def get(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Only admins'}, status=403)
        rates = fetch_rates_from_privatbank()
        return Response({'message': 'Rates have been updated', 'rates': {
            k: str(v) for k, v in rates.items()
        }})