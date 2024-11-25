import sys
import os
import dotenv
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QGridLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer
import queue

import carla
from client.client_manager import ClientManager
from vehicle.vehicle_manager import VehicleManager
from vehicle.vehicle_entity_manager import VehicleEntityManager
from vehicle.vehicle_pid_controller import VehiclePIDController
from gui.main_window import MainWindow

dotenv.load_dotenv()

app = QApplication(sys.argv)
window = MainWindow()
window.show()

client_manager = ClientManager(
    os.getenv('SERVER_HOST') or 'localhost',
    int(os.getenv('SERVER_PORT')) or 2000,
    os.getenv('MAP_NAME') or 'Town01'
)
client_manager.set_weather(carla.WeatherParameters.ClearNoon)
client_instance = client_manager.get_client_instance()
vehicle_manager = client_manager.get_vehicle_manager()
vehicle_entity_manager = vehicle_manager.spawn_vehicle(
    os.getenv('VEHICLE_BP') or 'vehicle.tesla.model3',
    int(os.getenv('VEHICLE_INDEX')) or 0
)

vehicle_entity_manager.add_camera(carla.Transform(carla.Location(x=1.5, z=1.5)), window)
vehicle_entity_manager.add_lidar(carla.Transform(carla.Location(x=1.5, z=1.5)), window)
# vehicle_entity_manager.add_collision_sensor(carla.Transform(carla.Location(x=1.5, z=1.5)))

vehicle_entity_manager.move_to_speed(30)

def respawn_vehicle():
    global vehicle_entity_manager
    window.clear_views()
    vehicle_entity_manager = vehicle_manager.respawn_vehicle_by_index(0)
    vehicle_entity_manager.add_camera(carla.Transform(carla.Location(x=1.5, z=1.5)), window)
    vehicle_entity_manager.add_lidar(carla.Transform(carla.Location(x=1.5, z=1.5)), window)
    vehicle_entity_manager.move_to_speed(30)

window.set_respawn_callback(respawn_vehicle)

app.aboutToQuit.connect(client_manager.cleanup)
sys.exit(app.exec_())
