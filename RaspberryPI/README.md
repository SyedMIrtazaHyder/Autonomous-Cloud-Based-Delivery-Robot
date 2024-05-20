# Raspberry Pi 3.5B files

## Content

This folder contains all the scripts ran on the Raspberry Pi 3.5B.

- **Road Segmentation**: `detection.py`, `unet.py`, `segmentation_model2.pth`
- **Cloud & Device Communication**: `pi_commv2.py`, `pi_comm.py`
- **Livestream**: `pi_livestream.py`
- **L298 Integration**: `mpu_driver.py`, `motors_driver_logic.ino`
- **Pi to Arduino**: `Raspberry_to_Arduino`

## Summary

### Road Segmentation
Road segmentation is performed using a Unet model, which is trained on the [CityScapes](https://www.kaggle.com/datasets/xiaose/cityscapes) dataset. The model was trained on the [Kaggle Notebook](https://www.kaggle.com/code/muhammadzakria2001/notebook10173fb2b9).

### Cloud & Device Communication
We used Microsoft Azure as our cloud service and Azure IoT Hub for developing the connection between the Raspberry Pi 3.5B and our Azure Webpage.

### Livestream
The USB web camera sent frames to the [Twitch account](https://www.twitch.tv/theguywhoneedstotakeapiss) at 30fps for the livestream. A 20 seconds delay was observed.

### L298 Integration
The motor drivers were used to control the 24V Henkwell Gear Motors. These drivers were controlled via Arduino Mega PWM and Digital Pins. These pins were given input from the Raspberry Pi GPIO pins. This approach was taken due to the concern of back current from the motor driver, which could damage the Raspberry Pi, so a cheaper and available middleman controller was placed. Our recommendation is to use an Arduino Nano instead.

### Pi to Arduino
A file which helps control 6 motor drivers using only 3 inputs. This was developed to address the concern stated above.

## Resources
- [MPU 6050 files for Raspberry Pi](https://github.com/m-rtijn/mpu6050)
- [General Tutorial Followed](https://github.com/microsoft/IoT-For-Beginners/blob/main/2-farm/lessons/4-migrate-your-plant-to-the-cloud/README.md)
- [Tutorial followed for implementing on Raspberry Pi](https://github.com/microsoft/IoT-For-Beginners/blob/main/2-farm/lessons/4-migrate-your-plant-to-the-cloud/single-board-computer-connect-hub.md)
- [C2D Message Implementation](https://learn.microsoft.com/en-us/azure/iot-hub/c2d-messaging-python)
- [Direct Message Theory](https://learn.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-direct-methods)
- [Direct Message Implementation](https://learn.microsoft.com/en-us/azure/iot-hub/device-management-python)
- [Python SDK for IoT Hub](https://github.com/Azure/azure-iot-hub-python)
- [Livestream with Pi-Cam](https://raspberrytips.com/how-to-live-stream-pi-camera/)
- [Streaming with USB webcam](https://raspberrypi.stackexchange.com/questions/115889/best-way-to-stream-usb-camera-video-in-2020)

## Current Problems:
1. NEO 6M GPS module not working with pynmea, readline error
2. MPU 6050 Integration Incomplete for now