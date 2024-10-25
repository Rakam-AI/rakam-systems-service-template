# from unittest import TestCase

# import requests

# class TestVS(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         # TODO : replace this with the "revert" function
#         cls.base_url = "http://localhost:8000/api/application/vector_store"
#         cls.search_url = f"{cls.base_url}/search/"

#     def test_health_endpoint(self):

#         # Missing an input json
#         response = requests.post(url=self.search_url, timeout=10)

#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {"status": "healthy"})




