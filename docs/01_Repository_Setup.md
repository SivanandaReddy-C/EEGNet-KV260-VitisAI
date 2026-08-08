# Repository Setup

## 1. Objective

Create and configure the GitHub repository that will be used to develop, document, and maintain the complete EEGNet deployment workflow on the AMD Kria KV260 using Vitis AI.

The repository will serve two purposes:

1. Store the source code, models, scripts, configuration files, and other project artifacts.
2. Maintain a continuous record of the steps followed during the project so that the complete workflow can later be reproduced for training and teaching.

---

## 2. Project Goal

The main goal of this project is to understand and implement the complete end-to-end Vitis AI workflow by deploying an EEGNet model trained on the BCI Competition IV Dataset 2a to the AMD Kria KV260.

The intended workflow is:

```text
BCI Competition IV Dataset 2a
            ↓
      Data Preparation
            ↓
       EEGNet Training
            ↓
      PyTorch Model
            ↓
         ONNX
            ↓
       Quantization
            ↓
    Vitis AI Compilation
            ↓
         .xmodel
            ↓
       Kria KV260
            ↓
    DPU-based Inference
            ↓
       Benchmarking
```
---
## 3. Repository Information
- Repository Name: EEGNet-KV260-VitisAI

- Repository Purpose:
The repository contains the implementation and documentation required to understand the end-to-end deployment of EEGNet on the AMD Kria KV260 using Vitis AI.

## 4. Initial Repository Structure

The initial repository structure is:

```text
EEGNet-KV260-VitisAI/
│
├── benchmarking/
├── compilation/
├── datasets/
├── deployment/
├── docs/
├── examples/
├── images/
├── models/
├── quantization/
├── scripts/
├── setup/
├── training/
│
├── .gitignore
├── LICENSE
└── README.md
```

Directory Description:
| Directory       | Purpose                                                        |
| --------------- | -------------------------------------------------------------- |
| `benchmarking/` | Scripts and results for measuring model performance            |
| `compilation/`  | Vitis AI compilation scripts and compilation-related artifacts |
| `datasets/`     | Dataset preparation scripts and dataset-related files          |
| `deployment/`   | KV260 deployment and inference files                           |
| `docs/`         | Project documentation and step-by-step learning records        |
| `examples/`     | Small examples used to understand the Vitis AI workflow        |
| `images/`       | Screenshots, diagrams, and other images used in documentation  |
| `models/`       | Trained, exported, quantized, and compiled model artifacts     |
| `quantization/` | Quantization scripts and related files                         |
| `scripts/`      | General-purpose utility scripts                                |
| `setup/`        | Environment setup and installation-related files               |
| `training/`     | EEGNet training and model-development scripts                  |

## 5. Development Environment

The project will use the following development environment:

Windows 11 as the host operating system
Visual Studio Code as the primary development environment.

WSL2 as the Linux development environment.

Ubuntu 22.04 LTS as the Linux distribution.

Git for version control.

GitHub as the remote repository.

Docker for containerized development environments.

Vitis AI for AI model deployment and acceleration on the Kria KV260

The individual components will be installed and configured in subsequent stages of the project.
 
## 6. Host PC

The initial host PC configuration is:
| Component               | Configuration         |
| ----------------------- | --------------------- |
| Operating System        | Windows 11 Enterprise |
| Windows Version         | 25H2                  |
| OS Build                | 26200.8655            |
| Processor               | Intel Core i7-14700   |
| RAM                     | 64 GB                 |
| Hardware Virtualization | Enabled               |

## 7. Creating the Local Working Copy

The GitHub repository was cloned to the local PC so that the project files can be edited using Visual Studio Code.

Local Workspace:
D:\KV260_Workspace

Local Repository:
D:\KV260_Workspace\EEGNet-KV260-VitisAI

Clone Command:
The repository was cloned using:

git clone <repository-url>


Replace <repository-url> with the URL of the GitHub repository.


## 8. Verify the Local Repository

After cloning the repository, the repository directory was opened:
cd D:\KV260_Workspace\EEGNet-KV260-VitisAI

The Git repository was then verified using:
git status