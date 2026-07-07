from django.db import models


class TenderOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "Kutilmoqda"),
        ("processing", "Ishlanmoqda"),
        ("done", "Tayyor"),
        ("error", "Xatolik"),
    ]

    company_name = models.CharField(max_length=255, verbose_name="Kompaniya nomi")
    company_inn = models.CharField(max_length=20, verbose_name="INN")
    company_activity = models.TextField(verbose_name="Kompaniya faoliyati")
    company_experience = models.TextField(verbose_name="Tajriba")
    tender_url = models.URLField(verbose_name="Tender linki")
    tender_title = models.CharField(max_length=500, blank=True, verbose_name="Tender nomi")
    tender_description = models.TextField(blank=True, verbose_name="Tender tavsifi")
    price_offer = models.CharField(max_length=255, verbose_name="Narx taklifi")
    generated_document = models.TextField(blank=True, verbose_name="AI yozgan hujjat")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tender buyurtma"
        verbose_name_plural = "Tender buyurtmalar"

    def __str__(self):
        return f"{self.company_name} - {self.tender_title or self.tender_url}"
