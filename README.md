# IoT Challenge

`camera_container` directory contains an application with a couple of routes simulating an API used to access stored video metadata from a specific model of security camera.

Your task is to create an application that consumes this API and aggregates the data it provides. The camera API is quite verbose and slow, so it's beneficial to group the data for faster future access while consuming less bandwidth.

The new API should be able to respond about the camera's stored videos, filtering for start time, end time and video type.

The expected outcome of this challenge is a well-documented, tested, and efficient application (including both the new API and the `camera_container` app). Additionally, it is recommended to create a Docker Compose configuration that integrates both applications.

### Additional Data:
```
record_type:
    NormalRecord: 0x1
    AlarmRecord: 0x2
    MotionRecord: 0x4
```
