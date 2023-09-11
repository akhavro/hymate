from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
import pandas as pd

from core.models import Consumer
from core.hygorithm import hygorithm


class Command(BaseCommand):
    help = "Runs the logic against a dummy file and generates an output file with energy distribution details. \
        The file must be a .csv file (comma separated), be named in.csv and be located in the main folder \
        alongside manage.py. The required columns must be labeled as (timestamp, pv_yield_power, household_consumption). \
        The output file will be named out.csv"

    def add_arguments(self, parser):
        parser.add_argument("consumer", type=int, help="ID of the Consumer which to run the simulation against")

    def handle(self, *args, **options):
        try:
            consumer = Consumer.objects.get(id=options.get('consumer'))
        except ObjectDoesNotExist as e:
            raise CommandError(f"{e} Consumer with id={options.get('consumer')} does not exist!")
        
        # Read the file
        df_input = pd.read_csv('in.csv')
        grid_lst = []
        storage_lst = []
        storage_level_lst = []
    
        # Iterate over each line calling the algorithm and saving the results
        for i, row in df_input.iterrows():
            current_storage = consumer.storages.aggregate(current=Sum('current_level')).get('current')
            maximum_storage = consumer.storages.aggregate(max=Sum('max_capacity')).get('max')

            storage_level_lst.append(current_storage)

            grid, storage = hygorithm(
                produced=row.get('pv_yield_power'),
                consumed=row.get('household_consumption'),
                current_storage=current_storage,
                maximum_storage=maximum_storage
            )

            # Update storage values
            if storage < 0:
                consumer.storages.first().store_energy(abs(storage))  
            else:
                consumer.storages.first().retrieve_energy(storage)

            grid_lst.append(grid)
            storage_lst.append(storage)

        df_input['grid'] = grid_lst
        df_input['storage'] = storage_lst
        df_input['storage_current_level'] = storage_level_lst
        df_input.to_csv('out.csv')

        print('Done')
        