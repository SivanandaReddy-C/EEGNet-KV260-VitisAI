import os
import numpy as np
from sklearn.model_selection import train_test_split


# ============================================================
# Configuration
# ============================================================

INPUT_FILE = "datasets/processed/EEGNet_dataset.npz"

OUTPUT_FILE = (
    "datasets/processed/EEGNet_train_test_split.npz"
)

RANDOM_STATE = 42
TEST_SIZE = 0.20

EXPECTED_SHAPE = (2592, 1, 22, 1000)
NUM_CLASSES = 4


# ============================================================
# Load dataset
# ============================================================

print("=" * 60)
print(" EEG DATASET VALIDATION")
print("=" * 60)

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(
        f"Dataset not found: {INPUT_FILE}"
    )

data = np.load(INPUT_FILE)

X = data["X"]
y = data["y"]
subjects = data["subjects"]

print("\nLoaded dataset:")
print("X shape       :", X.shape)
print("y shape       :", y.shape)
print("subjects shape:", subjects.shape)


# ============================================================
# 1. Shape validation
# ============================================================

print("\n--- Shape Validation ---")

assert X.shape == EXPECTED_SHAPE, (
    f"Unexpected X shape: {X.shape}"
)

assert y.shape == (EXPECTED_SHAPE[0],), (
    f"Unexpected y shape: {y.shape}"
)

assert subjects.shape == (EXPECTED_SHAPE[0],), (
    f"Unexpected subjects shape: {subjects.shape}"
)

print("Shape validation: PASS")


# ============================================================
# 2. NaN / Inf validation
# ============================================================

print("\n--- Numerical Validation ---")

nan_count = np.isnan(X).sum()
inf_count = np.isinf(X).sum()

print("NaN values:", nan_count)
print("Inf values:", inf_count)

assert nan_count == 0, "NaN values detected"
assert inf_count == 0, "Inf values detected"

print("NaN/Inf validation: PASS")


# ============================================================
# 3. Label validation
# ============================================================

print("\n--- Label Validation ---")

unique_labels = np.unique(y)

print("Labels found:", unique_labels)

assert np.array_equal(
    unique_labels,
    np.arange(NUM_CLASSES)
), "Unexpected class labels"

print("Label validation: PASS")


# ============================================================
# 4. Class distribution
# ============================================================

print("\n--- Class Distribution ---")

for label in range(NUM_CLASSES):

    count = np.sum(y == label)

    print(
        f"Class {label}: {count}"
    )


# ============================================================
# 5. Subject distribution
# ============================================================

print("\n--- Subject Distribution ---")

for subject in range(1, 10):

    count = np.sum(subjects == subject)

    print(
        f"A{subject:02d}T: {count}"
    )


# ============================================================
# 6. Normalization validation
#
# Every trial/channel should have approximately:
# mean = 0
# std  = 1
# ============================================================

print("\n--- Normalization Validation ---")

# X shape:
# [N, 1, 22, 1000]

X_eeg = X[:, 0, :, :]

trial_channel_means = X_eeg.mean(axis=2)
trial_channel_stds = X_eeg.std(axis=2)

max_abs_mean = np.max(
    np.abs(trial_channel_means)
)

max_std_error = np.max(
    np.abs(trial_channel_stds - 1.0)
)

print(
    "Maximum absolute mean:",
    max_abs_mean
)

print(
    "Maximum std error:",
    max_std_error
)

assert max_abs_mean < 1e-5, (
    "Normalization mean validation failed"
)

assert max_std_error < 1e-5, (
    "Normalization std validation failed"
)

print("Normalization validation: PASS")


# ============================================================
# 7. Dataset statistics
# ============================================================

print("\n--- Dataset Statistics ---")

print("Minimum:", X.min())
print("Maximum:", X.max())
print("Mean   :", X.mean())
print("Std    :", X.std())


# ============================================================
# 8. Create ONE reproducible train/test split
# ============================================================

print("\n--- Creating Train/Test Split ---")

indices = np.arange(len(y))

train_idx, test_idx = train_test_split(
    indices,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y
)

X_train = X[train_idx]
X_test = X[test_idx]

y_train = y[train_idx]
y_test = y[test_idx]

subjects_train = subjects[train_idx]
subjects_test = subjects[test_idx]


# ============================================================
# 9. Split validation
# ============================================================

print("\nTrain/Test sizes:")

print("X_train:", X_train.shape)
print("X_test :", X_test.shape)

print("y_train:", y_train.shape)
print("y_test :", y_test.shape)


print("\nTraining class distribution:")

for label in range(NUM_CLASSES):

    count = np.sum(y_train == label)

    print(
        f"Class {label}: {count}"
    )


print("\nTesting class distribution:")

for label in range(NUM_CLASSES):

    count = np.sum(y_test == label)

    print(
        f"Class {label}: {count}"
    )


# ============================================================
# 10. Save split
# ============================================================

np.savez_compressed(
    OUTPUT_FILE,

    X_train=X_train,
    y_train=y_train,
    subjects_train=subjects_train,

    X_test=X_test,
    y_test=y_test,
    subjects_test=subjects_test,

    train_idx=train_idx,
    test_idx=test_idx,

    random_state=RANDOM_STATE,
    test_size=TEST_SIZE
)


# ============================================================
# Final result
# ============================================================

print("\n" + "=" * 60)
print(" DATASET SPLIT COMPLETED")
print("=" * 60)

print("\nSaved:")
print(OUTPUT_FILE)

print("\nSplit configuration:")
print("test_size    :", TEST_SIZE)
print("random_state :", RANDOM_STATE)
print("stratify     : y")

print("\nDataset is now ready for EEGNet development.")