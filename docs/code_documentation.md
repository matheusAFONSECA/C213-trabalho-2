# Drone Fuzzy Control System Documentation

This document provides a detailed explanation of the components, methods, and logic implemented in the Drone Fuzzy Control System.

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Code Descriptions](#code-descriptions)
  - [FuzzyModels Class](#fuzzymodels-class)
  - [FuzzyControl Class](#fuzzycontrol-class)
  - [StreamlitApp Class](#streamlitapp-class)
  - [MQTTClient Class](#mqttclient-class)
- [MQTT Utilities](#mqtt-utilities)
  - [Monitor MQTT Script](#monitor-mqtt-script)
  - [MQTT Test Data Script](#mqtt-test-data-script)

---

## Overview

This project implements a fuzzy logic control system for managing the altitude of a drone. It uses fuzzy models, MQTT communication, and a Streamlit interface to allow real-time data visualization and interaction.

---

## Project Structure

```text

src/
├── data/
│   └── posicao_atual.txt          # Stores current drone position
├── fuzzy/
│   ├── models/
│   │   └── fuzzy_models.py        # Fuzzy models for control system
│   ├── utils/
│   │   └── fuzzy_utils.py         # Utility functions for fuzzy logic
│   └── fuzzy_control.py           # Implements the FuzzyControl class
├── interface/
│   └── streamlit_app.py           # Streamlit app for UI
├── mqtt/
│   └── mqtt_client.py             # MQTT client for communication
└── main.py                        # Main entry point for running the app

```

---

## Code Descriptions

### FuzzyModels Class

**File:** `fuzzy/models/fuzzy_models.py`

The `FuzzyModels` class defines fuzzy logic models and membership functions.

#### Key Methods:

- **`__init__()`**: Initializes fuzzy variables `Erro`, `dErro`, and `PotenciaMotor`.
- **`pertinence()`**: Defines membership functions for input and output variables.
- **`pertinence_error_plot()`**: Visualizes membership functions for `Erro`.
- **`pertinence_derror_plot()`**: Visualizes membership functions for `dErro`.
- **`pertinence_potencia_motor_plot()`**: Visualizes membership functions for `PotenciaMotor`.
- **`pertinence_plots()`**: Displays all pertinence plots.
- **`rules()`**: Defines a set of fuzzy control rules.

#### Usage:
This class is used to create fuzzy models and define control rules for the drone's altitude management.

---

### FuzzyControl Class

**File:** `fuzzy/fuzzy_control.py`

The `FuzzyControl` class applies fuzzy logic to compute altitude changes based on the current state of the drone.

#### Key Methods:

- **`__init__()`**: Initializes the control system using `FuzzyModels`.
- **`infer_rules()`**: Generates a DataFrame of fuzzy rules for visualization.
- **`Subir_e_Descer(Pos_Final)`**: Calculates the drone's position using fuzzy logic.
- **`set_home()`**: Sets the current position as the "home" position.
- **`go_to_home()`**: Moves the drone to the home position.
- **`ligar(altura)`**: Takes off the drone to a specified altitude.

#### Usage:
This class is responsible for handling the drone's movement logic, computing errors, and managing control rules.

---

### StreamlitApp Class

**File:** `interface/streamlit_app.py`

The `StreamlitApp` class provides a user interface for interacting with the drone control system.

#### Key Methods:

- **`__init__(mqtt_client, fuzzy_control)`**: Initializes the app with an MQTT client and fuzzy control object.
- **`run()`**: Runs the Streamlit app with tabs for sending and visualizing data.
- **`send_data_tab()`**: Allows users to input altitude and send data to the drone.
- **`visualize_data_tab()`**: Visualizes pertinence functions and rules in a tabular format.

#### Usage:
This class provides an interactive interface for monitoring and controlling the drone.

---

### MQTTClient Class

**File:** `mqtt/mqtt_client.py`

The `MQTTClient` class handles MQTT communication for publishing and subscribing to topics.

#### Key Methods:

- **`__init__(broker, topics)`**: Initializes the MQTT client with a broker and topics.
- **`connect()`**: Connects to the broker and subscribes to topics.
- **`on_message(client, userdata, msg)`**: Processes incoming messages.
- **`publish(topic, data)`**: Publishes data to a specified topic.

#### Usage:
This class enables communication between the fuzzy control system and the drone via MQTT.

---

## MQTT Utilities

### Monitor MQTT Script

**File:** `mqtt/monitor_mqtt.py`

This script monitors MQTT topics and prints received messages.

#### Key Functions:

- **`on_connect(client, userdata, flags, rc)`**: Subscribes to topics upon connection.
- **`on_message(client, userdata, message)`**: Decodes and displays messages.
- **`on_disconnect(client, userdata, rc)`**: Attempts to reconnect when disconnected.

---

### MQTT Test Data Script

**File:** `mqtt/mqtt_test_data.py`

This script publishes random test data to MQTT topics for testing.

#### Key Functions:

- **`generate_random_data(topic)`**: Generates random data for altitude and error topics.
- **`main()`**: Publishes data to topics at regular intervals.

---
