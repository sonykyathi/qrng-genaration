from django.db import models


class Qrng(models.Model):
    data = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"QRNG result {self.pk}"
