# Vitis AI Setup

## 1. Objective

This document records the setup and verification of the AMD Vitis AI development environment for the EEGNet deployment project.

The Vitis AI environment will be used on the development workstation for:

- Model quantization
- DPU compatibility analysis
- DPU compilation
- Generation of deployment artifacts

The KV260 will be used as the target inference platform.

The overall development workflow is:

```text
Trained EEGNet Model
        ↓
Vitis AI Quantization
        ↓
Quantized Model
        ↓
DPU Compilation
        ↓
Compiled Model
        ↓
Transfer to KV260
        ↓
DPU Inference
        ↓
Performance Benchmarking
```

The Vitis AI development environment will be isolated using Docker on the WSL2 development system.

## 2. Development and Target Architecture

The project uses two separate systems.

### 2.1 Development System

The development system is the Windows host PC running:
```
Windows
    ↓
WSL2
    ↓
Ubuntu 22.04
    ↓
Docker Desktop
    ↓
Vitis AI Docker Container
```
The development system will perform model preparation, quantization, and compilation.

### 2.2 Target System

The target system is:
```
AMD Kria KV260 Vision AI Starter Kit
    ↓
Ubuntu 22.04
    ↓
XRT 2.13.0
    ↓
K26 DFX 2RP
    ↓
B3136 DPU
```
The KV260 will execute the compiled model using the DPU.

## 3. Vitis AI Version Selection

The Vitis AI version must be compatible with the DPU configuration and KV260 platform used in this project.

The KV260 2022.1 documentation identifies the integrated DPU as a B3136 configuration and specifies Vitis AI 2.5.0 for model customization.

Therefore, this project will use:
```
Vitis AI Version: 2.5.0
Target Platform:  KV260
Target DPU:       B3136
Platform Release: 2022.1
```
A matching Vitis AI Docker image will be used rather than installing Vitis AI tools directly into the WSL Ubuntu environment.

## 4. Docker-Based Development Environment

Docker Desktop is installed on the Windows host and integrated with the WSL2 Ubuntu environment.

The Docker environment was verified from WSL.

### 4.1 Docker Version

The Docker CLI was verified using:
```bash
docker --version
```
The installed version is:
```
Docker version 29.7.2
```
### 4.2 Docker Engine Verification

The Docker Engine was verified using:
```bash
docker info
```
The Docker server reported:
```
Server Version: 29.7.2
Operating System: Docker Desktop
OSType: linux
Architecture: x86_64
CPUs: 28
Total Memory: approximately 31.18 GiB
```
Therefore, Docker is operational from within the WSL2 Ubuntu environment.

### 4.3 Initial Docker Image Verification
The locally available Docker images were checked using:
```bash
docker images
```
The initial environment contained:
```
hello-world:latest
```
No Vitis AI image has been downloaded at this stage.

## 5. Vitis AI Installation Strategy

Vitis AI will not be installed directly into the WSL Ubuntu environment.

Instead, the project will use the corresponding pre-built Vitis AI Docker image.

This approach provides:

- A reproducible Vitis AI software environment
- Isolation from the WSL host Python environment
- Version consistency between Vitis AI tools
- Easier recovery and recreation of the development environment
- Separation between host development tools and Vitis AI dependencies

The Vitis AI Docker image will be selected according to the Vitis AI 2.5.0 release.

## 6. Version Compatibility Baseline

The following configuration is treated as the project baseline:
| Component               | Version / Configuration              |
| ----------------------- | ------------------------------------ |
| Target board            | AMD Kria KV260 Vision AI Starter Kit |
| Target OS               | Ubuntu 22.04 LTS                     |
| Platform release        | 2022.1                               |
| XRT                     | 2.13.0                               |
| DFX firmware            | K26 DFX 2RP                          |
| DPU configuration       | B3136                                |
| Vitis AI                | 2.5.0                                |
| Development environment | WSL2 + Docker Desktop                |
| Docker                  | 29.7.2                               |

This compatibility baseline will be maintained throughout the model quantization and compilation stages.

The version choice is not arbitrary: AMD's KV260 2022.1 documentation explicitly states **Vitis AI 2.5.0** and **B3136** for these KV260 designs.

