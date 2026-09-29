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
# Import final model
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


# ============================================================
# Create model
# ============================================================

model = EEGNetDPU(
    num_classes=4
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
# Create Inspector
# ============================================================

inspector = Inspector(
    DPU_ARCH
)


# ============================================================
# Run inspection
# ============================================================

print("=" * 60)
print("VITIS AI DPU INSPECTION")
print("=" * 60)

print(
    "Project root     :",
    PROJECT_ROOT
)

print(
    "DPU architecture :",
    DPU_ARCH
)

print(
    "Input shape      :",
    tuple(dummy_input.shape)
)

print()
print("Starting inspection...")
print()

inspector.inspect(
    model,
    (dummy_input,),
    device=torch.device("cpu")
)

print()
print("Inspection completed.")