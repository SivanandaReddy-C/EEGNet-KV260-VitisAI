import mne
import numpy as np

FILE = "datasets/BCICIV_2a/A01T.gdf"

raw = mne.io.read_raw_gdf(
    FILE,
    preload=False,
    verbose=False
)

sfreq = raw.info["sfreq"]

print("--- Sampling Information ---")
print("Sampling frequency:", sfreq, "Hz")
print("Samples per second:", int(sfreq))

# Find first trial start and corresponding motor-imagery cue
trial_start = None
motor_cue = None
motor_code = None

for ann in raw.annotations:
    code = ann["description"]

    if code == "768" and trial_start is None:
        trial_start = ann["onset"]

    elif (
        trial_start is not None
        and code in {"769", "770", "771", "772"}
        and motor_cue is None
    ):
        motor_cue = ann["onset"]
        motor_code = int(code)
        break

print("\n--- First Trial ---")
print("Trial start :", trial_start, "s")
print("Motor cue   :", motor_cue, "s")
print("Motor code  :", motor_code)

# Convert times to sample indices
trial_start_sample = round(trial_start * sfreq)
motor_cue_sample = round(motor_cue * sfreq)

print("\n--- Sample Indices ---")
print("Trial start sample:", trial_start_sample)
print("Motor cue sample  :", motor_cue_sample)

delay_samples = motor_cue_sample - trial_start_sample

print("\n--- Trial Start -> Motor Cue ---")
print("Delay in samples:", delay_samples)
print("Delay in seconds:", delay_samples / sfreq)

# Official trial boundary used for inspection: 6 seconds
trial_end_time = trial_start + 6.0
trial_end_sample = round(trial_end_time * sfreq)

print("\n--- Trial Boundary ---")
print("Trial end time   :", trial_end_time, "s")
print("Trial end sample :", trial_end_sample)

# Motor imagery period approximately 1.25 to 4 seconds after cue
mi_start = motor_cue + 1.25
mi_end = motor_cue + 4.0

mi_start_sample = round(mi_start * sfreq)
mi_end_sample = round(mi_end * sfreq)

print("\n--- Nominal Motor-Imagery Window ---")
print("Start time   :", mi_start, "s")
print("End time     :", mi_end, "s")
print("Start sample :", mi_start_sample)
print("End sample   :", mi_end_sample)
print("Samples      :", mi_end_sample - mi_start_sample)

# Check 0-4 second window from cue
cue_window_start = motor_cue
cue_window_end = motor_cue + 4.0

cue_start_sample = round(cue_window_start * sfreq)
cue_end_sample = round(cue_window_end * sfreq)

print("\n--- 0-4 s Window From Cue ---")
print("Start sample:", cue_start_sample)
print("End sample  :", cue_end_sample)
print("Samples     :", cue_end_sample - cue_start_sample)

print("\n--- Expected Fixed Window Sizes ---")
print("1 second :", int(sfreq), "samples")
print("2 seconds:", int(2 * sfreq), "samples")
print("3 seconds:", int(3 * sfreq), "samples")
print("4 seconds:", int(4 * sfreq), "samples")