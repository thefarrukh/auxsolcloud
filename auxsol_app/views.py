from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import InverterData
import logging

logger = logging.getLogger(__name__)


@extend_schema(
    summary="Quyosh paneli ma'lumotlarini olish",
    description="Oxirgi 24 soatlik quvvat ma'lumotlarini grafik uchun qaytaradi.",
    responses={200: dict}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def get_chart_data(request):
    """
    Grafik uchun JSON ma'lumotlarini qaytaruvchi API.
    Oxirgi 20 ta ma'lumotni qaytaradi.
    """
    try:
        # ✅ BUGFIX: Oxirgi 20 ta ma'lumotni olish
        data = InverterData.objects.all().order_by('-timestamp')[:20]

        if not data:
            logger.warning("⚠️ Ma'lumot topilmadi")
            return Response({
                'labels': [],
                'values': [],
                'message': 'No data available'
            }, status=200)

        # ✅ BUGFIX: Vaqtni reverse qilish (eski ma'lumot birinchi)
        data_list = list(reversed(list(data)))

        labels = [d.timestamp.strftime('%H:%M') for d in data_list]
        values = [float(d.current_power) for d in data_list]

        logger.info(f"✅ Chart data qaytarildi: {len(labels)} ta nuqta")

        return Response({
            'labels': labels,
            'values': values,
            'count': len(labels)
        })

    except Exception as e:
        logger.error(f"❌ Chart data xatosi: {e}")
        return Response({
            'error': str(e)
        }, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_latest_data(request):
    """
    Eng oxirgi ma'lumotni olish
    """
    try:
        # ✅ BUGFIX: Eng oxirgi ma'lumotni olish
        latest = InverterData.objects.latest('timestamp')

        return Response({
            'timestamp': latest.timestamp.isoformat(),
            'current_power': float(latest.current_power),
            'daily_yield': float(latest.daily_yield),
            'total_yield': float(latest.total_yield)
        })

    except InverterData.DoesNotExist:
        logger.warning("⚠️ Ma'lumot topilmadi")
        return Response({
            'error': 'No data available'
        }, status=404)
    except Exception as e:
        logger.error(f"❌ Latest data xatosi: {e}")
        return Response({
            'error': str(e)
        }, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_statistics(request):
    """
    Statistikani olish (min, max, avg)
    """
    try:
        # ✅ BUGFIX: Statistika hisoblash
        data = InverterData.objects.all()

        if not data:
            return Response({
                'error': 'No data available'
            }, status=404)

        current_powers = [float(d.current_power) for d in data]

        stats = {
            'min_power': min(current_powers),
            'max_power': max(current_powers),
            'avg_power': sum(current_powers) / len(current_powers),
            'total_count': len(current_powers),
            'latest_daily_yield': float(data.latest('timestamp').daily_yield),
            'latest_total_yield': float(data.latest('timestamp').total_yield)
        }

        logger.info(f"✅ Statistics: {stats}")
        return Response(stats)

    except Exception as e:
        logger.error(f"❌ Statistics xatosi: {e}")
        return Response({
            'error': str(e)
        }, status=500)