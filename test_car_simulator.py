import pytest
from car_simulator import Car, turn_left, turn_right, move_forward, update_car_status, run_simulation

# 1. Testing the Car Class Initialization 
def test_car_initialization():
    car = Car("TestCar", 0, 0, "N", "FFRFL")
    assert car.name == "TestCar"
    assert car.x == 0
    assert car.y == 0
    assert car.direction == "N"
    assert car.commands == "FFRFL"
    assert str(car) == "- TestCar, (0,0), N"

# 2. Testing Direction Changes (turn_left)
@pytest.mark.parametrize("current_direction, expected_direction", [
    ("N", "W"),
    ("E", "N"),
    ("S", "E"),
    ("W", "S"),
])
def test_turn_left(current_direction, expected_direction):
    assert turn_left(current_direction) == expected_direction

# 3. Testing Direction Changes (turn_right)
@pytest.mark.parametrize("current_direction, expected_direction", [
    ("N", "E"),
    ("E", "S"),
    ("S", "W"),
    ("W", "N"),
])
def test_turn_right(current_direction, expected_direction):
    assert turn_right(current_direction) == expected_direction

# 4. Testing Movement (move_forward)
@pytest.mark.parametrize("x, y, direction, expected_position", [
    (0, 0, "N", (0, 1)),
    (1, 1, "E", (2, 1)),
    (2, 2, "S", (2, 1)),
    (3, 3, "W", (2, 3)),
])
def test_move_forward(x, y, direction, expected_position):
    assert move_forward(x, y, direction) == expected_position

# 5. Testing Collision and Status Update
def test_update_car_status():
    car1 = Car("Car1", 1, 1, "N", "")
    update_car_status(car1, "Car2", 1, 1, 1)
    assert car1.status == "- Car1, collides with Car2 at (1,1) at step 1"

# 6. Testing the Simulation Logic
def test_run_simulation_single_car():
    cars = [Car("Car1", 0, 0, "N", "F")]
    run_simulation(cars, 2, 2)
    assert cars[0].x == 0 and cars[0].y == 1

def test_run_simulation_multiple_cars_collision():
    cars = [Car("Car1", 1, 2, "N", "FFRFFFFRRL"), Car("Car2", 7, 8, "W", "FFLFFFFFFF")]
    run_simulation(cars, 10, 10)
    for car in cars:
        print(f"{car.name} Position: ({car.x}, {car.y}), Status: {car.status}")
    assert cars[0].status is not None, "Car1 did not update its status; no collision detected."
    assert cars[1].status is not None, "Car2 did not update its status; no collision detected."

def test_run_simulation_car_moves_out_of_bounds():
    car = Car("CarA", 0, 2, "N", "F")
    cars = [car]
    run_simulation(cars, 2, 2)
    assert car.status == "- CarA, goes out of bounds at step 1"

