# ROS 2 Base Station Package (`base_station_pkg`)

## Overview

- **Mock Camera Generation**: Uses OpenCV and `cv_bridge` to create a live synthetic video stream ("BASE STATION LIVE") and publish it to the ROS 2 domain as a standard `sensor_msgs/msg/Image`.
- **Sensor Telemetry**: Publishes sensor readings or status telemetry across ROS 2 nodes.
- **Web Video Bridge**: Integrates with `web_video_server` to convert ROS 2 image topics into an MJPEG stream accessible via any web browser across local network devices (such as a host Mac or client PC).

---

##  Package Structure

```text
climb_base_station/
├── climb_dashboard/              # Flask Web Application (Port 5000)
│   ├── app.py                    # Flask server entry point
│   ├── templates/                # HTML layout files
│   └── static/                   # CSS and JavaScript assets
│
├── simulation/                   # Simulation Assets
│   └── pipes_world.sdf           # Gazebo pipe inspection world environment
│
├── src/                          # ROS 2 Source Workspace
│   └── base_station_pkg/         # ROS 2 Package
│       ├── base_station_pkg/     # Python source module
│       │   ├── __init__.py
│       │   ├── mock_cam_node.py  # Camera image publisher node
│       │   └── sensor_publisher.py # Telemetry publisher node
│       ├── resource/
│       ├── test/
│       ├── package.xml
│       ├── setup.cfg
│       └── setup.py
│
└── README.md                
```

---

##  Components & Executables

### 1. `mock_cam_node.py` 
* **Purpose**: Generates dynamic video frames using OpenCV with embedded text labels (`BASE STATION LIVE`), converts them into `sensor_msgs/msg/Image` using `cv_bridge`, and publishes them periodically.
* **Topic Published**: `/camera/image_raw` (`sensor_msgs/msg/Image`)
* **Frequency**: 10 Hz (0.1s timer interval)

### 2. `sensor_publisher.py` (Executable: `sensor_pub`)
* **Purpose**: Simulates telemetry or sensor data publication across the ROS 2 network.

### 3. `web_video_server` (External ROS 2 Node)
* **Purpose**: Subscribes to `/camera/image_raw` and serves an interactive web interface with an MJPEG video stream accessible at `http://<IP_ADDRESS>:8080`.

---

## Dependencies
  * `rclpy`
  * `sensor_msgs`
  * `cv_bridge`
  * `python3-opencv`
  * `ros-<distro>-web-video-server`

---
## Installation & Build Instructions

### Step 1: Source ROS 2 Environment
```bash
source /opt/ros/humble/setup.bash
```

### Step 2: Navigate to Workspace
```bash
# Navigate to the base station directory
cd ~/climb_base_station
```

### Step 3: Install Package Dependencies
```bash
cd ~/climb_base_station

sudo apt update
sudo apt install ros-humble-web-video-server python3-opencv -y
```

### Step 4: Build the Workspace
```bash
cd ~/climb_base_station
colcon build
```

---

##  Running 

### Step 1: Terminal 1 — Run Sensor Publisher
```bash
cd ~/climb_base_station
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run base_station_pkg sensor_pub
```

### Step 2: Terminal 2 — Run Mock Camera Node
```bash
cd ~/climb_base_station
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run base_station_pkg mock_cam
```

### Step 3: Terminal 3 — Launch Web Video Server
```bash
cd ~/climb_base_station
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run web_video_server web_video_server
```

---

## Viewing the Stream on a Host

1. Find your machine's IP address:
   ```bash
   hostname -I
   ```
2. Open a web browser (Safari, Chrome, Firefox) on your host Mac or client device.
3. Access the web interface at:
   ```text
   http://<YOUR_IP_ADDRESS>:8080
   ```
   *(Example: `http://192.168.64.2:8080`)*
4. Click on the `/camera/image_raw` link in the topic list to view the live synthetic camera feed.

# Operator Dashboard

Note that this is not completely operational. The objectives were to make a dashboard that toggles individual sensor readings like UT and Odom on/off on the display, but the backend via Flask is not working. However, if you want to see the package structure and reuse the code, you can look below.

```text
 climb_dashboard/
  ├── app.py
  ├── templates/
  └── static/

```
### Operating instructions
Run the following commands in a new Terminal 
```text
cd ~/climb_base_station
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build
```
Now open 4 Terminal windows, and run the 3 commands for each respective window as mentioned previously. In the remaining window, run these following commands:
```
cd ~/climb_base_station/climb_dashboard
python3 app.py
```
## Viewing the Dashboard

1. Find your machine's IP address:
   ```bash
   hostname -I
   ```
2. Open a web browser (Safari, Chrome, Firefox) on your host Mac or client device.
3. Access the web interface at:
   ```text
   http://<YOUR_IP_ADDRESS>:5000
   ```
   *(Example: `http://192.168.64.2:5000`)*
4. Use the Toggle Odom Overlay and Toggle UT Overlay buttons below the stream to control telemetry visibility.

# World Files
The world files can be found at ['pipes_world.sdf'](simulation/pipes_world.sdf).