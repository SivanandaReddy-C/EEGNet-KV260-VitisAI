
# INT8 Quantization

## 1. Objective

Convert the trained FP32 EEGNet model into an INT8 model using the AMD Vitis AI PyTorch quantization flow.

Deployment flow:

```text
FP32 PyTorch Model
        ↓
Calibration Dataset
        ↓
Vitis AI PyTorch Quantizer
        ↓
INT8 Quantized Model
        ↓
XIR
```

## 2. Calibration Dataset

Calibration data is taken only from the frozen training dataset:
```
datasets/processed/EEGNet_train_test_split.npz
```
The test set is not used for calibration.

A deterministic balanced calibration subset is created:
```
50 samples × 4 classes = 200 samples
```
Input shape:
```
(200, 1, 22, 1000)
```
Configuration:
```
Random seed: 42
Data type: float32
```

## 3. Prepare Calibration Data
Environment
```
WSL Ubuntu.
```
Script
```
quantization/01_prepare_calibration.py
```
Run
```
cd ~/EEGNet-KV260-VitisAI
python quantization/01_prepare_calibration.py
```
Output
```
quantization/EEGNet_calibration.npz
```
The calibration dataset is now ready for Vitis AI INT8 quantization.
---