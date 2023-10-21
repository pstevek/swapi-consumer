import json
import os
import unittest
import requests
from unittest.mock import patch, Mock
from .consumer import PEOPLE_URL


def get_person_data(person_id):
    return requests.get(f"{PEOPLE_URL}{person_id}").json()


class TestSwapiApi(unittest.TestCase):

    @patch('requests.get')
    def test_get_people_data(self, mock_get):
        path = os.path.realpath(__file__)
        fp = os.path.dirname(path)
        with open(fp + "/mock/person.json") as file:

            response_dict = json.load(file)

            mock_response = Mock()
            mock_response.return_value.status_code = 200
            mock_response.json.return_value = response_dict
            mock_get.return_value = mock_response

            person = get_person_data(1)
            mock_get.assert_called_with("https://swapi.dev/api/people/1")

            self.assertEquals(person, response_dict)
