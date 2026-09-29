import os
import random

import numpy as np
import torch
import torch.nn as nn

from torch.utils.data import TensorDataset, DataLoader

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from eegnet_dpu import EEGNetDPU


# ============================================================
# 1. Reproducibility
# ============================================================

SEED = 42

random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)

if torch.cuda.is_available():

    torch.cuda.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)

    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


# ============================================================
# 2. Configuration
# ============================================================

DATASET_PATH = (
    "datasets/processed/"
    "EEGNet_train_test_split.npz"
)

MODEL_PATH = (
    "models/EEGNetDPU_FP32.pth"
)

BATCH_SIZE = 32
EPOCHS = 100
LEARNING_RATE = 0.001
WEIGHT_DECAY = 1e-4


# ============================================================
# 3. Device
# ============================================================

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


print("=" * 70)
print("Final EEGNet-DPU Training")
print("=" * 70)

print(
    f"Device          : {device}"
)

if device.type == "cuda":

    print(
        "GPU             :",
        torch.cuda.get_device_name(0)
    )

print(
    f"Seed            : {SEED}"
)

print(
    f"Batch size      : {BATCH_SIZE}"
)

print(
    f"Epochs          : {EPOCHS}"
)

print(
    f"Learning rate   : {LEARNING_RATE}"
)

print(
    f"Weight decay    : {WEIGHT_DECAY}"
)

print()


# ============================================================
# 4. Load frozen train/test split
# ============================================================

print("Loading frozen train/test split...")

data = np.load(
    DATASET_PATH
)

X_train = data["X_train"]
y_train = data["y_train"]

X_test = data["X_test"]
y_test = data["y_test"]


print(
    "X_train shape   :",
    X_train.shape
)

print(
    "y_train shape   :",
    y_train.shape
)

print(
    "X_test shape    :",
    X_test.shape
)

print(
    "y_test shape    :",
    y_test.shape
)

print()


# ============================================================
# 5. Convert to PyTorch tensors
# ============================================================

X_train_tensor = torch.from_numpy(
    X_train
).float()

y_train_tensor = torch.from_numpy(
    y_train
).long()

X_test_tensor = torch.from_numpy(
    X_test
).float()

y_test_tensor = torch.from_numpy(
    y_test
).long()


# ============================================================
# 6. Create datasets
# ============================================================

train_dataset = TensorDataset(
    X_train_tensor,
    y_train_tensor
)

test_dataset = TensorDataset(
    X_test_tensor,
    y_test_tensor
)


# ============================================================
# 7. Create DataLoaders
# ============================================================

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0,
    pin_memory=(device.type == "cuda")
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0,
    pin_memory=(device.type == "cuda")
)


# ============================================================
# 8. Create model
# ============================================================

model = EEGNetDPU(
    num_classes=4
).to(device)


total_params = sum(
    p.numel()
    for p in model.parameters()
)

trainable_params = sum(
    p.numel()
    for p in model.parameters()
    if p.requires_grad
)


print("Model")
print("-" * 70)

print(model)

print()

print(
    f"Total parameters     : "
    f"{total_params:,}"
)

print(
    f"Trainable parameters : "
    f"{trainable_params:,}"
)

print()


# ============================================================
# 9. Loss
# ============================================================

criterion = nn.CrossEntropyLoss()


# ============================================================
# 10. Optimizer
# ============================================================

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE,
    weight_decay=WEIGHT_DECAY
)


# ============================================================
# 11. Learning-rate scheduler
# ============================================================

scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=EPOCHS
)


# ============================================================
# 12. Training
# ============================================================

print("=" * 70)
print("Training")
print("=" * 70)


for epoch in range(EPOCHS):

    model.train()

    running_loss = 0.0
    correct = 0
    total = 0


    # --------------------------------------------------------
    # Training batches
    # --------------------------------------------------------

    for inputs, labels in train_loader:

        inputs = inputs.to(
            device,
            non_blocking=True
        )

        labels = labels.to(
            device,
            non_blocking=True
        )


        optimizer.zero_grad()


        # Forward
        outputs = model(inputs)


        # Loss
        loss = criterion(
            outputs,
            labels
        )


        # Backpropagation
        loss.backward()


        # Update weights
        optimizer.step()


        # Statistics
        running_loss += (
            loss.item()
            * inputs.size(0)
        )

        predictions = torch.argmax(
            outputs,
            dim=1
        )

        correct += (
            predictions == labels
        ).sum().item()

        total += labels.size(0)


    # --------------------------------------------------------
    # Epoch training metrics
    # --------------------------------------------------------

    train_loss = (
        running_loss / total
    )

    train_accuracy = (
        correct / total
    )


    # --------------------------------------------------------
    # Scheduler
    # --------------------------------------------------------

    scheduler.step()

    current_lr = (
        optimizer.param_groups[0]["lr"]
    )


    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print(
        f"Epoch [{epoch + 1:3d}/{EPOCHS}] "
        f"Loss: {train_loss:.4f} "
        f"Train Acc: "
        f"{train_accuracy * 100:.2f}% "
        f"LR: {current_lr:.6f}"
    )


# ============================================================
# 13. Final evaluation on frozen test set
# ============================================================

print()
print("=" * 70)
print("Final Test Evaluation")
print("=" * 70)


model.eval()

all_predictions = []
all_labels = []


with torch.no_grad():

    for inputs, labels in test_loader:

        inputs = inputs.to(
            device,
            non_blocking=True
        )

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


all_predictions = np.array(
    all_predictions
)

all_labels = np.array(
    all_labels
)


# ============================================================
# 14. Metrics
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

cm = confusion_matrix(
    all_labels,
    all_predictions
)


print(
    f"Test Accuracy  : "
    f"{accuracy * 100:.2f}%"
)

print(
    f"Test Precision  : "
    f"{precision * 100:.2f}%"
)

print(
    f"Test Recall     : "
    f"{recall * 100:.2f}%"
)

print(
    f"Test F1-score   : "
    f"{f1 * 100:.2f}%"
)

print()

print("Confusion Matrix")
print("-" * 70)

print(cm)

print()


# ============================================================
# 15. Save trained FP32 model
# ============================================================

os.makedirs(
    os.path.dirname(MODEL_PATH),
    exist_ok=True
)


torch.save(
    {
        "model_state_dict":
            model.state_dict(),

        "model_class":
            "EEGNetDPU",

        "num_classes":
            4,

        "input_shape":
            [1, 1, 22, 1000],

        "seed":
            SEED,

        "epochs":
            EPOCHS,

        "batch_size":
            BATCH_SIZE,

        "learning_rate":
            LEARNING_RATE,

        "weight_decay":
            WEIGHT_DECAY,

        "test_accuracy":
            accuracy,

        "test_precision":
            precision,

        "test_recall":
            recall,

        "test_f1":
            f1,
    },
    MODEL_PATH
)


print("=" * 70)
print("Training completed")
print("=" * 70)

print(
    f"Model saved to: {MODEL_PATH}"
)