## 7. Vitis AI 2.5 Repository Setup

The Vitis AI source repository was cloned separately from the EEGNet-KV260-VitisAI project repository.

The purpose of keeping the Vitis AI repository separate is to avoid adding the complete Vitis AI source tree to the project repository.

The Vitis AI repository was cloned using:

```bash
cd ~/projects

git clone --branch v2.5 --recursive \
https://github.com/Xilinx/Vitis-AI.git \
Vitis-AI-2.5
```
The repository is located at:
```
~/projects/Vitis-AI-2.5
```
### 7.1 Vitis AI Release Verification

The Vitis AI repository was checked using:
```bash
cd ~/projects/Vitis-AI-2.5

git branch --show-current
git status
git describe --tags --exact-match
```
The exact release was verified as:
```
v2.5
```
The working tree was clean.

The repository is in a detached HEAD state because the exact release tag `v2.5` was checked out.

This is acceptable and desirable for reproducibility because the project is intentionally pinned to the Vitis AI 2.5 release.

## 8. Vitis AI 2.5 Docker Image

The Vitis AI 2.5 CPU Docker image was selected for the development environment.

The image used is:
```
xilinx/vitis-ai-cpu:2.5.0
```
The image was downloaded using:
```bash
docker pull xilinx/vitis-ai-cpu:2.5.0
```
The download completed successfully.

### 8.1 Docker Image Verification

The locally available image was checked using:
```bash
docker images xilinx/vitis-ai-cpu
```
The image was reported as:
```
xilinx/vitis-ai-cpu:2.5.0
```
with an image ID beginning with:
```
eaa85efb0692
```
The reported content size was approximately:
```
6.4 GB
```
The Docker image was further verified using:
```bash
docker inspect xilinx/vitis-ai-cpu:2.5.0 --format '{{.Id}}'
```
The image ID/digest was:
```
sha256:eaa85efb06924995ebdb973546e7f69169b003b8cc525764bd9524ad554dddbe
```
This exact image will be used for the Vitis AI development workflow.

## 9. Vitis AI Docker Container Launch

The Vitis AI container was launched from the WSL2 Ubuntu environment.

The EEGNet project repository was mounted into the container so that project files can be accessed directly without copying them into the container.

The container was started using:
```bash
cd ~/projects/EEGNet-KV260-VitisAI

docker run --rm -it \
  -v ~/projects/EEGNet-KV260-VitisAI:/workspace/EEGNet-KV260-VitisAI \
  xilinx/vitis-ai-cpu:2.5.0
  ```
The container started successfully.

The Vitis AI startup information reported:
```
Docker Image Version: 2.5.0.1260 (CPU)
Vitis AI Git Hash: 502703c
Build Date: 2022-06-12
```
The container prompt was successfully reached:
```
Vitis-AI /
```
The container displayed a warning that it was running as root. This warning does not indicate a failure of the Vitis AI environment.

## 10. PyTorch Environment Verification

The Vitis AI Docker container provides multiple framework environments.

For this project, the PyTorch environment is required because the EEGNet model will be developed using PyTorch.

The PyTorch environment was activated using:
```bash
conda activate vitis-ai-pytorch
```
The active environment was verified through the shell prompt:
```
(vitis-ai-pytorch)
```

### 10.1 Python Version

Python was checked using:
```bash
python --version
```
The installed version is:
```
Python 3.7.12
```
### 10.2 PyTorch Version
PyTorch was checked using:
```bash
python -c "import torch; print(torch.__version__)"
```
The installed version is:
```
1.10.1
```
### 10.3 CUDA Availability

CUDA availability was checked using:
```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```
The result was:
```
CUDA available: False
```
This is expected because the selected Vitis AI Docker image is the CPU image.

No modification or upgrade of the installed PyTorch version was performed.

## 11. Vitis AI PyTorch Quantization Environment Verification

The Vitis AI PyTorch quantization framework was verified using the Python package interface.

