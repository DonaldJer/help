import unittest, requests
# from urllib.request import Request, urlopen

class ServerTestCase(unittest.TestCase):
    def test_missing_user_info(self):
        # Test when user information is missing in a request
        # Expected behavior: Server returns 401 status code with proper error message

        payload = {"password": "1234-pw"}
        response = requests.post("http://localhost:5000/quote", json=payload)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "User info error")

    # def test_invalid_user_info(self):
    #     # Test when user information is invalid in a request
    #     # Expected behavior: Server returns 401 status code with proper error message

    #     payload = {"username": "1234", "password": "5678-pw"}
    #     response = requests.post("http://localhost:5000/quote", json=payload)
    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(response.json()["error"], "User info error")

    # def test_quote_web_missing_fields(self):
    #     # Test when a field is missing in a request
    #     # Expected behavior: Server returns 400 status code with proper error message

    #     payload = {
    #         "username": "1234", 
    #         "password": "1234-pw", 
    #         "concurrency": 2
    #     }
    #     response = requests.post("http://localhost:5000/quote", json=payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json()["error"], "Missing field protocol")

    # def test_quote_web_invalid_fields(self):
    #     # Test when a field is invalid in a request
    #     # Expected behavior: Server returns 400 status code with proper error message

    #     payload = {
    #         "username": "1234",
    #         "password": "1234-pw",
    #         "protocol": "tcp",
    #         "concurrency": 0,
    #     }
    #     response = requests.post("http://localhost:5000/quote", json=payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json()["error"], "Invalid field concurrency")

    # def test_pi_web_missing_fields(self):
    #     # Test when a field is missing in a request
    #     # Expected behavior: Server returns 400 status code with proper error message

    #     payload = {"username": "1234", "password": "1234-pw", "concurrency": 2}
    #     response = requests.post("http://localhost:5000/pi", json=payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json()["error"], "Missing field simulations")

    # def test_pi_web_invalid_fields(self):
    #     # Test when a field is invalid in a request
    #     # Expected behavior: Server returns 400 status code with proper error message

    #     payload = {
    #         "username": "1234",
    #         "password": "1234-pw",
    #         "simulations": 10000,
    #         "concurrency": 0,
    #     }
    #     response = requests.post("http://localhost:5000/pi", json=payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json()["error"], "Invalid field concurrency")

    # def test_quote_web_service(self):
    #     # Test the quote web service
    #     # Expected behavior: Server returns the requested number of quotes

    #     payload = {
    #         "username": "1234",
    #         "password": "1234-pw",
    #         "protocol": "tcp",
    #         "concurrency": 2,
    #     }
    #     response = requests.post("http://localhost:5000/quote", json=payload)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("quotes", response.json())
    #     self.assertIsInstance(response.json()["quotes"], list)
    #     self.assertEqual(len(response.json()["quotes"]), payload["concurrency"])

    # def test_pi_web_service(self):
    #     # Test the pi web service
    #     # Expected behavior: Server returns an approximate value of pi

    #     payload = {
    #         "username": "1234",
    #         "password": "1234-pw",
    #         "simulations": 10000,
    #         "concurrency": 4,
    #     }
    #     response = requests.post("http://localhost:5000/pi", json=payload)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("pi", response.json())
    #     self.assertIsInstance(response.json()["pi"], float)

    # def test_pi_web_processing_time(self):
    #     # Test the pi web service that a higher level of concurrency generally results in a smaller processing time than a lower level of concurrency
    #     # Expected behavior: higher level of concurrency processing time is small than smaller level of concurrency processing time

    #     higher_concurrency_payload = {
    #         "username": "1234",
    #         "password": "1234-pw",
    #         "simulations": 100000000,
    #         "concurrency": 4,
    #     }
    #     higher_concurrency_response = requests.post("http://localhost:5000/pi", json=higher_concurrency_payload)
    #     self.assertEqual(higher_concurrency_response.status_code, 200)
    #     self.assertIn("pi", higher_concurrency_response.json())
    #     self.assertIsInstance(higher_concurrency_response.json()["pi"], float)

    #     smaller_concurrency_payload = {
    #         "username": "1234",
    #         "password": "1234-pw",
    #         "simulations": 100000000,
    #         "concurrency": 1,
    #     }
    #     smaller_concurrency_response = requests.post("http://localhost:5000/pi", json=smaller_concurrency_payload)
    #     self.assertEqual(smaller_concurrency_response.status_code, 200)
    #     self.assertIn("pi", smaller_concurrency_response.json())
    #     self.assertIsInstance(smaller_concurrency_response.json()["pi"], float)

    #     self.assertLess(higher_concurrency_response.json()["processing_time"], smaller_concurrency_response.json()["processing_time"])

if __name__ == "__main__":
    unittest.main()
