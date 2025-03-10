class TrafficSignal:
    def __init__(self, segments, config={}):
        # Initialize segments
        self.segments = segments
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)
        # Calculate properties
        self.init_properties()

    def set_default_config(self):
        self.cycle = [(False, True,60), (False,False,66), (True, False,126), (False, False, 132)]
        self.slow_distance = 40
        self.slow_factor = 10
        self.stop_distance = 15


        self.current_cycle_index = 0
        self.last_t = 0
    

    def init_properties(self):
        for i in range(len(self.segments)):
            for segment in self.segments[i]:
                segment.set_traffic_signal(self, i)

    @property
    def current_cycle(self):
        return self.cycle[self.current_cycle_index]

    def update(self, sim):
        # Check for vehicles in the stopping zone
        east_west_vehicles = any(self.is_vehicle_in_stopping_zone(segment, sim) for segment in self.segments[0])
        north_south_vehicles = any(self.is_vehicle_in_stopping_zone(segment, sim) for segment in self.segments[1])

        if east_west_vehicles and not north_south_vehicles:
            # Prioritize East and West segments
            self.current_cycle_index = 2  # Assuming index 2 is the cycle for East-West green light
        elif north_south_vehicles and not east_west_vehicles:
            # Prioritize North and South segments
            self.current_cycle_index = 0  # Assuming index 0 is the cycle for North-South green light
        elif east_west_vehicles and north_south_vehicles:
            # If both directions have vehicles, follow the default cycle
            k = int(sim.t) % self.cycle[-1][2]
            for i in range(len(self.cycle)):
                if k < self.cycle[i][2]:
                    self.current_cycle_index = i
                    break
        else:
            # If no vehicles are present, follow the default cycle
            k = int(sim.t) % self.cycle[-1][2]
            for i in range(len(self.cycle)):
                if k < self.cycle[i][2]:
                    self.current_cycle_index = i
                    break

    def is_vehicle_in_stopping_zone(self, segment, sim):
        # Check if there are any vehicles within the slowing distance of the traffic signal
        for vehicle in segment.vehicles:
            if segment.get_length() - self.slow_distance <= sim.vehicles[vehicle].x <= segment.get_length():
                return True
        return False