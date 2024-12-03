# C213-trabalho-2

Repository dedicated to storing the codes for the second project of the C213 - Embedded Systems course at INATEL - Instituto Nacional de Telecomunicações. This repository contains a project developed for a system that uses Fuzzy Logic to perform corrections and optimizations within the system.

## Index

1. [Overview](#overview)  
2. [Documentation](#documentation)  
3. [Getting Started](#getting-started)  
   3.1 [Cloning the Repository](#cloning-the-repository)  
   3.2 [Setting Up the Virtual Environment](#setting-up-the-virtual-environment)  
   3.3 [Installing the Requirements](#installing-the-requirements)  
4. [Running the Project](#running-the-project)  
5. [Authors](#authors)

## Overview

This project features an interface developed with **Streamlit** that leverages a **Fuzzy Control System**. The results are transmitted via **Mosquitto-MQTT** to a dashboard managed by **Node-RED**, where system errors and fuzzy control outcomes are displayed.

## Documentation

The repository includes comprehensive documentation covering the code, project structure, and the interface, with explanatory images:

- [**Code and Project Structure Documentation**](/docs/code_documentation.md)

- [**Interface Documentation**](/docs/interface_documentation.md)

## Getting Started

Follow the steps below to set up and run the project locally.

### Cloning the Repository

To get started, clone this repository to your local machine. Run the following command in the directory where you want to save the repository:

```bash
git clone https://github.com/matheusAFONSECA/C213-trabalho-2.git
```

### Setting Up the Virtual Environment

A Python interpreter must be previous installed on your machine to create and activate the virtual environment. There are two ways to set up the virtual environment:

#### 1 - Using Commands

To create a virtual environment in your repository, run the following command:

```bash
python -m venv C213venv
```

After creating the virtual environment, activate it with the following command:

```bash
.\C213venv\Scripts\activate
```

#### 2 - Using Scripts

Alternatively, you can use one of the scripts provided in the `scripts` directory to automate the setup:

- **Windows:**

```bash
.\scripts\create_and_activate_venv.ps1
```

- **Linux or macOS:**

```bash
./scripts/create_and_activate_venv.sh
```

### Installing the Requirements

Once the virtual environment is active, install the required dependencies by running the following command:

```bash
pip install -r requirements.txt
```

## Running the project

### Streamlit Interface

To run the application, execute the following command:

```bash
streamlit run src/main.py
```

### Node-RED Dashboard

To visualize the MQTT messages in the Node-RED dashboard, run the following command in a separate terminal:

```bash
node-red
```

> Note:
> Ensure that your machine has npm installed, along with the necessary modules to run Node-RED. Additionally, verify that the Node-RED connections are properly configured.


## Authors

### [Matheus Fonseca](https://github.com/matheusAFONSECA)

Undergraduate student in the eighth (8th) semester of Computer Engineering at the National Institute of Telecommunications (Inatel). I participated in a Scientific Initiation at the Cybersecurity and Internet of Things Laboratory (CS&ILAB), where, in the Park Here project, I developed skills in computer vision applied to parking systems, focusing on license plate recognition and vehicle identification. Additionally, I served as a teaching assistant for Physics 1, 2, and 3, helping with practical classes, report writing, and answering theoretical questions. Currently, I am an intern at the Inatel Competence Center (ICC) in the PDI SW department.

## [Davi Rosa](https://github.com/DaviRGomes)
Computer Engineering student at Inatel, currently in the 8th semester. At 21 years old, I am completing my degree, focused on gaining practical experience and specializing in an area related to the course I am finishing.
