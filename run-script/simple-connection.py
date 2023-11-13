from controller.sensorManager import SensorManager


if __name__ == '__main__':
    sensor_manager = SensorManager("00:1A:7D:DA:71:13", print)
    sensor_manager.start()