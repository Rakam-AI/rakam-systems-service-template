from unittest import TestCase

import requests


class TestHealth(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_url = "http://localhost:8000"
        cls.health_check_url = f"{cls.base_url}/health/"

    def test_health_endpoint(self):
        response = requests.get(url=self.health_check_url, timeout=10)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "healthy"})