The `pytorch_nndct` package was tested using:
```bash
python -c "import pytorch_nndct; print('pytorch_nndct imported successfully'); print(pytorch_nndct.__file__)"
```
The result confirmed:
```
pytorch_nndct imported successfully
```
The package is installed under:
```
/opt/vitis_ai/conda/envs/vitis-ai-pytorch/lib/python3.7/site-packages/pytorch_nndct/
```
### 11.1 PyTorch Quantizer API Verification

The Vitis AI PyTorch quantizer API was verified using:
```bash
python -c "from pytorch_nndct.apis import torch_quantizer; print('torch_quantizer imported successfully'); print(torch_quantizer)"
```
The result confirmed:
```
torch_quantizer imported successfully
<class 'pytorch_nndct.apis.torch_quantizer'>
```
Therefore, the Vitis AI 2.5 PyTorch quantization API is available in the container.

No additional quantization package was installed.

## 12. EEGNet Project Repository Mount Verification

The EEGNet-KV260-VitisAI repository was mounted into the Vitis AI Docker container using:
```
/workspace/EEGNet-KV260-VitisAI
```
The repository was verified using:
```bash
ls -la /workspace/EEGNet-KV260-VitisAI
```
The repository directories were visible from inside the container, including:
```
benchmarking/
compilation/
datasets/
deployment/
docs/
examples/
images/
models/
quantization/
scripts/
setup/
training/
```
This confirms that the WSL2 project repository is accessible from inside the Vitis AI Docker container.

## 13. Current Project Model and Training Directories

The contents of the model and training directories were inspected using:
```bash
find /workspace/EEGNet-KV260-VitisAI/models \
-maxdepth 2 -type f -printf '%p\n'
```
and:
```bash
find /workspace/EEGNet-KV260-VitisAI/training \
-maxdepth 2 -type f -printf '%p\n'
```
At this stage, the directories contain only their .gitkeep files:
```
models/
└── .gitkeep

training/
└── .gitkeep
```
This is expected because the EEGNet development and training stage has not yet started.

No EEGNet model has been copied into the repository.

No EEGNet model has been quantized.

No ONNX model has been generated as part of this project yet.

No Vitis AI compilation has been performed yet.

## 14. Current Status

The Vitis AI development environment is now successfully configured and verified.

The current verified configuration is:
| Component               | Verified Configuration                                                    | Status   |
| ----------------------- | ------------------------------------------------------------------------- | -------- |
| Development OS          | Windows + WSL2 Ubuntu 22.04                                               | ✅        |
| Docker                  | 29.7.2                                                                    | ✅        |
| Vitis AI repository     | v2.5                                                                      | ✅        |
| Vitis AI Docker image   | 2.5.0.1260 CPU                                                            | ✅        |
| Docker image digest     | `sha256:eaa85efb06924995ebdb973546e7f69169b003b8cc525764bd9524ad554dddbe` | ✅        |
| Python                  | 3.7.12                                                                    | ✅        |
| PyTorch                 | 1.10.1                                                                    | ✅        |
| CUDA                    | Not available                                                             | Expected |
| `pytorch_nndct`         | Installed                                                                 | ✅        |
| `torch_quantizer`       | Import successful                                                         | ✅        |
| EEGNet repository mount | Working                                                                   | ✅        |
| EEGNet model            | Not created yet                                                           | ⏳        |
| EEGNet training         | Not started                                                               | ⏳        |
| Quantization            | Not started                                                               | ⏳        |
| DPU compilation         | Not started                                                               | ⏳        |
| KV260 inference         | Not started                                                               | ⏳        |

## 15. Environment Freeze Point

At this stage, the Vitis AI development environment is considered ready for the EEGNet development stage.

The following environment versions will be treated as the baseline:
```
Vitis AI Repository : v2.5
Vitis AI Image      : 2.5.0.1260 (CPU)
Python              : 3.7.12
PyTorch             : 1.10.1
PyTorch NNDCT       : Vitis AI 2.5
Docker              : 29.7.2

Target:
KV260
Ubuntu 22.04.4 LTS
XRT 2.13.0
K26 DFX 2RP
B3136 DPU
```
No package upgrades or environment modifications should be performed without documenting and evaluating their impact on Vitis AI 2.5 compatibility.

The next stage will begin the EEGNet development workflow. No EEGNet-specific work has been performed in this setup stage.