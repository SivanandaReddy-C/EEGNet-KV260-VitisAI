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

The version choice is not arbitrary: AMD's KV260 2022.1 documentation explicitly states **Vitis AI 2.5.0** and **B3136** for these KV260 designs. :contentReference[oaicite:2]{index=2}
