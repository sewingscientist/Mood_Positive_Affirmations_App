'''
The first two tests don't work properly. It appears to be calling get.requests twice which is causing it to fail.
I tried looking into this but couldn't work it out.

I did find HTTPretty for testing APIs but didn't have time to fully read into to be able to add to the code.
'''

import unittest
from unittest.mock import patch
from final_code import PositiveAffirmationsApp


class TestPositiveAffirmationsApp(unittest.TestCase):

    # Test that the requests.get function works
    @patch('requests.get')
    def test_get_positive_affirmation(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = [{'q': 'Test affirmation'}]

        app = PositiveAffirmationsApp()
        affirmation = app.get_positive_affirmation()

        self.assertEqual(affirmation, 'Test affirmation')
        mock_get.assert_called_once()

    # Test that the requests.get returns an error when status is 404
    @patch('requests.get')
    def test_get_positive_affirmation_error(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 404

        app = PositiveAffirmationsApp()
        affirmation = app.get_positive_affirmation()

        self.assertEqual(affirmation, 'Unable to fetch affirmation')
        mock_get.assert_called_once()
        print(mock_get.call_args_list)  # Print the call arguments

    # Test that the affirmation is saved into the My SQL database
    # When running test, it will pop up the app, need to go into affirmations and click 'Save Affirmation'
    def test_save_affirmation(self):
        app = PositiveAffirmationsApp()
        app.current_affirmation = 'Test affirmation'

        with patch.object(app.db_manager, 'insert_into_database') as mock_insert:
            app.save_affirmation()

        mock_insert.assert_called_once_with('fave_affirmation', 'Test affirmation')


if __name__ == '__main__':
    unittest.main()
