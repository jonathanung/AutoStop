import carla
import numpy as np
import math
import cv2
from gui.main_window import MainWindow
from vehicle.vehicle_pid_controller import VehiclePIDController

LIDAR_BP = 'sensor.lidar.ray_cast'
RADAR_BP = 'sensor.radar.ray_cast'
COLLISION_BP = 'sensor.other.collision'
CAMERA_BP = 'sensor.camera.rgb'

class VehicleEntityManager:
    """
    Manages vehicle entities in a simulation, including the addition and processing
    of various sensors. This class provides methods to handle the transformation
    and visualization of sensor data, as well as vehicle control functionalities.

    Attributes
    ----------
    vehicle : carla.Vehicle
        The vehicle instance being managed.
    world : carla.World
        The simulation world the vehicle resides in.
    vehicle_bp : str
        The blueprint identifier for the vehicle.
    pid_controller : VehiclePIDController
        The PID controller instance for managing vehicle speed.
    lidars : list
        List of LIDAR sensors attached to the vehicle.
    radars : list
        List of radar sensors attached to the vehicle.
    cameras : list
        List of cameras attached to the vehicle.
    collision_sensors : list
        List of collision sensors attached to the vehicle.
    """
    def __init__(self, vehicle: carla.Vehicle, vehicle_bp: str):
        self.vehicle = vehicle
        self.world = vehicle.get_world()
        self.vehicle_bp = vehicle_bp
        self.pid_controller = VehiclePIDController(Kp=0.1, Ki=0.01, Kd=0.01, dt=0.1)
        self.lidars = []
        self.radars = []
        self.cameras = []
        self.collision_sensors = []

    def cleanup(self):
        """
        Cleans up all sensors and the vehicle by stopping and destroying each sensor,
        then destroying the vehicle instance.

        Raises
        ------
        RuntimeError
            If unable to stop or destroy any of the sensors or the vehicle.
        """
        for lidar in self.lidars:
            lidar.stop()
            lidar.destroy()
        for radar in self.radars:
            radar.stop()
            radar.destroy()
        for camera in self.cameras:
            camera.stop()
            camera.destroy()
        for collision_sensor in self.collision_sensors:
            collision_sensor.stop()
            collision_sensor.destroy()
        self.vehicle.destroy()

    def add_lidar(self, lidar_transform: carla.Transform, window: MainWindow):
        """
        Adds a LIDAR sensor to the vehicle, sets its attributes, and processes the point
        cloud data for visualization in the main window.

        Parameters
        ----------
        lidar_transform : carla.Transform
            The transform to apply to the LIDAR sensor, including its location and rotation.
        window : MainWindow
            The main window instance where the LIDAR view will be added and updated.

        Returns
        -------
        carla.Actor
            The spawned LIDAR actor.

        """
        lidar_bp = self.world.get_blueprint_library().find(LIDAR_BP)
        
        # Set LIDAR parameters
        lidar_bp.set_attribute('range', '50')
        lidar_bp.set_attribute('rotation_frequency', '10')
        lidar_bp.set_attribute('channels', '32')
        lidar_bp.set_attribute('points_per_second', '500000')
        lidar_bp.set_attribute('upper_fov', '15')
        lidar_bp.set_attribute('lower_fov', '-25')
        
        lidar = self.world.spawn_actor(lidar_bp, lidar_transform, attach_to=self.vehicle)
        view_index = window.add_view(f"{self.vehicle_bp} {lidar_bp} {len(self.lidars) + 1}")
        
        def process_lidar(point_cloud):
            """
            Manages vehicle entities in a simulation, including the addition and processing
            of lidar sensors. This class provides methods to handle the transformation
            and visualization of lidar data.
            """
            points = np.frombuffer(point_cloud.raw_data, dtype=np.dtype('f4'))
            points = np.reshape(points, (-1, 4))
            
            # Create visualization image
            image_size = 400
            lidar_img = np.zeros((image_size, image_size, 3), dtype=np.uint8)
            
            # Adjust scale factor for better visibility
            scale_factor = 8
            
            # Center of the image
            cx, cy = image_size // 2, image_size // 2
            
            # Process points
            for point in points:
                x, y, z, intensity = point
                
                # Filter out points
                if -2.0 < z < 3.0:
                    try:
                        # Convert to top-down view
                        px = int(cx + y * scale_factor)
                        py = int(cy - x * scale_factor)
                        
                        if 0 <= px < image_size and 0 <= py < image_size:
                            # Color based on height and intensity
                            h_color = int((z + 2) * 64)
                            i_color = int(intensity * 128)
                            color = (min(255, h_color), 
                                    min(255, i_color), 
                                    min(255, int((x*x + y*y) * 255/2500)))
                            
                            cv2.circle(lidar_img, (px, py), 2, color, -1)
                            
                    except OverflowError:
                        continue
            
            window.update_frame_for_view(view_index, lidar_img)
        
        lidar.listen(process_lidar)
        self.lidars.append(lidar)
        return lidar

    def add_radar(self, radar_transform: carla.Transform):
        #TODO: Write add radar logic
        pass

    def add_camera(self, camera_transform: carla.Transform, window: MainWindow):
        """
        Adds a new camera to the vehicle and sets up a listener to process the incoming
        camera frames.

        Parameters
        ----------
        camera_transform : carla.Transform
            The transform to be applied to the camera when spawning it.
        window : MainWindow
            The main window instance where the camera view will be displayed.

        Returns
        -------
        camera : carla.Actor
            The spawned camera actor.

        """
        camera_bp = self.world.get_blueprint_library().find(CAMERA_BP)
        camera_bp.set_attribute('image_size_x', '800')
        camera_bp.set_attribute('image_size_y', '600')
        camera_bp.set_attribute('fov', '90')
        
        camera = self.world.spawn_actor(camera_bp, camera_transform, attach_to=self.vehicle)
        view_index = window.add_view(f"{self.vehicle_bp} {camera_bp} {len(self.cameras) + 1}")
        
        def process_camera(image):
            array = np.frombuffer(image.raw_data, dtype=np.uint8)
            array = np.reshape(array, (image.height, image.width, 4))
            array = array[:, :, :3]
            window.update_frame_for_view(view_index, array)
        
        camera.listen(process_camera)
        self.cameras.append(camera)
        return camera

    def add_collision_sensor(self, collision_sensor_transform: carla.Transform):
        #TODO: Write add collision sensor logic
        pass

    def move_to_speed(self, speed: float):
        """
        Calculates and applies throttle control to move the vehicle at the desired speed.

        Parameters
        ----------
        speed : float
            The desired speed to which the vehicle should move.

        """
        control = carla.VehicleControl()
        velocity = self.vehicle.get_velocity()
        current_speed = math.sqrt(velocity.x**2 + velocity.y**2 + velocity.z**2)
        control.throttle = self.pid_controller.control(speed, current_speed)
        self.vehicle.apply_control(control)
    
    def brake(self, brake_value: float):
        """
        Controls the braking mechanism of a vehicle in the CARLA simulator.

        Parameters
        ----------
        brake_value : float
            The amount to apply the brake, where 0.0 indicates no braking and 1.0 indicates full braking.
        """
        control = carla.VehicleControl()
        control.brake = brake_value
        self.vehicle.apply_control(control)
