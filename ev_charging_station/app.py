from flask import Flask, jsonify, request


from reservation_manager import make_reservation, retrieve_user_reservations

app = Flask(__name__)


@app.route('/users/<int:user_id>/reservations', methods=['GET'])
def get_reservations(user_id: int):
    """
    Returns a list of reservations made by user with user_id
    """
    return jsonify(retrieve_user_reservations(user_id)), 200


@app.route('/users/<int:user_id>/reservations', methods=['POST'])
def create_reservation(user_id: int):
    """
    Creates a new reservation for the user with user_id
    """
    data = request.get_json(force=True)
    
    reservation = make_reservation(
        user_id,
        data['capacity_kwh'],
        data['max_charge_rate_kw'],
        data['charging_efficiency'],
        data['day_of_week'],
        data['starting_hour'],
        data['desired_charge']
    )

    return jsonify(reservation), 201


app.run(port=8000)