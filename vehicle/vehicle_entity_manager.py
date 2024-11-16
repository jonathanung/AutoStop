import carla

LIDAR_BP = 'sensor.lidar.ray_cast'
RADAR_BP = 'sensor.radar.ray_cast'
COLLISION_BP = 'sensor.other.collision'
CAMERA_BP = 'sensor.camera.rgb'

"""
This class manages the entities of a vehicle and the vehicle itself.
"""
class VehicleEntityManager:
    """
    Initializes the VehicleEntityManager class.
    """
    def __init__(self, vehicle: carla.Vehicle):
        self.vehicle = vehicle
        self.lidars = []
        self.radars = []
        self.cameras = []
        self.collision_sensors = []
    
    def cleanup(self):
        #TODO: Write cleanup logic
        pass
    
    def add_lidar(self, lidar: carla.Lidar):
        #TODO: Write add lidar logic
        pass
    
    def add_radar(self, radar: carla.Radar):
        #TODO: Write add radar logic
        pass
    
    def add_camera(self, camera: carla.Camera):
        #TODO: Write add camera logic
        pass

    def add_collision_sensor(self, collision_sensor: carla.CollisionSensor):
        #TODO: Write add collision sensor logic
        pass
