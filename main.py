import carla
from client import ClientManager
from manager.vehicle_manager import VehicleManager
import os
import dotenv

dotenv.load_dotenv()

client_manager = ClientManager(os.getenv('SERVER_HOST') or 'localhost', os.getenv('SERVER_PORT') or 2000, os.getenv('MAP_NAME') or 'Town01')
client_instance = client_manager.get_client_instance()
vehicle_manager = VehicleManager(client_instance)
vehicle = vehicle_manager.spawn_vehicle(os.getenv('VEHICLE_BP') or 'vehicle.tesla.model3', os.getenv('VEHICLE_INDEX') or 0)
client_manager.set_vehicle_manager(vehicle_manager)

