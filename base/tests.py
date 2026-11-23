from django.test import TestCase
from django.urls import reverse


class ApiTests(TestCase):
    def test_qrng_hex(self):
        response = self.client.get("/api/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

    def test_decimal_array(self):
        response = self.client.post(
            "/api/getqrng_DecimalArray/",
            {"length": 10},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 10)
