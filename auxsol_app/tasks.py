from celery import shared_task
from .services.client import AuxsolClient
from .models import InverterData
import logging

logger = logging.getLogger(__name__)


@shared_task
def sync_solar_data():
    client = AuxsolClient()
    if client.login():
        res = client.get_solar_data(12973)
        if res and res.get("code") == "AWX-0000":
            data = res.get("data", {})
            energy = data.get("energyData", {})

            InverterData.objects.create(
                current_power=energy.get("power", 0),
                daily_yield=energy.get("y", 0),
                monthly_yield=energy.get("ym", 0),
                total_yield=energy.get("yt", 0),

                daily_earnings=energy.get("earn", 0),
                total_earnings=energy.get("earnT", 0),
                co2_saved=energy.get("co2", 0),
                trees_planted=energy.get("treePlants", 0)
            )
            return "Success: Full data saved"
    return "Failed"