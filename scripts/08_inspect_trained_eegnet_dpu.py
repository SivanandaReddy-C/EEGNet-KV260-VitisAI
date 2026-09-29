import sys
from pathlib import Path

import torch
from pytorch_nndct.apis import Inspector


# ============================================================
# Project root
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# Import final DPU-compatible model
# ============================================================

from training.eegnet_dpu import EEGNetDPU


# ============================================================
# Configuration
# ============================================================

DPU_ARCH = "DPUCZDX8G_ISA1_B4096"

INPUT_SHAPE = (
    1,
    1,
    22,
    1000
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "EEGNetDPU_FP32.pth"
)


# ============================================================
# Check model file
# ============================================================

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"\nTrained model not found:\n{MODEL_PATH}\n"
    )


# ============================================================
# Create model architecture
# ============================================================

model = EEGNetDPU(
    num_classes=4
)


# ============================================================
# Load trained FP32 weights
# ============================================================

checkpoint = torch.load(
    MODEL_PATH,
    map_location="cpu"
)


# ------------------------------------------------------------
# Support both:
#   1. plain state_dict
#   2. checkpoint containing "model_state_dict"
# ------------------------------------------------------------

if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint:

    state_dict = checkpoint["model_state_dict"]

else:

    state_dict = checkpoint


# ============================================================
# Load weights into model
# ============================================================

model.load_state_dict(
    state_dict
)

model.eval()


# ============================================================
# Create dummy input
# ============================================================

dummy_input = torch.randn(
    INPUT_SHAPE,
    dtype=torch.float32
)


# ============================================================
# Create Vitis AI Inspector
# ============================================================

inspector = Inspector(
    DPU_ARCH
)


# ============================================================
# Display information
# ============================================================

print("=" * 70)
print("VITIS AI DPU INSPECTION - TRAINED FP32 MODEL")
print("=" * 70)

print(
    "Project root     :",
    PROJECT_ROOT
)

print(
    "Model path       :",
    MODEL_PATH
)

print(
    "DPU architecture :",
    DPU_ARCH
)

print(
    "Input shape      :",
    tuple(dummy_input.shape)
)

print(
    "Parameters       :",
    sum(p.numel() for p in model.parameters())
)

print()
print("Trained FP32 model loaded successfully.")
print()
print("Starting DPU inspection...")
print()


# ============================================================
# Run Vitis AI Inspector
# ============================================================

inspector.inspect(
    model,
    (dummy_input,),
    device=torch.device("cpu")
)


# ============================================================
# Completion
# ============================================================

print()
print("=" * 70)
print("Inspection completed.")
print("=" * 70)