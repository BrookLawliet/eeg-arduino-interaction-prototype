from pylsl import StreamInlet, resolve_byprop
from scipy.signal import welch
import numpy as np
import time
import serial

# === Configuration ===
COM_PORT = 'COM5'         
BAUD_RATE = 9600
THRESHOLD = 20            # Alpha power threshold

# Connect to Arduino
arduino = serial.Serial(COM_PORT, BAUD_RATE)
print(f" Arduino connected on {COM_PORT}")

# Connect to EEG stream
print(" Looking for EEG stream...")
streams = resolve_byprop('type', 'EEG', timeout=10)
inlet = StreamInlet(streams[0])
print(" EEG stream connected.")

# EEG parameters
fs = 256
samples_per_window = fs * 1
alpha_band = (8, 12)

# Eye state tracking
eye_states = []            # For blink detection
recent_eye_states = []     # For sleep detection
led_state = False

print("\n Real-time Alpha Power Monitoring (Blink + Sleep Detection)")

while True:
    data = []
    while len(data) < samples_per_window:
        sample, _ = inlet.pull_sample()
        data.append(sample)

    data = np.array(data).T
    eeg = (data[0] + data[3]) / 2  # Use TP9 and TP10 average

    freqs, psd = welch(eeg, fs=fs, nperseg=128)
    alpha_mask = (freqs >= alpha_band[0]) & (freqs <= alpha_band[1])
    alpha_power = np.trapz(psd[alpha_mask], freqs[alpha_mask])

    current_state = 'open' if alpha_power <= THRESHOLD else 'closed'
    print(f"Alpha Power: {alpha_power:.2f}   {' Eyes Open' if current_state == 'open' else ' Eyes Closed'}")

    # Blink sequence detection
    eye_states.append(current_state)
    if len(eye_states) > 4:
        eye_states.pop(0)

    if eye_states == ['open', 'closed', 'open', 'closed']:
        led_state = not led_state
        arduino.write(b'ON\n' if led_state else b'OFF\n')
        print(f" LED Toggled: {'ON' if led_state else 'OFF'}")
        eye_states.clear()

    # Sleep detection: over 20 'closed' in last 30 readings
    recent_eye_states.append(current_state)
    if len(recent_eye_states) > 30:
        recent_eye_states.pop(0)

    if recent_eye_states.count('closed') > 20:
        if led_state:
            arduino.write(b'OFF\n')
            led_state = False
            print(" Sleep detected →  LED Forced OFF")
        eye_states.clear()
        recent_eye_states.clear()

    time.sleep(0.2)
