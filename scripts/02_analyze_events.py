import mne
from collections import Counter

FILE = "datasets/BCICIV_2a/A01T.gdf"

print("Reading:", FILE)

raw = mne.io.read_raw_gdf(
    FILE,
    preload=False,
    verbose=False
)

events, event_id = mne.events_from_annotations(
    raw,
    verbose=False
)

# Reverse mapping: MNE event ID -> original annotation code
event_id_reverse = {value: key for key, value in event_id.items()}

# Count events
counts = Counter(events[:, 2])

print("\n--- Event Counts ---")

for event_code, count in sorted(counts.items()):
    original_code = event_id_reverse.get(event_code, event_code)
    print(f"{original_code}: {count}")

print("\n--- Motor Imagery Events ---")

motor_imagery_codes = {
    "769": "Left hand",
    "770": "Right hand",
    "771": "Feet",
    "772": "Tongue",
}

for code, label in motor_imagery_codes.items():
    count = sum(
        1 for event in raw.annotations
        if event["description"] == code
    )
    print(f"{code} -> {label:12s}: {count}")