from pylsl import StreamInlet, resolve_byprop
from scipy.signal import welch
import numpy as np
import time
import serial

# ========== Configuration ==========
fs = 256
samples_per_window = fs * 1
alpha_band = (8, 12)
beta_band = (13, 30)

engagement_threshold = 10
window_size = 20

# Arduino setup
arduino = serial.Serial('COM5', 9600)  # Replace with your actual port
time.sleep(2)  # Wait for Arduino to initialize

# Engagement tracking
engagement_history = []
led_state = False
buzzer_state = False

# ========== EEG Stream ==========
print("Looking for EEG stream...")
streams = resolve_byprop('type', 'EEG', timeout=10)
inlet = StreamInlet(streams[0])
print("EEG stream connected.")

print("\n Real-time Focus Detection (with LED + Buzzer)")
print("---------------------------------------------------")

while True:
    data = []
    while len(data) < samples_per_window:
        sample, _ = inlet.pull_sample()
        data.append(sample)

    data = np.array(data).T
    eeg = (data[1] + data[2]) / 2  # AF7 + AF8

    freqs, psd = welch(eeg, fs=fs, nperseg=128)

    def bandpower(band):
        mask = (freqs >= band[0]) & (freqs <= band[1])
        return np.trapz(psd[mask], freqs[mask])

    alpha_power = bandpower(alpha_band)
    beta_power = bandpower(beta_band)
    engagement_index = beta_power / (alpha_power + 1e-6)

    is_focused = engagement_index > engagement_threshold
    engagement_history.append(is_focused)
    if len(engagement_history) > window_size:
        engagement_history.pop(0)

    focused_count = engagement_history.count(True)
    unfocused_count = engagement_history.count(False)

    print(f"α: {alpha_power:.2f} | β: {beta_power:.2f} | β/α: {engagement_index:.2f}  =>  {'Focused' if is_focused else 'Not Focused'}")

    # LED control
    if focused_count > 10 and not led_state:
        arduino.write(b'LED_ON\n')
        led_state = True
    elif focused_count <= 10 and led_state:
        arduino.write(b'LED_OFF\n')
        led_state = False

    # Buzzer control
    if unfocused_count >= 15 and not buzzer_state:
        arduino.write(b'BEEP\n')
        buzzer_state = True
        print("Buzzer ON (too much distraction)")
        engagement_history.clear()  # Reset after alert
    elif unfocused_count < 15 and buzzer_state:
        buzzer_state = False

    time.sleep(0.2)
