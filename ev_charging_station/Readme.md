# PROJECT: EV Charging Station

## Installation/Execution:
You can install the app on your local machine, using a Virtual Environment.


**Requirements:** Python 3

1 - Clone the git repository to your local machine

2 - Set-up a virtual environment for the project and make sure it is active

3 - From `ev_charging_station` folder run:
`pip install -r requirements.txt`

4 - Run `python app.py` (default port: 8000).

5 - Access the printed url from a browser to make sure it is working.


## Architecture
A reservation is composed by a set of TimeSlots, a Car Lot, an User and some
characteristics of a car, such as the battery capacity and the maximum charge rate.

The Reservations can be managed by users through a Flask API.

![Screenshot](/ev_charging_station/docs/EV_charging.drawio.png)


## API usage

The endpoint `/users/<int:user_id>/reservations` supports GET and POST requests, respectively for getting all the reservations of a user and to create a new reservation for the user identified by *user_id*.

While GET does not require data to be submitted (besides *user_id*). the POST method requires the following payload:

```
{      
    'capacity_kwh': int,
    'max_charge_rate_kw': int,
    'charging_efficiency': float,
    'day_of_week': int,
    'starting_hour': int,
    'desired_charge': float
}
```

Other methods such as DELETE can be added in future. 
