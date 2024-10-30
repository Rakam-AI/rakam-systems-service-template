from unittest import TestCase
import requests

class TestVS(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_url = "http://localhost:8000/api/application"
        cls.processor_url = f"{cls.base_url}/internal/dataprocessor/"
        cls.search_url = f"{cls.base_url}/vector_store/search/"
        cls.vs_manager_inject_url = f"{cls.base_url}/vs_manager/inject/"
        cls.rag_url = f"{cls.base_url}/rag/"

    def test_dataprocessor(self):
        data = {"directory": "data"}
        response = requests.post(url=self.processor_url, json=data, timeout=10)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_search_vector_store(self):
        data = {"query": "another file"}
        response = requests.post(url=self.search_url, json=data, timeout=10)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_vs_manager_inject(self):
        response = requests.post(url=self.vs_manager_inject_url, timeout=10)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())

    def test_rag(self):
        data = {"test_query": "What is attention mechanism?"}
        response = requests.post(url=self.rag_url, json=data, timeout=30)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.json())
