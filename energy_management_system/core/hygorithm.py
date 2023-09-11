from core.models import Consumer


def hygorithm(
        produced: int, 
        consumed: int, 
        current_storage: int, 
        maximum_storage: int
    ) -> (int, int):
    """
    Given:
        - the amount of produced energy, 
        - the amount of the consumed energy,
        - the amount of energy available in storage and 
        - the maximum amount of energy that can be stored,
    returns:
        - the amount of energy to be stored or retieved in/from a storage and 
        - the amount of energy to be fetched/delivered from/to the Grid.

    Examples:
        Input -> Producing: 100, Consuming: 150, Storage: 0
        Returns -> Grid: 10, Storage: 0

        Input -> Producing: 100, Consuming: 80, Storage: 0
        Returns -> Grid: 0, Storage: -20 (meaning 20 is saved in Storage)

        Input -> Producing: 100, Consuming 150, Storage: 100
        Returns -> Grid: 0, Storage: 50 (meaning 50 is retrieved from Storage)

        Input -> Producing: 100, Consuming 50, Storage: 200 (max)
        Returns -> Grid: -50 (delivered to Grid), Storage: 0 (because storage is already full)
    """
    delta = consumed - produced     # if > 0 => "too much", if > 0 => "too little"

    if delta > 0:
        print('too little was produced')
        storage = delta if delta < current_storage else current_storage
        grid = delta if current_storage == 0 else delta - current_storage
        return grid, storage

    elif delta == 0:
        return 0, 0
    
    else:
        print('too much was produced')
        free_storage = maximum_storage - current_storage  # how much more energy can be stored
        grid = 0 if abs(delta) < free_storage else free_storage - abs(delta)
        storage = -free_storage if abs(delta) > free_storage else delta
        return grid, storage

    