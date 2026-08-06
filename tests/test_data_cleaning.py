import unittest
from unittest.mock import patch

from utils.data_cleaning import summarize_data


class DataCleaningTests(unittest.TestCase):
    @patch("utils.data_cleaning.get_client")
    def test_summarize_data_returns_model_text(self, mock_get_client):
        class FakeModels:
            def __init__(self):
                self.last_call = None

            def generate_content(self, **kwargs):
                self.last_call = kwargs
                return type("Response", (), {"text": "Summary ready"})()

        class FakeClient:
            def __init__(self):
                self.models = FakeModels()

        mock_client = FakeClient()
        mock_get_client.return_value = mock_client

        context = {
            "analysis": {
                "rows": 10,
                "columns": 3,
                "missing": 1,
                "duplicates": 0,
            },
            "column_info": [{"column_name": "age"}],
        }

        result = summarize_data(context)

        self.assertEqual(result, "Summary ready")
        self.assertEqual(mock_client.models.last_call["model"], "gemini-2.5-flash")


if __name__ == "__main__":
    unittest.main()
