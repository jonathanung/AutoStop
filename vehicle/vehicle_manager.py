import carla
import random
from vehicle.vehicle_entity_manager import VehicleEntityManager

class VehicleManager:
    """
    Manages vehicle operations in the CARLA simulator.

    The VehicleManager class is responsible for managing vehicle lifecycle operations such as spawning, retrieving,
    and destroying vehicles in the CARLA simulator environment. It interacts with the CARLA client to spawn vehicles
    at designated spawn points, keep track of vehicles, and ensure proper cleanup of resources.

    Attributes:
        client (carla.Client): The CARLA client for connecting to the simulator.
        world (carla.World): The world object representing the simulator's environment.
        vehicles (list): A list to keep track of spawned vehicle entities.
        blueprint_library (carla.BlueprintLibrary): The library of vehicle blueprints available in the simulator.
        spawn_points (list): A list of spawn points suitable for vehicle spawning.
    """
    def __init__(self, client: carla.Client):
        self.client = client
        self.world = self.client.get_world()
        self.vehicles = []
        self.blueprint_library = self.world.get_blueprint_library()
        self.spawn_points = self.world.get_map().get_spawn_points()

    def spawn_vehicle(self, vehicle_bp: str, index: int):
        """

        Spawns a vehicle in the simulation world using the blueprint provided and an index for the blueprint library.

        The method attempts to spawn a vehicle at a designated spawn point,
        selected randomly from available spawn points, for a maximum number
        of attempts. Upon successfully spawning the vehicle, it adds the vehicle
        to the vehicle entity manager and returns the manager instance.

        Args:
            vehicle_bp (str): A string representing the vehicle blueprint to filter from the blueprint library.
            index (int): An integer index used to select a specific blueprint from the filtered results.

        Returns:
            VehicleEntityManager: The manager instance for the newly spawned vehicle. This contains the vehicle entity and its blueprint.

        Raises:
            Exception: If the vehicle could not be spawned after the maximum number of attempts.
        """
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
        vehicle_entity_manager = VehicleEntityManager(vehicle, vehicle_bp)
        self.vehicles.append(vehicle_entity_manager)
        return vehicle_entity_manager 

    def get_vehicle_by_index(self, index: int):
        """

        Retrieves a vehicle from the list of vehicles by its index.

        Args:
            index (int): The index of the vehicle to retrieve.

        Returns:
            Vehicle: The vehicle at the specified index.

        """
        return self.vehicles[index]

    def get_vehicles(self):
        """
        Gets the list of vehicles owned by the vehicle manager.

        Returns:
            list: A list containing the entity managers within the vehicle manager.
        """
        return self.vehicles

    def destroy_vehicle_by_index(self, index: int):
        """
        Destroys a vehicle from the list at the specified index.

        This method retrieves the vehicle at the given index, performs cleanup
        operations on the vehicle, and removes it from the list of vehicles.

        Args:
            index (int): The index of the vehicle to be destroyed.
        """
        vehicle = self.vehicles[index]
        vehicle.cleanup()
        self.vehicles.pop(index)

    def destroy_vehicle(self, vehicle: VehicleEntityManager):
        """
        Destroys a vehicle by performing cleanup and removing it from the list of vehicles.

        Args:
            vehicle (VehicleEntityManager): The vehicle to be destroyed.
        """
        vehicle.cleanup()
        self.vehicles.remove(vehicle)

    def destroy_all_vehicles(self):
        """
        Destroys all vehicles managed by the instance.

        This method iterates through the `vehicles` list, calls the `cleanup` method on each vehicle to handle any necessary
        cleanup operations, and then clears the list.

        Raises:
            No specific exceptions are raised by this method.
        """
        for vehicle in self.vehicles:
            vehicle.cleanup()
        self.vehicles = []

    def cleanup(self):
        """
        Clean up the simulation environment by destroying all vehicles and clearing client and world references.

        Destroys all the vehicles present in the simulation environment, and subsequently sets the
        client and world attributes to None to ensure no residual connections are maintained.

        Returns:
            None
        """
        self.destroy_all_vehicles()
        self.client = None
        self.world = None
