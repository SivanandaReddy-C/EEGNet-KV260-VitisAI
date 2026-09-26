import mne
import numpy as np

FILE = "datasets/BCICIV_2a/A01T.gdf"

print("Reading:", FILE)

raw = mne.io.read_raw_gdf(
    FILE,
    preload=False,
    verbose=False
)

# Extract annotations
annotations = raw.annotations

# Store trial-start and motor-imagery events
trial_starts = []
motor_events = []

for ann in annotations:
    code = ann["description"]
    onset = ann["onset"]

    if code == "768":
        trial_starts.append(onset)

    elif code in {"769", "770", "771", "772"}:
        motor_events.append((onset, int(code)))

print("\n--- Trial Timing Analysis ---")

print("Trial starts (768):", len(trial_starts))
print("Motor-imagery events:", len(motor_events))

# Find the trial start immediately preceding each motor-imagery event
delays = []

for onset, code in motor_events:
    previous_starts = [
        start for start in trial_starts
        if start <= onset
    ]

    if previous_starts:
        trial_start = previous_starts[-1]
        delay = onset - trial_start
        delays.append(delay)

print("\n--- Delay: Trial Start (768) -> Motor Cue (769-772) ---")

if delays:
    print("Number of matched trials:", len(delays))
    print("Minimum delay           :", np.min(delays), "s")
    print("Maximum delay           :", np.max(delays), "s")
    print("Mean delay              :", np.mean(delays), "s")
    print("Unique delays           :", sorted(set(np.round(delays, 3))))

# Check intervals between consecutive motor-imagery cues
cue_onsets = [onset for onset, code in motor_events]

if len(cue_onsets) > 1:
    intervals = np.diff(cue_onsets)

    print("\n--- Consecutive Motor Cue Intervals ---")
    print("Minimum interval:", np.min(intervals), "s")
    print("Maximum interval:", np.max(intervals), "s")
    print("Mean interval   :", np.mean(intervals), "s")

print("\n--- First 10 Motor-Imagery Events ---")

for onset, code in motor_events[:10]:
    label = {
        769: "Left hand",
        770: "Right hand",
        771: "Feet",
        772: "Tongue",
    }[code]

    print(
        f"Onset={onset:.3f}s | "
        f"Code={code} | "
        f"Class={label}"
    )