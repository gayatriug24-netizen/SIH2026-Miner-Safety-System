# JEEVAN SETU – AI-Powered Underground Mine Safety, Monitoring and Rescue System

JEEVAN SETU is an AI-powered underground mine safety and rescue
system developed for Smart India Hackathon 2026. The system combines
a smart miner helmet-torch module, a reconnaissance rover and a
surface control station to provide better worker monitoring,
environmental awareness and rescue support.

## 1. Project Information

- Project Title: JEEVAN SETU
- Problem Statement ID: SIH26039
- Problem Statement: AI-Powered Underground Mine Safety, Monitoring and Rescue System
- Theme: Smart Automation
- Category: Hardware
- Team Name: MINERDS

## 2. Problem Statement

Underground mine rescue operations can become difficult when
rescue teams do not have a live picture of the mine and the
condition of workers.

The major challenges include:

- Limited situational awareness during emergencies
- Difficulty in locating workers underground
- Toxic gases, high temperature, flooding and debris
- Delayed emergency communication
- Separate sources of worker and environmental information

These factors can increase the time required to understand an
emergency and plan a safe rescue response.

## 3. Proposed Solution

JEEVAN SETU consists of three main components:

### Smart Miner Helmet-Torch

The existing safety helmet/torch is enhanced with electronics for
worker identification, movement and fall detection, vital
monitoring and emergency communication.

An ESP32 processes the worker data. The MPU6050 is used for fall
and inactivity detection, while an OLED, buzzer and emergency
push button provide local status and emergency interaction.

### AI Rescue Rover

The reconnaissance rover is designed to enter hazardous or
inaccessible areas before rescue personnel.

It collects environmental and visual information using sensors
including the MQ-2 gas sensor, DHT11 and HC-SR04. An ESP32-CAM
provides live video and wireless communication.

LiDAR can be used for underground mapping and localization.

### Surface Control Station

A browser-based control station provides a unified view of worker,
rover and environmental information.

The dashboard is intended to display live data, video and emergency
events so that rescue teams can assess the situation before
entering the affected area.

## 4. System Workflow

The overall system follows the workflow:

Miner
  |
  +--> Smart Helmet-Torch --> Worker Data
  |
  +--> AI Rescue Rover --> Mine Environment Data
                              |
                              v
                    Surface Control Station
                              |
                              v
                       AI / Event Analysis
                              |
                              v
                         Risk / Alert
                              |
                              v
                    Human Rescue Decision

The system follows a human-in-the-loop approach. AI is used to
support the analysis and prioritization of events, while the final
rescue decision remains with trained personnel.

## 5. Technical Approach

### Smart Miner Helmet-Torch Layer

- ESP32 for processing and wireless transmission
- MPU6050 for fall and inactivity detection
- OLED for local status information
- Emergency push button for SOS
- Buzzer for local alerts
- Li-ion battery for power

### Reconnaissance Rover Layer

- Arduino Nano for rover control
- 2WD geared chassis
- L298N motor driver
- HC-SR04 for obstacle detection
- MQ-2 for smoke and combustible-gas detection
- DHT11 for temperature and humidity monitoring
- ESP32-CAM for live video
- LiDAR for mapping and localization

### Surface Control Station

The monitoring interface uses:

- HTML5
- CSS
- JavaScript
- Python / Flask
- WebSockets
- Chart.js

The control station provides real-time monitoring of worker,
rover and environmental information.

## 6. Key Features

### Worker Monitoring
- Worker identification
- Fall detection
- Inactivity detection
- Emergency SOS
- Worker status monitoring

### Mine Monitoring
- Gas detection
- Temperature and humidity monitoring
- Obstacle detection
- Live video
- Underground mapping

### Rescue Support
- Real-time worker information
- Last known worker location/zone
- Environmental information
- Emergency alerts
- Rover-based reconnaissance
- Unified control station

## 7. Unique Features

### Existing-Equipment Integration

The system upgrades the miner's existing helmet/torch instead of
requiring an additional wearable device.

### Direct Worker SOS

The emergency push button provides a direct way for a worker to
send an SOS to the control station.

### Mobile Mine Intelligence

The rover can be sent into hazardous or inaccessible areas to
collect information before human entry.

### Worker and Mine Data Fusion

Worker status and surrounding environmental conditions are
considered together during an emergency.

### Resilient Emergency Response

The worker SOS mechanism is independent of the rover, allowing
emergency communication even if the rover becomes unavailable.

### Human-in-the-Loop Rescue

The system provides information and recommendations to rescue
teams while keeping the final decision with trained personnel.

## 8. Feasibility and Viability

The proposed system is designed as a modular and low-cost
prototype that can be developed and tested before being scaled
towards mine-grade technology.

### Major Risks

- Communication limitations
- Localization challenges
- Harsh underground conditions
- False alarms

### Possible Mitigation

- Relay nodes for communication
- Last-known worker zone
- Protected hardware enclosure
- Sensor fusion for better event detection

The prototype focuses on demonstrating the critical
emergency-to-rescue workflow rather than attempting to solve every
requirement of a complete underground mine on the first version.

## 9. Expected Impact

JEEVAN SETU aims to improve underground mine rescue operations by:

- Reducing emergency detection time
- Reducing worker localization time
- Reducing response delay
- Improving awareness of mine hazards
- Providing information before rescuers enter hazardous areas
- Supporting faster and better-informed rescue decisions

## 10. Hardware and Software

| Layer | Hardware / Software |
| --- | --- |
| Smart Helmet-Torch | ESP32, MPU6050, OLED, SOS Button, Buzzer, Li-ion Battery |
| Rescue Rover | Arduino Nano, 2WD Chassis, L298N, HC-SR04, MQ-2, DHT11 |
| Vision & Communication | ESP32-CAM, Wi-Fi / ESP-NOW |
| Mapping | LiDAR |
| Control Station | HTML5, CSS, JavaScript, Python/Flask |
| Real-time Communication | WebSockets |
| Dashboard | Chart.js |

## 11. Repository Structure

```text
SIH2026-Miner-Safety-System/
│
├── README.md
│
├── src/
│   ├── firmware/
│   ├── rover/
│   ├── control-station/
│   └── ai/
│
├── docs/
│   ├── architecture/
│   ├── hardware/
│   └── methodology/
│
├── assets/
│   ├── screenshots/
│   ├── diagrams/
│   └── hardware/
│
└── submission/
    ├── presentation/
    └── demo/
##12. Project Status

```text
SIH2026-Miner-Safety-System/

JEEVAN SETU is being developed as a prototype for Smart India
Hackathon 2026.

The current development focuses on integrating the worker
monitoring unit, reconnaissance rover and control station into a
single emergency-to-rescue workflow.

##13. Research and References

```text
SIH2026-Miner-Safety-System/

The project has referred to existing work and technical
documentation related to:

Mine rescue robots
Underground mine mapping
Gas and environmental sensing
ESP32 and MPU6050
LiDAR systems
ROS 2 and Nav2
YOLO
Streamlit

Detailed references used during the development are documented
separately in the docs/ directory.

##14. Team

```text
SIH2026-Miner-Safety-System/

Team Name: MINERDS

Project: JEEVAN SETU

Smart India Hackathon 2026

Problem Statement ID: SIH26039
