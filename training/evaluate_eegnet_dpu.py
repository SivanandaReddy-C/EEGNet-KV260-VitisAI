import sys
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader, TensorDataset

from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report
)

from eegnet_dpu import EEGNetDPU


# ============================================================
# Configuration
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "processed"
    / "EEGNet_train_test_split.npz"
)

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "EEGNetDPU_FP32.pth"
)

BATCH_SIZE = 32
NUM_CLASSES = 4

CLASS_NAMES = [
    "Left Hand",
    "Right Hand",
    "Feet",
    "Tongue"
]


# ============================================================
# Header
# ============================================================

print("=" * 70)
print(" EEGNet DPU-COMPATIBLE MODEL EVALUATION")
print("=" * 70)

print("Dataset :", DATA_FILE)
print("Model   :", MODEL_FILE)


# ============================================================
# Device
# ============================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device  :", device)


# ============================================================
# Load frozen test set
# ============================================================

print()
print("Loading frozen test set...")

data = np.load(DATA_FILE)

X_test = data["X_test"]
y_test = data["y_test"]

print("X_test shape :", X_test.shape)
print("y_test shape :", y_test.shape)


# ============================================================
# Convert to tensors
# ============================================================

X_test_tensor = torch.from_numpy(
    X_test.astype(np.float32)
)

y_test_tensor = torch.from_numpy(
    y_test.astype(np.int64)
)


# ============================================================
# DataLoader
# ============================================================

test_dataset = TensorDataset(
    X_test_tensor,
    y_test_tensor
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)


# ============================================================
# Load model
# ============================================================

print()
print("Loading trained model...")

model = EEGNetDPU(
    num_classes=NUM_CLASSES
)

model.load_state_dict(
    torch.load(
        MODEL_FILE,
        map_location=device
    )
)

model = model.to(device)
model.eval()

print("Model loaded successfully.")


# ============================================================
# Inference
# ============================================================

print()
print("Running test-set inference...")

all_predictions = []
all_labels = []

with torch.no_grad():

    for inputs, labels in test_loader:

        inputs = inputs.to(device)

        outputs = model(inputs)

        predictions = torch.argmax(
            outputs,
            dim=1
        )

        all_predictions.extend(
            predictions.cpu().numpy()
        )

        all_labels.extend(
            labels.numpy()
        )


all_labels = np.array(all_labels)
all_predictions = np.array(all_predictions)


# ============================================================
# Overall accuracy
# ============================================================

accuracy = accuracy_score(
    all_labels,
    all_predictions
)

print()
print("=" * 70)
print(" OVERALL PERFORMANCE")
print("=" * 70)

print(
    f"Accuracy : {accuracy * 100:.2f}%"
)


# ============================================================
# Confusion matrix
# ============================================================

cm = confusion_matrix(
    all_labels,
    all_predictions,
    labels=np.arange(NUM_CLASSES)
)

print()
print("=" * 70)
print(" CONFUSION MATRIX")
print("=" * 70)

print()
print("Rows    = Actual class")
print("Columns = Predicted class")
print()

print(
    f"{'':15s}"
    f"{'Left':>10s}"
    f"{'Right':>10s}"
    f"{'Feet':>10s}"
    f"{'Tongue':>10s}"
)

for i, class_name in enumerate(CLASS_NAMES):

    print(
        f"{class_name:15s}"
        f"{cm[i, 0]:10d}"
        f"{cm[i, 1]:10d}"
        f"{cm[i, 2]:10d}"
        f"{cm[i, 3]:10d}"
    )


# ============================================================
# Per-class metrics
# ============================================================

precision, recall, f1, support = (
    precision_recall_fscore_support(
        all_labels,
        all_predictions,
        labels=np.arange(NUM_CLASSES),
        zero_division=0
    )
)

print()
print("=" * 70)
print(" PER-CLASS PERFORMANCE")
print("=" * 70)

print()
print(
    f"{'Class':15s}"
    f"{'Precision':>12s}"
    f"{'Recall':>12s}"
    f"{'F1':>12s}"
    f"{'Support':>10s}"
)

for i, class_name in enumerate(CLASS_NAMES):

    print(
        f"{class_name:15s}"
        f"{precision[i] * 100:11.2f}%"
        f"{recall[i] * 100:11.2f}%"
        f"{f1[i] * 100:11.2f}%"
        f"{support[i]:10d}"
    )


# ============================================================
# Full classification report
# ============================================================

print()
print("=" * 70)
print(" CLASSIFICATION REPORT")
print("=" * 70)

print()

print(
    classification_report(
        all_labels,
        all_predictions,
        labels=np.arange(NUM_CLASSES),
        target_names=CLASS_NAMES,
        digits=4,
        zero_division=0
    )
)


# ============================================================
# Prediction distribution
# ============================================================

print("=" * 70)
print(" PREDICTION DISTRIBUTION")
print("=" * 70)

for i, class_name in enumerate(CLASS_NAMES):

    count = np.sum(
        all_predictions == i
    )

    percentage = (
        count / len(all_predictions)
    ) * 100

    print(
        f"{class_name:15s}: "
        f"{count:4d} "
        f"({percentage:.2f}%)"
    )


print()
print("=" * 70)
print(" EVALUATION COMPLETED")
print("=" * 70)