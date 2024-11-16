# Autostop

This project is a simulation of a self-driving car in the CARLA simulator. It is a simple implementation of a self-driving car that can navigate a course without hitting any obstacles.

Read more about CARLA [here](https://carla.org/).

Install CARLA following the instructions [here](https://carla.readthedocs.io/en/latest/start_quickstart/).

## Setup
0. Run the CARLA server and set environment variables:
    In your .env file,
    ```
    SERVER_HOST=<CARLA server host>
    SERVER_PORT=<CARLA server port>
    MAP_NAME=<CARLA map name>
    VEHICLE_BP=<CARLA vehicle blueprint name>
    VEHICLE_INDEX=<CARLA vehicle index>
    ```

    For example,
    ```
    SERVER_HOST=localhost
    SERVER_PORT=2000
    MAP_NAME=Town01
    VEHICLE_BP=vehicle.tesla.model3
    VEHICLE_INDEX=0
    ```

    To run the CARLA server, search the instructions [here](https://carla.readthedocs.io/en/latest/start_quickstart/).

1. Install the necessary dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run the main script:
    ```bash
    python main.py
    ```
