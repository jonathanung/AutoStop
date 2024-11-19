import carla
from client.client_manager import ClientManager
from vehicle.vehicle_manager import VehicleManager
from vehicle.vehicle_entity_manager import VehicleEntityManager
import os
import dotenv

dotenv.load_dotenv()

client_manager = ClientManager(os.getenv('SERVER_HOST') or 'localhost', int(os.getenv('SERVER_PORT')) or 2000, os.getenv('MAP_NAME') or 'Town01')
client_instance = client_manager.get_client_instance()
vehicle_manager = VehicleManager(client_instance)
vehicle = vehicle_manager.spawn_vehicle(os.getenv('VEHICLE_BP') or 'vehicle.tesla.model3', int(os.getenv('VEHICLE_INDEX')) or 0)
client_manager.set_vehicle_manager(vehicle_manager)

