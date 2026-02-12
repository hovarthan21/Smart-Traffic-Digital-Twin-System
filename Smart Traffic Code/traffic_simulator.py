import random
import pandas as pd
import time

class TrafficDigitalTwin:

    def __init__(self):
        self.roads = {
            "North": 0,
            "South": 0,
            "East": 0,
            "West": 0
        }
        self.signal_state = "North"
        self.waiting_time = {
            "North": 0,
            "South": 0,
            "East": 0,
            "West": 0
        }

    def generate_traffic(self):
        # Simulate vehicle arrival
        for road in self.roads:
            self.roads[road] += random.randint(5, 25)

    def update_signal(self):
        # Give green to highest traffic road
        self.signal_state = max(self.roads, key=self.roads.get)

        # Reduce vehicles on green road
        self.roads[self.signal_state] = max(
            0, self.roads[self.signal_state] - random.randint(20, 40)
        )

    def update_waiting_time(self):
        for road in self.roads:
            if road != self.signal_state:
                self.waiting_time[road] += 5
            else:
                self.waiting_time[road] = 0

    def congestion_index(self):
        total = sum(self.roads.values())
        if total > 200:
            return "High"
        elif total > 100:
            return "Medium"
        else:
            return "Low"

    def step(self):
        self.generate_traffic()
        self.update_signal()
        self.update_waiting_time()

        data = {
            "Vehicles": self.roads,
            "Signal": self.signal_state,
            "WaitingTime": self.waiting_time,
            "Congestion": self.congestion_index()
        }

        return data
