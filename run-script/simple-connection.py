from controller.bt.sensorManager import SensorManager


if __name__ == '__main__':
    sensor_manager = SensorManager("90:0F:0C:35:C6:B2", print)
    sensor_manager.start()
    print("Sensor manager started")