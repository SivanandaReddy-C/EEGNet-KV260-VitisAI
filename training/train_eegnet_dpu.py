import random
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from eegnet_dpu import EEGNetDPU


# ============================================================
# Configuration
# ============================================================

SEED = 42

BATCH_SIZE = 32
EPOCHS = 100

LEARNING_RATE = 0.001
WEIGHT_DECAY = 1e-4

NUM_CLASSES = 4

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = (
    PROJECT_ROOT
    / "datasets"
    / "processed"
    / "EEGNet_train_test_split.npz"
)

MODEL_DIR = PROJECT_ROOT / "models"

MODEL_FILE = (
    MODEL_DIR
    / "EEGNetDPU_Experiment2_FP32.pth"
)


# ============================================================
# Reproducibility
# ============================================================

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)


# ============================================================
# Header
# ============================================================

print("=" * 70)
print(" EEGNet DPU-COMPATIBLE TRAINING - EXPERIMENT 2")
print("=" * 70)

print("Seed           :", SEED)
print("Batch size     :", BATCH_SIZE)
print("Epochs         :", EPOCHS)
print("Learning rate  :", LEARNING_RATE)
print("Weight decay   :", WEIGHT_DECAY)

print()
print("Dataset        :", DATA_FILE)
print("Model output   :", MODEL_FILE)


# ============================================================
# Device
# ============================================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print()
print("Device         :", device)


# ============================================================
# Load frozen train/test split
# ============================================================

print()
print("Loading frozen train/test split...")

data = np.load(DATA_FILE)

X_train = data["X_train"]
y_train = data["y_train"]

X_test = data["X_test"]
y_test = data["y_test"]

print("X_train shape  :", X_train.shape)
print("y_train shape  :", y_train.shape)
print("X_test shape   :", X_test.shape)
print("y_test shape   :", y_test.shape)


# ============================================================
# Convert to PyTorch tensors
# ============================================================

X_train_tensor = torch.from_numpy(
    X_train.astype(np.float32)
)

y_train_tensor = torch.from_numpy(
    y_train.astype(np.int64)
)

X_test_tensor = torch.from_numpy(
    X_test.astype(np.float32)
)

y_test_tensor = torch.from_numpy(
    y_test.astype(np.int64)
)


# ============================================================
# DataLoaders
# ============================================================

train_dataset = TensorDataset(
    X_train_tensor,
    y_train_tensor
)

test_dataset = TensorDataset(
    X_test_tensor,
    y_test_tensor
)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)


# ============================================================
# Model
# ============================================================

model = EEGNetDPU(
    num_classes=NUM_CLASSES
)

model = model.to(device)

total_params = sum(
    p.numel()
    for p in model.parameters()
)

print()
print("Model          : EEGNetDPU")
print("Parameters     :", total_params)


# ============================================================
# Loss
# ============================================================

criterion = nn.CrossEntropyLoss()


# ============================================================
# Optimizer
# ============================================================

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE,
    weight_decay=WEIGHT_DECAY
)


# ============================================================
# Learning-rate scheduler
# ============================================================

scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=EPOCHS
)


# ============================================================
# Training
# ============================================================

print()
print("=" * 70)
print(" STARTING TRAINING - EXPERIMENT 2")
print("=" * 70)

for epoch in range(EPOCHS):

    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, labels in train_loader:

        inputs = inputs.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(inputs)

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += (
            loss.item() * inputs.size(0)
        )

        predictions = torch.argmax(
            outputs,
            dim=1
        )

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_accuracy = correct / total

    current_lr = optimizer.param_groups[0]["lr"]

    print(
        f"Epoch [{epoch + 1:03d}/{EPOCHS}] "
        f"Loss: {epoch_loss:.4f} "
        f"Train Accuracy: {epoch_accuracy * 100:.2f}% "
        f"LR: {current_lr:.6f}"
    )

    scheduler.step()


# ============================================================
# Final test-set evaluation
# ============================================================

print()
print("=" * 70)
print(" FINAL TEST SET EVALUATION - EXPERIMENT 2")
print("=" * 70)

model.eval()

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


# ============================================================
# Metrics
# ============================================================

accuracy = accuracy_score(
    all_labels,
    all_predictions
)

precision = precision_score(
    all_labels,
    all_predictions,
    average="macro",
    zero_division=0
)

recall = recall_score(
    all_labels,
    all_predictions,
    average="macro",
    zero_division=0
)

f1 = f1_score(
    all_labels,
    all_predictions,
    average="macro",
    zero_division=0
)


print()
print(f"Accuracy   : {accuracy * 100:.2f}%")
print(f"Precision  : {precision * 100:.2f}%")
print(f"Recall     : {recall * 100:.2f}%")
print(f"F1-Score   : {f1 * 100:.2f}%")


# ============================================================
# Save model
# ============================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

torch.save(
    model.state_dict(),
    MODEL_FILE
)

print()
print("Model saved to:")
print(MODEL_FILE)

print()
print("=" * 70)
print(" EXPERIMENT 2 TRAINING COMPLETED")
print("=" * 70)