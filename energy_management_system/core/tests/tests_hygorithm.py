from django.test import TestCase

from core.hygorithm import hygorithm


class TestHygorithm(TestCase):
    def test_deliver_to_grid(self):
        "Should happen when Storage is full and too much is produced"
        self.assertEqual(
            hygorithm(
                produced=200, 
                consumed=150, 
                current_storage=200, 
                maximum_storage=200
            ),
            (-50, 0) # Expected result (grid, storage)
        )

    def test_store_in_storage(self):
        "Should happen when Storage has space and too much is produced"
        self.assertEqual(
            hygorithm(
                produced=200,
                consumed=150,
                current_storage=100,
                maximum_storage=200
            ),
            (0, -50)  # Expected result (grid, storage)
        )

    def test_deliver_to_storage_and_to_grid(self):
        """ Should happen when Storage has SOME space but too much is produced """
        self.assertEqual(
            hygorithm(
                produced=200,
                consumed=150,
                current_storage=190,
                maximum_storage=200
            ),
            (-40, -10)  # Expected result (grid, storage)
        )

    def test_get_from_grid(self):
        """ Should happen when Storage is empty and too little is produced """
        self.assertEqual(
            hygorithm(
                produced=200,
                consumed=250,
                current_storage=0,
                maximum_storage=200
            ),
            (50, 0)  # Expected result (grid, storage)
        )

    def test_get_from_storage(self):
        """ Should happen when Storage has enough energy to cover the requirements """
        self.assertEqual(
            hygorithm(
                produced=200,
                consumed=250,
                current_storage=50,
                maximum_storage=200
            ),
            (0, 50)  # Expected result (grid, storage)
        )

    def test_get_from_storage_and_from_grid(self):
        """ Should happen when Storage has SOME energy but the requirements are too large """
        self.assertEqual(
            hygorithm(
                produced=200,
                consumed=250,
                current_storage=20,
                maximum_storage=200
            ),
            (30, 20)  # Expected result (grid, storage)
        )