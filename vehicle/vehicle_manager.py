import carla
import random
from vehicle.vehicle_entity_manager import VehicleEntityManager

"""
This class is used to manage vehicles in the CARLA simulator.
"""
class VehicleManager:
    """
    This method initializes the VehicleManager class.
    """
    def __init__(self, client: carla.Client):
        self.client = client
        self.world = self.client.get_world()
        self.vehicles = []
        self.blueprint_library = self.world.get_blueprint_library()
        self.spawn_points = self.world.get_map().get_spawn_points()

    """
    This method spawns a vehicle in the CARLA simulator.
    """
    def spawn_vehicle(self, vehicle_bp: str, index: int):
        vehicle_bp = self.blueprint_library.filter(vehicle_bp)[index]
        spawn_point = random.choice(self.spawn_points)
        vehicle = None
        max_spawn_attempts = 10
        # This loop tries to spawn a vehicle at the given spawn point. If it fails, it tries again at a random spawn point.
        for _ in range(max_spawn_attempts):
            try:
                vehicle = self.world.spawn_actor(vehicle_bp, spawn_point)
                print(f"Vehicle spawned at: {spawn_point.location}")
                break
            except RuntimeError:
                spawn_point = random.choice(self.spawn_points)
                continue
        if vehicle is None:
            print(f"Failed to spawn a vehicle after {max_spawn_attempts} attempts")
            raise Exception("Failed to spawn a vehicle")
        vehicle_entity_manager = VehicleEntityManager(vehicle)
        self.vehicles.append(vehicle_entity_manager)
        return vehicle_entity_manager 

    """
    This method returns the vehicle.
    """
    def get_vehicle_by_index(self, index: int):
        return self.vehicles[index]

    """
    This method returns all vehicles.
    """
    def get_vehicles(self):
        return self.vehicles
    
    """
    This method destroys a vehicle in the CARLA simulator.
    """
    def destroy_vehicle_by_index(self, index: int):
        vehicle = self.vehicles[index]
        vehicle.cleanup()
        self.vehicles.pop(index)

    """
    This method destroys a vehicle in the CARLA simulator.
    """
    def destroy_vehicle(self, vehicle: VehicleEntityManager):
        vehicle.cleanup()
        self.vehicles.remove(vehicle)

    """
    This method destroys all vehicles in the CARLA simulator.
    """
    def destroy_all_vehicles(self):
        for vehicle in self.vehicles:
            vehicle.cleanup()
        self.vehicles = []

    def cleanup(self):
        self.destroy_all_vehicles()
        self.client = None
        self.world = None
