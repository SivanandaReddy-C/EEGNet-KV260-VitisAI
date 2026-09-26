import mne

FILE = "datasets/BCICIV_2a/A01T.gdf"

print("Reading:", FILE)

raw = mne.io.read_raw_gdf(
    FILE,
    preload=False,
    verbose=False
)

print("\n--- Recording Information ---")
print("Channels      :", len(raw.ch_names))
print("Sampling rate :", raw.info["sfreq"], "Hz")
print("Duration      :", raw.times[-1], "seconds")

print("\n--- Channels ---")
for i, ch in enumerate(raw.ch_names):
    print(f"{i:2d}: {ch}")

print("\n--- Annotations ---")
print("Number of annotations:", len(raw.annotations))

for i, annotation in enumerate(raw.annotations[:20]):
    print(
        f"{i:2d}: "
        f"onset={annotation['onset']:.3f}s, "
        f"duration={annotation['duration']:.3f}s, "
        f"description={annotation['description']}"
    )