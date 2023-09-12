user_reservations = {}


def get_available_parking_lot(
        day_of_week: int, 
        starting_hour: int,
        amount_of_slots: int
        ) -> dict:
    '''
    Returns a parking lot that is available for reservation. 
    Raises exception if there's no parking lots available.
    '''
    return {"status": "NOT_IMPLEMENTED"}

def make_reservation(
        user_id: int,
        capacity_kwh: int, 
        max_charge_rate_kw: int, 
        charging_efficiency: float, 
        day_of_week: int,
        starting_hour: int, 
        desired_charge: int
        ) -> dict:
    global user_reservations

    # Calculate the amount of slots of 15 min needed to charge to desired level
    amount_of_slots = int(capacity_kwh / (max_charge_rate_kw * charging_efficiency) * 60 / 15)
    # cost = calculate_cost() ...
    parking_lot = get_available_parking_lot(day_of_week, starting_hour, amount_of_slots)

    reservation = {
        'starting_hour': starting_hour,
        'desired_charge': desired_charge,
        'day_of_week': day_of_week,
        'amount_of_slots': amount_of_slots,
        'cost': amount_of_slots * 1,  # dummy_cost = 1 per slot,
        'parking_lot': parking_lot
    }

    if not user_id in user_reservations.keys():
        user_reservations[user_id] = []     # If user's 1-st reservation ever

    user_reservations[user_id].append(reservation)
    return reservation



def retrieve_user_reservations(user_id: id):
    global user_reservations
    return user_reservations.get(user_id) if user_id in user_reservations.keys() else []