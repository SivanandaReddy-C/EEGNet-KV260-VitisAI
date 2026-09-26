import os
import numpy as np
import mne

# ============================================================
# Configuration
# ============================================================

DATA_DIR = "datasets/BCICIV_2a"
OUTPUT_DIR = "datasets/processed"

SFREQ = 250
N_EEG_CHANNELS = 22
N_SAMPLES = 1000

LOW_FREQ = 8.0
HIGH_FREQ = 30.0

# Motor-imagery event codes
EVENT_LABELS = {
    "769": 0,   # Left hand
    "770": 1,   # Right hand
    "771": 2,   # Feet
    "772": 3,   # Tongue
}

LABEL_NAMES = {
    0: "Left hand",
    1: "Right hand",
    2: "Feet",
    3: "Tongue",
}

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# Main preprocessing
# ============================================================

def main():

    all_X = []
    all_y = []
    all_subjects = []

    print("=" * 50)
    print(" EEG PREPROCESSING")
    print("=" * 50)

    # --------------------------------------------------------
    # Process subjects A01T to A09T
    # --------------------------------------------------------

    for subject in range(1, 10):

        filename = f"A{subject:02d}T.gdf"
        filepath = os.path.join(DATA_DIR, filename)

        print(f"\nProcessing {filename}")

        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"Dataset file not found: {filepath}"
            )

        # ----------------------------------------------------
        # 1. Read GDF
        # ----------------------------------------------------

        raw = mne.io.read_raw_gdf(
            filepath,
            preload=False,
            verbose=False
        )

        # ----------------------------------------------------
        # 2. Verify sampling frequency
        # ----------------------------------------------------

        if raw.info["sfreq"] != SFREQ:
            raise ValueError(
                f"{filename}: Expected sampling frequency "
                f"{SFREQ} Hz, found {raw.info['sfreq']} Hz"
            )

        # ----------------------------------------------------
        # 3. Explicitly select the 22 EEG channels
        #
        # MNE identifies all 25 channels as EEG in this GDF.
        # Therefore, channel names are used to exclude EOG.
        # ----------------------------------------------------

        eeg_names = [
            ch for ch in raw.ch_names
            if not ch.startswith("EOG-")
        ]

        if len(eeg_names) != N_EEG_CHANNELS:
            raise ValueError(
                f"{filename}: Expected "
                f"{N_EEG_CHANNELS} EEG channels, "
                f"found {len(eeg_names)}"
            )

        eeg_picks = mne.pick_channels(
            raw.ch_names,
            include=eeg_names
        )

        print("  EEG channels:", len(eeg_names))

        # ----------------------------------------------------
        # 4. Load EEG data
        # ----------------------------------------------------

        raw.load_data()

        # ----------------------------------------------------
        # 5. Band-pass filter: 8–30 Hz
        # ----------------------------------------------------

        raw.filter(
            l_freq=LOW_FREQ,
            h_freq=HIGH_FREQ,
            picks=eeg_picks,
            method="fir",
            verbose=False
        )

        # ----------------------------------------------------
        # 6. Extract motor-imagery trials
        # ----------------------------------------------------

        subject_X = []
        subject_y = []

        for annotation in raw.annotations:

            code = annotation["description"]

            # Ignore all non-motor-imagery events
            if code not in EVENT_LABELS:
                continue

            label = EVENT_LABELS[code]

            # ------------------------------------------------
            # Convert cue onset to sample index
            # ------------------------------------------------

            cue_sample = raw.time_as_index(
                annotation["onset"],
                use_rounding=True
            )[0]

            end_sample = cue_sample + N_SAMPLES

            # ------------------------------------------------
            # Check that complete 4-second window exists
            # ------------------------------------------------

            if end_sample > raw.n_times:
                print(
                    f"  WARNING: Skipping event at "
                    f"{annotation['onset']:.3f}s "
                    f"(insufficient samples)"
                )
                continue

            # ------------------------------------------------
            # Extract:
            # 22 EEG channels × 1000 samples
            # ------------------------------------------------

            epoch = raw.get_data(
                picks=eeg_picks,
                start=cue_sample,
                stop=end_sample
            )

            if epoch.shape != (
                N_EEG_CHANNELS,
                N_SAMPLES
            ):
                raise ValueError(
                    f"{filename}: Unexpected epoch shape "
                    f"{epoch.shape}"
                )

            # ------------------------------------------------
            # Per-trial, per-channel normalization
            #
            # Each EEG channel is normalized independently
            # across its 1000 time samples.
            # ------------------------------------------------

            mean = epoch.mean(
                axis=1,
                keepdims=True
            )

            std = epoch.std(
                axis=1,
                keepdims=True
            )

            # Prevent division by zero
            std[std < 1e-12] = 1.0

            epoch = (epoch - mean) / std

            # ------------------------------------------------
            # Store trial
            # ------------------------------------------------

            subject_X.append(
                epoch.astype(np.float32)
            )

            subject_y.append(label)

        # ----------------------------------------------------
        # Convert subject data to NumPy arrays
        # ----------------------------------------------------

        subject_X = np.asarray(
            subject_X,
            dtype=np.float32
        )

        subject_y = np.asarray(
            subject_y,
            dtype=np.int64
        )

        print("  Trials:", len(subject_X))
        print("  Shape :", subject_X.shape)

        # ----------------------------------------------------
        # Store subject data
        # ----------------------------------------------------

        all_X.append(subject_X)
        all_y.append(subject_y)

        all_subjects.extend(
            [subject] * len(subject_y)
        )

    # ========================================================
    # Combine all subjects
    # ========================================================

    X = np.concatenate(
        all_X,
        axis=0
    )

    y = np.concatenate(
        all_y,
        axis=0
    )

    subjects = np.asarray(
        all_subjects,
        dtype=np.int64
    )

    # ========================================================
    # Add PyTorch input-channel dimension
    #
    # Before:
    #     [N, 22, 1000]
    #
    # After:
    #     [N, 1, 22, 1000]
    # ========================================================

    X = X[:, np.newaxis, :, :]

    # ========================================================
    # Final dataset information
    # ========================================================

    print("\n" + "=" * 50)
    print(" FINAL DATASET")
    print("=" * 50)

    print("X shape      :", X.shape)
    print("y shape      :", y.shape)
    print("Subjects     :", subjects.shape)

    # ========================================================
    # Class distribution
    # ========================================================

    print("\nClass distribution:")

    for label in range(4):

        count = np.sum(y == label)

        print(
            f"  Class {label} "
            f"({LABEL_NAMES[label]:10s}): {count}"
        )

    # ========================================================
    # Subject distribution
    # ========================================================

    print("\nSubject distribution:")

    for subject in range(1, 10):

        count = np.sum(
            subjects == subject
        )

        print(
            f"  A{subject:02d}T: {count}"
        )

    # ========================================================
    # Dataset sanity checks
    # ========================================================

    print("\nSanity checks:")

    assert X.ndim == 4
    assert X.shape[1] == 1
    assert X.shape[2] == N_EEG_CHANNELS
    assert X.shape[3] == N_SAMPLES
    assert len(X) == len(y) == len(subjects)

    print("  Shape check       : PASS")
    print("  Label check       : PASS")
    print("  Subject check     : PASS")

    # ========================================================
    # Save processed dataset
    # ========================================================

    output_file = os.path.join(
        OUTPUT_DIR,
        "EEGNet_dataset.npz"
    )

    np.savez_compressed(
        output_file,
        X=X,
        y=y,
        subjects=subjects
    )

    print("\nSaved:")
    print(output_file)

    print("\nPreprocessing completed successfully.")


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()