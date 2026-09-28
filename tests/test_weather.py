import unittest
from unittest.mock import Mock, patch

from gcp_trial.weather import API_URL, fetch_weather


class FetchWeatherTests(unittest.TestCase):
    @patch("gcp_trial.weather.requests.get")
    def test_fetches_current_weather_for_city(self, get):
        response = Mock()
        response.json.return_value = {"name": "London"}
        get.return_value = response

        result = fetch_weather("London", "test-key")

        get.assert_called_once_with(
            API_URL,
            params={"q": "London", "appid": "test-key", "units": "metric"},
            timeout=10,
        )
        response.raise_for_status.assert_called_once_with()
        self.assertEqual(result, {"name": "London"})


if __name__ == "__main__":
    unittest.main()