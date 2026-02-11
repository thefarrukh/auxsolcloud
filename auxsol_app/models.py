from django.db import models
from django.utils import timezone


class AuxsolToken(models.Model):
    """Auxsol Cloud API token'ini saqlash"""
    access_token = models.CharField(
        max_length=500,
        help_text="Auxsol API access token"
    )
    expires_at = models.DateTimeField(
        help_text="Token muddati tugash vaqti"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Token yaratilgan vaqt"
    )

    def is_valid(self):
        """Token hali amal qilmoqda yoki o'tib ketgan?"""
        return timezone.now() < self.expires_at

    def __str__(self):
        status = "Valid" if self.is_valid() else "Expired"
        return f"Token - {status} (Expires: {self.expires_at})"

    class Meta:
        verbose_name = 'Auxsol Token'
        verbose_name_plural = 'Auxsol Tokens'
        ordering = ['-created_at']  # ✅ BUGFIX: Oxirgi token birinchi
        indexes = [
            models.Index(fields=['-created_at']),
        ]


class InverterData(models.Model):
    # Asosiy elektr ko'rsatkichlari
    current_power = models.DecimalField(max_digits=10, decimal_places=3)
    daily_yield = models.DecimalField(max_digits=10, decimal_places=2)

    # Yangi qo'shilgan maydonlar uchun default=0 yoki null=True beramiz
    monthly_yield = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_yield = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Iqtisodiy va ekologik ko'rsatkichlar
    daily_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_earnings = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    co2_saved = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    trees_planted = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.current_power} kW"

    class Meta:
        verbose_name = 'Inverter Data'
        verbose_name_plural = 'Inverter Data'
        ordering = ['-timestamp']  # ✅ BUGFIX: Eng oxirgi ma'lumot birinchi
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['current_power']),
        ]