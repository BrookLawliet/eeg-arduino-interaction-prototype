# EEG-Based Arduino Interaction Prototype

This project demonstrates a simple EEG-based interactive control system using Python signal processing and Arduino-based output control.

## Demo Video

YouTube demo video:  
Eye status control via EEG: https://youtu.be/cobWKBGCmuM 
Concentration control via EEG: https://youtu.be/6-eNrrrxXvw

## Project Overview

The goal of this prototype is to explore how EEG signals can be used as a simple input channel for interactive systems. EEG signals are acquired from a wearable EEG device, processed in Python, and then used to control output devices through Arduino.

## System Pipeline

1. EEG signal acquisition
2. Signal preprocessing in Python
3. Feature extraction from EEG signals
4. Command generation
5. Arduino-based output control
6. LED and buzzer activation

## Hardware

- Wearable EEG device (Muse 2)
- Arduino board
- LED
- Buzzer

## Software

- Python
- Arduino

## Environment Setup

The EEG signal was acquired using a Muse 2 headset. The Python environment was used for real-time signal acquisition and signal processing, while Arduino was used for output control.

Example workflow:

1. Connect the Muse 2 headset via Bluetooth.
2. Start the Python environment for EEG signal acquisition and processing.
3. Run the EEG processing script.
4. Upload the Arduino control program to the Arduino board.
5. Execute the prototype and observe LED/buzzer responses.

Note: The exact environment configuration may depend on the operating system, Bluetooth connection method, and installed Python packages.

## Motivation

This prototype was developed independently after my undergraduate studies. Through this project, I became interested in using biological signals such as EEG, gaze, and visual information as new channels for human-computer interaction, human augmentation, and behavior understanding.
