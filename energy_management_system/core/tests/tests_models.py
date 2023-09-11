from django.test import TestCase

from core.models import Storage, StorageTypes
from core.exceptions import StorageCapacityReachedException, StorageNotEnoughEnergyException


class StorageModelTests(TestCase):
    """
    Returns the correct current battery state in %
    """
    def test_storage_current_percentage(self):
        storage = Storage(
            name="TestS", 
            type=StorageTypes.BATTERY,
            max_capacity = 500,
            current_level = 100
        )

        self.assertEqual(storage.current_percentage(), 20)

    def test_store_energy(self):
        """
        Adds 100 units of energy to a specific storage
        """
        storage = Storage(
            name="TestS", 
            type=StorageTypes.BATTERY,
            max_capacity = 500,
            current_level = 100
        )
        storage.store_energy(100)
        self.assertEqual(storage.current_level, 200)

    def test_store_energy_too_much(self):
        """
        Tries to store too much energy in a storage (expected raised exception)
        """
        storage = Storage(
            name="TestS", 
            type=StorageTypes.BATTERY,
            max_capacity = 500,
            current_level = 450
        )
        
        with self.assertRaises(StorageCapacityReachedException):
            storage.store_energy(100)

    def test_retrieve_energy(self):
        """
        Retrieves 100 units of energy from a specific storage
        """
        storage = Storage(
            name="TestS", 
            type=StorageTypes.BATTERY,
            max_capacity = 500,
            current_level = 100
        )
        storage.retrieve_energy(100)
        self.assertEqual(storage.current_level, 0)

    def test_retrieve_energy_too_much(self):
        """
        Tries to retrieve more than available energy from a storage (expected raised exception)
        """
        storage = Storage(
            name="TestS", 
            type=StorageTypes.BATTERY,
            max_capacity = 500,
            current_level = 100
        )
        
        with self.assertRaises(StorageNotEnoughEnergyException):
            storage.retrieve_energy(150)