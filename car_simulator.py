# BY: Nikit Swaraj

# Initializing  the Car object with its name, position (x, y), direction, commands, and status for collision or out of bounds.

class Car:
    def __init__(self, name, x, y, direction, commands):     
        self.name = name
        self.x = x
        self.y = y
        self.direction = direction
        self.commands = commands
        self.status = None

    #If the car has a status (like a collision or out of bounds), it will returns that status. Otherwise, it returns the car's name, position, and direction.
    def __str__(self):
        if self.status:
            return self.status
        return f"- {self.name}, ({self.x},{self.y}), {self.direction}"

# Lists of allowed directions and commands
allowed_directions = ["N", "E", "S", "W"]
allowed_commands = ["F", "R", "L"]

# Returns the new direction after turning left.
def turn_left(direction):
    return allowed_directions[(allowed_directions.index(direction) - 1) % 4]

# Returns the new direction after turning right.
def turn_right(direction): 
    return allowed_directions[(allowed_directions.index(direction) + 1) % 4]

# Returns the new position (x, y) of a car after moving forward one unit in its current facing direction.
def move_forward(x_cordinate, y_cordinate, direction):
    if direction == "N":
        return x_cordinate, y_cordinate + 1
    elif direction == "E":
        return x_cordinate + 1, y_cordinate
    elif direction == "S":
        return x_cordinate, y_cordinate - 1
    elif direction == "W":
        return x_cordinate - 1, y_cordinate
    
# Updates the status of a car to by provding whether it has collided with another car at a specific position and step in the simulation.
def update_car_status(car, other_car_name, x, y, step):
    car.status = f"- {car.name}, collides with {other_car_name} at ({x},{y}) at step {step}"


# Simulates the movement of cars on a grid, checking for collisions and out-of-bounds movements.
# Updates the position of cars as they execute their commands and handles collisions and bounds checking.
# Returns  the final states of all cars after the simulation.
def run_simulation(cars, width, height):
    # Initialize an empty dictionary to track the final positions of cars across steps.
    positions = {}
    try:

        # Check the maximum number of commands among all cars to define the total number of steps in the simulation.
        for step in range(max(len(car.commands) for car in cars)):
            # Initialize an empty dictionary to track positions of cars within the current step, for collision detection.
            step_positions = {}
            # Iterate over each car to process its command for the current step.
            for car in cars:
                # Skip processing for cars that have either completed all their commands or have an incident.
                if car.status or step >= len(car.commands):
                    continue
                # Retrieve the command for the current step.
                command = car.commands[step]
                # Skip processing if the command is not recognized (not in allowed_commands).
                if command not in allowed_commands:
                    continue

                if command == "L":
                    car.direction = turn_left(car.direction)
                
                elif command == "R":
                    car.direction = turn_right(car.direction)
                
                elif command == "F":
                    new_x, new_y = move_forward(car.x, car.y, car.direction)
                    # Check if the new position is within the grid boundaries.
                    if 0 <= new_x < width and 0 <= new_y < height:
                        # Check if another car has already moved to or is planning to move to the same position in this step.
                        if (new_x, new_y) in step_positions:
                            # Collision detected, update the status of both cars involved.
                            collided_with = step_positions[(new_x, new_y)]
                            update_car_status(car, collided_with, new_x, new_y, step + 1)
                            for other_car in cars:
                                if other_car.name == collided_with:
                                    update_car_status(other_car, car.name, new_x, new_y, step + 1)
                                    break
                        # No collision, and the position is not previously occupied, record the car's new position.
                        elif (new_x, new_y) not in positions:
                            step_positions[(new_x, new_y)] = car.name
                            car.x, car.y = new_x, new_y
                        # Skip if the position was already occupied in a previous step (handled by the logic in positions dictionary).
                        else:
                            continue
                    # Handle the car going out of bounds by updating its status.
                    else:
                        car.status = f"- {car.name}, goes out of bounds at step {step + 1}"
            # Update the cumulative positions with the positions from this step.
            positions.update(step_positions)
    except Exception as e:
        print(f"Error during simulation: {e}")
    # Return a string representation of the final states of all cars, including any incidents that occurred.
    return "\n".join(str(car) for car in cars)


# Entry point for the simulation. It provides interaction of simulation environment,
def main():
    print("Welcome to Auto Driving Car Simulation!")
    try:
        width, height = map(int, input("Please enter the width and height of simulation field in x y format:\n").split())
        if width <= 0 or height <= 0:
            raise ValueError("Width and height must be positive integers.")
    except ValueError as ve:
        print(f"Invalid input for field dimensions: {ve}")
        return
    print(f"\nYou have created a field of {width} x {height}.")
    cars = []

    while True:
        print("Please choose from the following options:\n[1] Add a car to field\n[2] Run simulation")
        choice = input()
        if choice == "1":
            try:
                name = input("\nPlease enter the name of the car:\n")
                x, y, direction = input(f"\nPlease enter initial position of Car {name} in \"x y direction\" format\n").split()
                x, y = int(x), int(y)
                if (0 <= x <=width and 0 <= y <= height) and direction in allowed_directions:
                    commands = input(f"Please enter the commands for car {name}:\n")
                    if set(commands).issubset(allowed_commands):
                        car = Car(name, x, y, direction, commands)
                        cars.append(car)
                        print("Your current list of cars are:\n")
                        for car in cars:
                            print(f"{car}, {car.commands}")
                    else:
                        print("Please provide the allowed commands \"F\" \"R\" \"L\" ")
                else:
                    print("Please provide the appropriate co-ordinates within the range and direction between N E S W")
            except ValueError as ve:
                print(f"Error adding car: {ve}")
                continue

        elif choice == "2":
             if len(cars) == 0:
                print("There is no car added pls add the car")
             else:
                print("\nYour current list of cars are:")
                for car in cars:
                    print(f"{car}, {car.commands}")
                print("After simulation, the result is:")
                print(run_simulation(cars, width, height))
                print("Please choose from the following options:\n[1] start over\n[2] exit")
                post_choice = input()
                if post_choice == "1":
                    cars = []  # Clear the list of cars to start over
                    continue
                elif post_choice == "2":
                    break
# Checks if the script is being run directly and if so, calls the main function to start the simulation.
if __name__ == "__main__":
    main()
