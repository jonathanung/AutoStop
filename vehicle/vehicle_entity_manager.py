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
    
    """
    This method cleans up the vehicle entity manager.
    """
    def cleanup(self):
        for lidar in self.lidars:
            lidar.destroy()
        for radar in self.radars:
            radar.destroy()
        for camera in self.cameras:
            camera.destroy()
        for collision_sensor in self.collision_sensors:
            collision_sensor.destroy()
        self.vehicle.destroy()

    """
    This method adds a lidar to the vehicle entity manager.
    """
    def add_lidar(self, lidar_transform: carla.Transform):
        #TODO: Write add lidar logic
        pass
    
    """
    This method adds a radar to the vehicle entity manager.
    """
    def add_radar(self, radar_transform: carla.Transform):
        #TODO: Write add radar logic
        pass
    
    """
    This method adds a camera to the vehicle entity manager.
    """
    def add_camera(self, camera_transform: carla.Transform):
        #TODO: Write add camera logic
        pass
    
    """
    This method adds a collision sensor to the vehicle entity manager.
    """
    def add_collision_sensor(self, collision_sensor_transform: carla.Transform):
        #TODO: Write add collision sensor logic
        pass
