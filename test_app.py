import unittest
from unittest.mock import MagicMock, patch
from falcon.testing import TestClient
from requests.exceptions import RequestException
from app import app

class TestAppInfoResource(unittest.TestCase):
    
    def setUp(self):
        self.client = TestClient(app)
        self.mock_request = MagicMock(spec=['bounded_stream', 'content_type', 'stream_len'])
        self.mock_response = MagicMock()

    def test_successful_post_request(self):
        mock_body = "url=https://en.aptoide.com/app"
        self.mock_request.bounded_stream.read.return_value.decode.return_value = mock_body
        self.mock_request.content_type = 'application/x-www-form-urlencoded'
        self.mock_request.stream_len = len(mock_body.encode('utf-8'))

        # Configure mock_response to simulate requests.get
        self.mock_response.status_code = 200
        self.mock_response.text = """
            <div class="info__DetailsCol-sc-hpbddq-11 kvOojZ">
                <span class="info__APKDetail-sc-hpbddq-8 buGwFg">Name: Test App</span>
                <span class="info__APKDetail-sc-hpbddq-8 buGwFg">Downloads: 1000+</span>
                <span class="info__APKDetail-sc-hpbddq-8 buGwFg">Version: 1.0</span>
                <span class="info__APKDetail-sc-hpbddq-8 buGwFg">Release Date: 2024-06-15</span>
            </div>
            <p class="details__Paragraph-sc-rnz8ql-2 emzOuH">This is a test description.</p>
        """

        # Patch requests.get to return the mock_response
        with patch('requests.get', return_value=self.mock_response):
            response = self.client.simulate_post('/get-app-info', headers={'Content-Type': 'application/x-www-form-urlencoded'}, body=mock_body)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')

        json_data = response.json
        self.assertEqual(json_data['Name'], 'Test App')
        self.assertEqual(json_data['Downloads'], '1000+')
        self.assertEqual(json_data['Version'], '1.0')
        self.assertEqual(json_data['Release Date'], '2024-06-15')
        self.assertEqual(json_data['Description'], 'This is a test description.')

    def test_missing_url_parameter(self):
        mock_body = ""
        self.mock_request.bounded_stream.read.return_value.decode.return_value = mock_body
        self.mock_request.content_type = 'application/x-www-form-urlencoded'
        self.mock_request.stream_len = len(mock_body.encode('utf-8'))

        response = self.client.simulate_post('/get-app-info', headers={'Content-Type': 'application/x-www-form-urlencoded'}, body=mock_body)

        self.assertEqual(response.status_code, 400)

    def test_invalid_url_parameter(self):
        mock_body = "url=https://example.com"
        self.mock_request.bounded_stream.read.return_value.decode.return_value = mock_body
        self.mock_request.content_type = 'application/x-www-form-urlencoded'
        self.mock_request.stream_len = len(mock_body.encode('utf-8'))

        response = self.client.simulate_post('/get-app-info', headers={'Content-Type': 'application/x-www-form-urlencoded'}, body=mock_body)

        self.assertEqual(response.status_code, 400)

    def test_app_not_found(self):
        mock_body = "url=https://en.aptoide.com/invalid-app"
        self.mock_request.bounded_stream.read.return_value.decode.return_value = mock_body
        self.mock_request.content_type = 'application/x-www-form-urlencoded'
        self.mock_request.stream_len = len(mock_body.encode('utf-8'))

        # Configure mock_response to simulate requests.get raising RequestException
        self.mock_response.raise_for_status.side_effect = RequestException

        # Patch requests.get to raise RequestException
        with patch('requests.get', side_effect=self.mock_response.raise_for_status):
            response = self.client.simulate_post('/get-app-info', headers={'Content-Type': 'application/x-www-form-urlencoded'}, body=mock_body)

        # Assertions
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
