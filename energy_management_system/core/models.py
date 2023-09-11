from django.db import models
from django.db.models import Sum, F
from django.utils.translation import gettext_lazy as _

from core.exceptions import StorageCapacityReachedException, StorageNotEnoughEnergyException


class ProducerTypes(models.TextChoices):
    WIND = "WIND", _("Eolic")
    SUN = "SUN", _("Solar")
    GEOTHERMAL = "GEOTHERMAL", _("Geothermal")
    HYDROGEN = "HYDROGEN", _("Hydrogen")


class StorageTypes(models.TextChoices):
    BATTERY = "BATTERY", _("Battery")


class ConsumerTypes(models.TextChoices):
    HOUSEHOLD = "HOUSEHOLD", _("Household")


class Producer(models.Model):
    name = models.TextField()
    type = models.TextField(choices=ProducerTypes.choices)

    def __str__(self):
        return self.name


class Storage(models.Model):
    name = models.TextField()
    type = models.TextField(choices=StorageTypes.choices)
    max_capacity = models.BigIntegerField(default=0)
    current_level = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name

    def current_percentage(self) -> int:
        """ Returns the current storage state in integer percentage (0-100) """
        return self.current_level / self.max_capacity * 100
    
    def store_energy(self, amount: int) -> None:
        if self.max_capacity < self.current_level + amount:
            raise StorageCapacityReachedException
        self.current_level += amount
        self.save() # can be done in async

    def retrieve_energy(self, amount: int) -> None:
        if self.current_level < amount:
            raise StorageNotEnoughEnergyException
        self.current_level -= amount
        self.save() # can be done in async


class GridAccess(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


class Consumer(models.Model):
    name = models.TextField()
    type = models.TextField(choices=ConsumerTypes.choices)
    producers = models.ManyToManyField(Producer)
    storages = models.ManyToManyField(Storage)
    grid = models.OneToOneField(GridAccess, on_delete=models.CASCADE)

    def __str__(self):
        return self.name 