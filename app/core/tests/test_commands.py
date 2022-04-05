from unittest.mock import patch
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase
# mock behaviour of django's get_db() function


class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """Test waiting for DB when DB is available"""
        # management command will try to retrieve DB connection, so we need to mock that get_connection() call
        # this is the function called when Django tries to get DB connection
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # we override behaviour of function by having it simply return True
            gi.return_value = True
            call_command('wait_for_db')

            self.assertEqual(gi.call_count, 1)

    # decorator works similar way to "with patch('django.db.utils.ConnectionHandler.__getitem__') as gi"
    # it will override behaviour of function and pass mock function as argument to the function
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for DB"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')

            self.assertEqual(gi.call_count, 6)
