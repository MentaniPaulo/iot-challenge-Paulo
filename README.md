# IoT Challenge

The camera_container directory contains an application that simulates several routes, representing the API used to access video history metadata from a specific model of security camera.

Your task is to create an application that consumes this API and aggregates the data it provides. The camera API is quite verbose and slow, so it's beneficial to group the data for faster future access while consuming less bandwidth.

The new API you develop should have the capability to respond with the camera's video history, including filters for time (start and end) and video type.

Your responsibilities also include understanding how the code simulating the camera_container works, and the format of the data it provides.

The expected outcome of this challenge is a well-documented, tested, and efficient application (both the new API and the camera_container app). Additionally, it is recommended to create a Docker Compose configuration that integrates both applications.

### Additional Data:
```
record_type:
    NormalRecord: 0x1
    AlarmRecord: 0x2
    MotionRecord: 0x4
```