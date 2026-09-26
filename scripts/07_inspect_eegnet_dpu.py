import sys
from pathlib import Path

import torch
from pytorch_nndct.apis import Inspector


# ============================================================
# Add project root to Python path
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


# ============================================================
# Import EEGNet
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
# Create dummy input tensor
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
# Run inspection
# ============================================================

print("=" * 60)
print(" VITIS AI DPU INSPECTION")
print("=" * 60)

print("Project root     :", PROJECT_ROOT)
print("DPU architecture :", DPU_ARCH)
print("Input shape      :", tuple(dummy_input.shape))

print("\nStarting inspection...\n")

inspector.inspect(
    model,
    (dummy_input,),
    device=torch.device("cpu")
)

print("\nInspection completed.")