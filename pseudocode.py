import numpy as np
import random

class Truck:
    def __init__(self, id, location):
        self.id = id
        self.location = location
        self.available = True
        self.destination = None
        self.arrival_time = 0

class Load:
    def __init__(self, origin, destination, revenue, timestamp):
        self.origin = origin
        self.destination = destination
        self.revenue = revenue
        self.timestamp = timestamp

class DispatchEnvironment:
    def __init__(self, num_trucks, locations):
        self.trucks = [Truck(i, random.choice(locations)) for i in range(num_trucks)]
        self.time = 0
        self.locations = locations

    def step(self, load, action):
        reward = 0

        if action[0] == 'accept':
            truck = self.trucks[action[1]]
            travel_cost = self.calculate_cost(truck.location, load.origin) + self.calculate_cost(load.origin, load.destination)
            reward = load.revenue - travel_cost

            truck.available = False
            truck.destination = load.destination
            truck.arrival_time = self.time + self.calculate_travel_time(truck.location, load.destination)

        # Move time forward
        self.time += 1
        self.update_trucks()

        return reward

    def update_trucks(self):
        for truck in self.trucks:
            if not truck.available and self.time >= truck.arrival_time:
                truck.available = True
                truck.location = truck.destination
                truck.destination = None

    def calculate_cost(self, start, end):
        # Simple Euclidean distance for cost
        return np.linalg.norm(np.array(start) - np.array(end))

    def calculate_travel_time(self, start, end):
        # Travel time proportional to distance
        return int(self.calculate_cost(start, end))

    def get_available_trucks(self):
        return [truck for truck in self.trucks if truck.available]

class SequentialDispatcher:
    def __init__(self, environment):
        self.env = environment

    def policy(self, load):
        available_trucks = self.env.get_available_trucks()
        if not available_trucks:
            return ('reject', None)

        # Example policy: Assign nearest truck
        distances = [self.env.calculate_cost(truck.location, load.origin) for truck in available_trucks]
        nearest_truck = available_trucks[np.argmin(distances)]

        # Simple acceptance logic: revenue should outweigh costs
        total_cost = distances[np.argmin(distances)] + self.env.calculate_cost(load.origin, load.destination)
        if load.revenue > total_cost:
            return ('accept', nearest_truck.id)
        else:
            return ('reject', None)

# Example simulation
if __name__ == "__main__":
    locations = [(0,0), (5,5), (10,10), (15,15), (20,20)]
    env = DispatchEnvironment(num_trucks=3, locations=locations)
    dispatcher = SequentialDispatcher(env)

    # Simulate incoming loads
    loads = [
        Load(origin=(2,2), destination=(8,8), revenue=100, timestamp=1),
        Load(origin=(12,12), destination=(18,18), revenue=150, timestamp=2),
        Load(origin=(1,1), destination=(15,15), revenue=120, timestamp=3),
    ]

    total_reward = 0
    for load in loads:
        action = dispatcher.policy(load)
        reward = env.step(load, action)
        total_reward += reward
        print(f"Load {load.origin}->{load.destination}, Action: {action}, Reward: {reward}")

    print(f"Total Reward: {total_reward}")
