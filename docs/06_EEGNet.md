## Step 1 — Create the EEGNet Working Area
### 1. Objective

Create the basic directories required for the EEGNet-specific workflow.

At this stage:

- No EEG dataset has been downloaded.
- No EEG preprocessing has been performed.
- No MNE environment has been created.
- No EEGNet model has been created.

This step only establishes the working directories.

### 2. Environment

Platform: WSL Ubuntu 22.04
Repository: EEGNet-KV260-VitisAI

### 3. Commands

Navigate to the project repository:
```bash
cd ~/projects/EEGNet-KV260-VitisAI
```
Create the EEG dataset and script directories:
```bash
mkdir -p datasets
mkdir -p scripts
```
Verify:
```bash
ls -ld datasets scripts
```
### 4. Expected Result

The following directories should exist:
```
EEGNet-KV260-VitisAI/
├── datasets/
└── scripts/
```

## Step 2 — Obtain the EEG Dataset
### 1. Objective

Obtain the BCI Competition IV Dataset 2a, which will be used for the EEGNet development and deployment workflow.

### 2. Dataset

Dataset: BCI Competition IV — Dataset 2a

Dataset archive:
```
BCICIV_2a_gdf.zip
```
The dataset is obtained from the official BCI Competition IV website.

Official download page:
```
https://www.bbci.de/competition/iv/download/?utm_source=chatgpt.com
```
### 3. Download Procedure
- Open the official BCI Competition IV download page.
- Locate Dataset 2a.
- Download:
```
BCICIV_2a_gdf.zip
```
- Save the ZIP file in the Windows Downloads directory.
### 4. Expected Result

The downloaded file should be available as:
```
BCICIV_2a_gdf.zip
```
in the Windows Downloads folder.

## Step 3 — Transfer the Dataset to the WSL Project
Goal

Copy the downloaded `BCICIV_2a_gdf.zip` from your Windows Downloads folder into the project's `datasets/` directory.

Where to run

WSL Ubuntu 22.04 terminal

### 1. Verify the downloaded file

Run:
```
ls -lh /mnt/c/Users/MIT/Downloads/BCICIV_2a_gdf.zip
```
You should see the ZIP file and its size.

### 2. Copy it into the project
```bash
cd ~/projects/EEGNet-KV260-VitisAI
cp /mnt/c/Users/MIT/Downloads/BCICIV_2a_gdf.zip datasets/
```

### 3. Verify the copy
```bash
ls -lh datasets/BCICIV_2a_gdf.zip
```
### 4. Expected result
``` EEGNet-KV260-VitisAI/
└── datasets/
    └── BCICIV_2a_gdf.zip
```
## Step 4 — Extract the EEG Dataset
Goal:

Extract BCICIV_2a_gdf.zip into the project so that the individual GDF files become available for inspection.

Where to run:
```
WSL Ubuntu 22.04 terminal
```
### 1. Go to the project
```bash
cd ~/projects/EEGNet-KV260-VitisAI
```

### 2. Extract the ZIP
Run:
```bash
unzip datasets/BCICIV_2a_gdf.zip -d datasets/BCICIV_2a
```
If unzip is not installed, install it first:
```bash
sudo apt update
sudo apt install -y unzip
```
Then run the extraction command again.

### 3. Check the extracted files
```bash
ls -lh datasets/BCICIV_2a
```
### Expected result

You should see GDF files similar to:
```
A01E.gdf
A01T.gdf
A02E.gdf
A02T.gdf
...
A09E.gdf
A09T.gdf
```
## Step 5 — Inspect the Dataset Structure
Goal

Before installing preprocessing tools or writing preprocessing code, verify that the extracted dataset contains the expected GDF files.

Where to run
```
WSL Ubuntu 22.04 terminal
```
### 1. Go to the project
```bash
cd ~/projects/EEGNet-KV260-VitisAI
```
### 2. Count the GDF files
```bash
find datasets/BCICIV_2a -maxdepth 1 -type f -name "*.gdf" | wc -l
```
### Expected result
```
18
```
### 3. List the files
```bash
find datasets/BCICIV_2a -maxdepth 1 -type f -name "*.gdf" -printf "%f\n" | sort
```
You should see:
```
A01E.gdf
A01T.gdf
A02E.gdf
A02T.gdf
A03E.gdf
A03T.gdf
A04E.gdf
A04T.gdf
A05E.gdf
A05T.gdf
A06E.gdf
A06T.gdf
A07E.gdf
A07T.gdf
A08E.gdf
A08T.gdf
A09E.gdf
A09T.gdf
```
### 4. Check the total size
```bash
du -sh datasets/BCICIV_2a
```
This gives us a quick confirmation that the extraction completed properly.

## Step 6 — Set Up the EEG Data Processing Environment
Goal

Create a dedicated Python environment for EEG data inspection and preprocessing.

We will use MNE-Python to read and process the GDF files.

Where to run
```
WSL Ubuntu 22.04 terminal
```
### 1. Go to the project
```bash
cd ~/projects/EEGNet-KV260-VitisAI
```
### 2. Check Python
```bash
python3 --version
```
We will use the system Python available in your WSL environment.

### 3. Install Python virtual-environment support
```bash
sudo apt update
sudo apt install -y python3-venv
```
### 4. Create the EEG environment
```bash
python3 -m venv .venv/eeg-data
```
### 5. Activate it
```bash
source .venv/eeg-data/bin/activate
```
Your terminal should now show something similar to:
```
(eeg-data) user@machine:~/projects/EEGNet-KV260-VitisAI$
```
### 6. Upgrade pip
```bash
pip install --upgrade pip
```
### 7. Install MNE and NumPy

For reproducibility, install the versions we will use for this project:
```bash
pip install mne==1.6.1 numpy==1.26.4
```
### 8. Verify the installation
```bash
python -c "import mne, numpy; print('MNE:', mne.__version__); print('NumPy:', numpy.__version__)"
```
Expected:
```
MNE: 1.6.1
NumPy: 1.26.4
```
## Step 7 — Inspect the First EEG Recording
Goal

Read one raw GDF recording with MNE and verify its basic structure before designing the preprocessing pipeline.

We will inspect A01T.gdf only. No filtering, epoching, normalization, or data modification yet.

Where to run
```
WSL Ubuntu 22.04 terminal, with the eeg-data environment activated.
```
### 1. Verify the environment
```bash
source ~/projects/EEGNet-KV260-VitisAI/.venv/eeg-data/bin/activate
cd ~/projects/EEGNet-KV260-VitisAI
```
### 2. Create the inspection script
```bash
nano scripts/01_inspect_gdf.py
```
Paste the code
```
import mne

FILE = "datasets/BCICIV_2a/A01T.gdf"

print("Reading:", FILE)

raw = mne.io.read_raw_gdf(
    FILE,
    preload=False,
    verbose=False
)

print("\n--- Recording Information ---")
print("Channels      :", len(raw.ch_names))
print("Sampling rate :", raw.info["sfreq"], "Hz")
print("Duration      :", raw.times[-1], "seconds")

print("\n--- Channels ---")
for i, ch in enumerate(raw.ch_names):
    print(f"{i:2d}: {ch}")

print("\n--- Annotations ---")
print("Number of annotations:", len(raw.annotations))

for i, annotation in enumerate(raw.annotations[:20]):
    print(
        f"{i:2d}: "
        f"onset={annotation['onset']:.3f}s, "
        f"duration={annotation['duration']:.3f}s, "
        f"description={annotation['description']}"
    )
```
Save and exit.

### 3. Run it
```bash
python scripts/01_inspect_gdf.py
```
### 4. Observed Recording Structure

The inspection produced the following results:
| Property           |   Observed value |
| ------------------ | ---------------: |
| Total channels     |               25 |
| Sampling rate      |           250 Hz |
| Recording duration | 2690.108 seconds |
| Total annotations  |              603 |

## Step 8 — Analyze the EEG Event Codes
Goal

Determine exactly which event codes correspond to the motor-imagery trials and verify their distribution in A01T.gdf.

This is important before we define the preprocessing and labeling strategy.

Where to run
```
WSL Ubuntu 22.04, with (eeg-data) activated.
```
### 1. Create the event-analysis script

From the project directory:
```bash
cd ~/projects/EEGNet-KV260-VitisAI
nano scripts/02_analyze_events.py
```

### 2. Run the script
```bash
python scripts/02_analyze_events.py
```

### 3. Recording Analyzed
```
datasets/BCICIV_2a/A01T.gdf
```

### 4. Analysis Method

The GDF annotations were converted into MNE events using:
```bash
events, event_id = mne.events_from_annotations(
    raw,
    verbose=False
)
```
The event codes were then counted to determine their distribution.
### 5. Observed Event Distribution

The following event codes were found:
| Event code |  Count |
| ---------: | -----: |
|       1023 |     15 |
|       1072 |      1 |
|        276 |      1 |
|        277 |      1 |
|      32766 |      9 |
|        768 |    288 |
|    **769** | **72** |
|    **770** | **72** |
|    **771** | **72** |
|    **772** | **72** |
Total motor-imagery trials:
```
72 + 72 + 72 + 72 = 288 trials
```
### 6. Outcome

This step establishes the actual motor-imagery event mapping and class distribution for A01T.gdf.

The preprocessing stage can now use event codes 769–772 as the basis for identifying motor-imagery trials.

## Step 9 — Analyze Trial Timing and Cue Structure
Goal

Before deciding the EEG epoch window, verify the timing relationship between trial-start events (768) and motor-imagery cue events (769–772).

This will tell us exactly where the motor-imagery segment begins and how much signal is available after the cue.

Where to run
```
WSL Ubuntu 22.04, with (eeg-data) activated.
```
### 1. Create the trial-timing analysis script
```bash
cd ~/projects/EEGNet-KV260-VitisAI
nano scripts/03_analyze_trial_timing.py
```

### 2. Run the analysis
```bash
python scripts/03_analyze_trial_timing.py
```

## Step 11 — Verify Exact Sample-Level Timing
Goal

Convert the trial timing from seconds into exact EEG sample indices and verify how many samples are available in the motor-imagery period.

This is important because EEGNet requires a fixed number of samples per trial.

Where to run
```
WSL Ubuntu 22.04, with (eeg-data) activated.
```

### 1. Create the script
```bash
cd ~/projects/EEGNet-KV260-VitisAI
nano scripts/04_verify_sample_timing.py
```

### Result — Exact Sample-Level Timing Verified

The output confirms the timing at the sample level.
| Parameter          |                  Result |
| ------------------ | ----------------------: |
| Sampling frequency |              **250 Hz** |
| Trial start        |           **367.472 s** |
| Trial start sample |              **91,868** |
| Motor cue          |           **369.472 s** |
| Motor cue sample   |              **92,368** |
| Trial start → cue  | **500 samples = 2.0 s** |
| Trial end          |           **373.472 s** |
| Trial end sample   |              **93,368** |

Relationship:
```
Trial start                         Motor cue                    Trial end
367.472 s                           369.472 s                    373.472 s
   │                                    │                            │
   │──────── 2.0 s / 500 samples ──────│──────── 4.0 s / 1000 ─────│
```
Important finding:

A 4-second window starting at the motor-imagery cue gives:
```
Start sample = 92,368
End sample   = 93,368
Samples      = 1,000
```
At 250 Hz:
```
4 × 250 = 1,000 samples
```

## Step 12 — Finalize the EEG Preprocessing Specification

We now have enough evidence from Steps 7–11 to freeze the preprocessing design and move forward. No more tiny timing-analysis steps.

### 1. Final preprocessing objective

Convert the raw BCI Competition IV Dataset 2a GDF recordings into fixed-size EEG trials suitable for:
```
EEGNet training
ONNX export
Vitis AI quantization
KV260/DPU deployment
```
### 2. Dataset files to use

Use the training recordings:
```
A01T.gdf
A02T.gdf
...
A09T.gdf
```
The E recordings will not be used for supervised training because their class labels are not available in the same way as the training recordings.

### 3. EEG channels

Each recording contains:
```
25 channels
├── 22 EEG
└── 3 EOG
```
We will use only the 22 EEG channels.

The following EOG channels will be excluded:
```
EOG-left
EOG-central
EOG-right
```
Final spatial dimension:
```
22 EEG channels
```
### 4. Sampling frequency

The dataset is sampled at:
```
250 Hz
```
We will retain the original sampling rate.

No resampling will be performed initially.

### 5. Trial identification

Only the four motor-imagery events will be extracted:
```
769 → Left hand
770 → Right hand
771 → Feet
772 → Tongue
```
Labels will be encoded as:
```
769 → 0 → Left hand
770 → 1 → Right hand
771 → 2 → Feet
772 → 3 → Tongue
```
### 6. Final epoch window

We will use:
```
0 to 4 seconds
```
relative to the motor-imagery cue (769–772).

Therefore:
```
Cue
│
├────────────── 4 seconds ──────────────┤
│                                       │
0 s                                     4 s
```
At 250 Hz:
```
4 × 250 = 1000 samples
```
Therefore, every trial will contain:
```
22 channels × 1000 samples
```
Why 0–4 seconds?

Our Step 11 verification established that:
- cue occurs exactly 2 seconds after trial start;
- the trial extends sufficiently beyond the cue;
- a 4-second cue-relative window gives exactly 1000 samples.

Most importantly for our deployment project, 1000 samples gives us a deterministic fixed-size input without relying on endpoint-inclusive epoching that produces 1001 samples.

We will therefore implement the extraction using sample indexing/slicing, not an inclusive tmax=4.0 convention.

### 7. Filtering

We will apply a band-pass filter:
```
8–30 Hz
```
to retain the frequency range commonly used for motor-imagery EEG analysis.

The filtering will be performed before epoch extraction.

### 8. Normalization

Each extracted trial will be standardized independently for each EEG channel.

For each trial and channel:
```
X_normalized = (X - mean(X)) / std(X)
```
where the mean and standard deviation are calculated across the 1000 time samples of that particular channel.

This gives every channel within each trial approximately:
```
mean = 0
standard deviation = 1
```
### 9. Final EEGNet input format

After preprocessing, each trial will have:
```
[22, 1000]
```
For PyTorch Conv2d, we will add:
```
Channel dimension = 1
```
Therefore:
```
[1, 22, 1000]
```
For a batch:
```
[N, 1, 22, 1000]
```
where N is the number of trials.

### 10. Final preprocessing pipeline

The complete pipeline is now:
```
BCI Competition IV Dataset 2a
             │
             ▼
       A01T–A09T GDF
             │
             ▼
       Select 22 EEG channels
             │
             ▼
       Band-pass 8–30 Hz
             │
             ▼
       Detect events 769–772
             │
             ▼
     Epoch 0–4 s from cue
             │
             ▼
       1000 samples/trial
             │
             ▼
 Per-channel, per-trial normalization
             │
             ▼
      Label: 0, 1, 2, 3
             │
             ▼
       Shape [N, 1, 22, 1000]
             │
             ▼
          EEGNet
```
### 11. Frozen preprocessing specification
| Parameter     | Final decision                 |
| ------------- | ------------------------------ |
| Dataset       | BCI Competition IV Dataset 2a  |
| Files         | A01T–A09T                      |
| EEG channels  | 22                             |
| EOG channels  | Excluded                       |
| Sampling rate | 250 Hz                         |
| Events        | 769–772                        |
| Classes       | 4                              |
| Filter        | 8–30 Hz                        |
| Epoch         | 0–4 s from cue                 |
| Samples/trial | **1000**                       |
| Normalization | Per-trial, per-channel z-score |
| Trial shape   | `[22, 1000]`                   |
| EEGNet input  | `[N, 1, 22, 1000]`             |

Status:

Preprocessing specification is now FROZEN.

## Step 13 — Implement the Complete EEG Preprocessing Pipeline

Now we move from analysis to actual preprocessing.

Goal

Process all nine training recordings:
```
A01T.gdf → A09T.gdf
```
and generate one reproducible dataset with:
```
22 EEG channels
8–30 Hz band-pass
0–4 s from motor-imagery cue
1000 samples/trial
per-trial/per-channel normalization
4 classes
```
Final input:
```
[N, 1, 22, 1000]
```
### 1. Create the preprocessing script
```
cd ~/projects/EEGNet-KV260-VitisAI
nano scripts/05_preprocess_eeg.py
```

### 2. Run the complete preprocessing

Make sure the environment is active:
```
source ~/projects/EEGNet-KV260-VitisAI/.venv/eeg-data/bin/activate
```
Then:
```
python scripts/05_preprocess_eeg.py
```

### 3. Verify the generated file

After preprocessing completes:
```
ls -lh datasets/processed/EEGNet_dataset.npz
```
Then verify that it can be loaded:
```
python -c "import numpy as np; d=np.load('datasets/processed/EEGNet_dataset.npz'); print('X:', d['X'].shape); print('y:', d['y'].shape); print('subjects:', d['subjects'].shape)"
```

## Step 14 — Validate the Processed Dataset and Create the Reproducible Train/Test Split

We now have the actual processed EEG dataset. This step will validate it and freeze the dataset split that will be used for all subsequent EEGNet experiments.

No EEGNet architecture yet.

Goal

Perform all of the following in one step:

- Verify dataset shape and consistency.
- Check for NaN and Inf.
- Verify per-trial/per-channel normalization.
- Verify class distribution.
- Create one reproducible train/test split.
- Use:
     - test_size = 0.20
     - random_state = 42
     - stratify = y
- Save the split for all future PyTorch/ONNX/DPU comparisons.

### 1. Install scikit-learn if required

With `(eeg-data)` active:
```bash
python -c "import sklearn; print('scikit-learn:', sklearn.__version__)"
```
If it reports that the module is missing:
```bash
pip install scikit-learn
```

### 2. Create the validation and split script
```bash
cd ~/projects/EEGNet-KV260-VitisAI
nano scripts/06_validate_and_split.py
```

### 3. Run it
```bash
python scripts/06_validate_and_split.py
```

### 4. Output

The script will create:
```
datasets/
└── processed/
    ├── EEGNet_dataset.npz
    └── EEGNet_train_test_split.npz
```

The second file becomes the frozen input for all future model experiments.

Frozen experimental rule

From this point onward:
```
EEGNet training       → X_train, y_train
EEGNet evaluation     → X_test, y_test
ONNX evaluation       → X_test, y_test
INT8 evaluation       → X_test, y_test
KV260 evaluation      → X_test, y_test
```

## Step 15 — Design and Verify the Deployment-Oriented EEGNet Architecture

### 1. Objective

The EEG dataset, preprocessing pipeline, and train/test split are
already frozen.

The purpose of this step is to define the **final EEGNet architecture
selected for the KV260 deployment workflow**.

We are no longer using this document to record architecture experiments
or tuning attempts. The architecture below is the model that will be
taken forward through the Vitis AI deployment flow.

### 2. Target DPU

``` text
DPUCZDX8G_ISA1_B4096
```

Target input:

``` text
[1, 1, 22, 1000]
```

### 3. Final architecture

The final model uses standard `Conv2D`, `BatchNorm2d`, `ReLU`,
`AvgPool2d`, `Flatten`, and `Linear` operations.

No depthwise convolution is used in the final deployment model.

``` text
Input
[1, 1, 22, 1000]
        │
        ▼
Temporal Conv2D
1 → 16
kernel = (1,16)
        │
        ▼
BatchNorm + ReLU
        │
        ▼
Temporal Conv2D
16 → 16
kernel = (1,16)
        │
        ▼
BatchNorm + ReLU
        │
        ▼
Temporal Conv2D
16 → 16
kernel = (1,16)
        │
        ▼
BatchNorm + ReLU
        │
        ▼
Spatial Conv2D
16 → 32
kernel = (11,1)
        │
        ▼
BatchNorm + ReLU
        │
        ▼
Spatial Conv2D
32 → 32
kernel = (12,1)
        │
        ▼
BatchNorm + ReLU
        │
        ▼
AveragePool2D
kernel = (1,4)
stride = (1,4)
        │
        ▼
Temporal Conv2D
32 → 32
kernel = (1,8)
        │
        ▼
BatchNorm + ReLU
        │
        ▼
Pointwise Conv2D
32 → 16
kernel = (1,1)
        │
        ▼
BatchNorm + ReLU
        │
        ▼
AveragePool2D
kernel = (1,8)
stride = (1,8)
        │
        ▼
Flatten
        │
        ▼
Linear
448 → 4
        │
        ▼
4 class logits
```

### 4. Tensor dimensions

For an input tensor:

``` text
[1, 1, 22, 1000]
```

the final tensor progression is:

  Stage             Output shape
  ----------------- --------------------
  Input             `(1, 1, 22, 1000)`
  Temporal Conv 1   `(1, 16, 22, 985)`
  Temporal Conv 2   `(1, 16, 22, 970)`
  Temporal Conv 3   `(1, 16, 22, 955)`
  Spatial Conv 1    `(1, 32, 12, 955)`
  Spatial Conv 2    `(1, 32, 1, 955)`
  Pool 1            `(1, 32, 1, 238)`
  Temporal Conv 4   `(1, 32, 1, 231)`
  Pointwise Conv    `(1, 16, 1, 231)`
  Pool 2            `(1, 16, 1, 28)`
  Flatten           `(1, 448)`
  Output            `(1, 4)`

The classifier therefore uses:

``` text
Linear(448, 4)
```

### 5. Model size

``` text
Total parameters     : 37,188
Trainable parameters : 37,188
```

### 6. Model source

The final architecture is implemented in:

``` text
training/eegnet_dpu.py
```
Do not modify this architecture during the deployment workflow.

## Step 16 --- Verify the Final Architecture

### 1. Environment

Use the Vitis AI PyTorch environment for the DPU compatibility checks.

``` bash
cd /workspace/EEGNet-KV260-VitisAI
```

### 2. Verify tensor dimensions

Run:

``` bash
python training/eegnet_dpu.py
```

The output must confirm:

``` text
Input              : (1, 1, 22, 1000)
Temporal Conv 1    : (1, 16, 22, 985)
Temporal Conv 2    : (1, 16, 22, 970)
Temporal Conv 3    : (1, 16, 22, 955)
Spatial Conv 1     : (1, 32, 12, 955)
Spatial Conv 2     : (1, 32, 1, 955)
Pool 1             : (1, 32, 1, 238)
Temporal Conv 4    : (1, 32, 1, 231)
Pointwise Conv     : (1, 16, 1, 231)
Pool 2             : (1, 16, 1, 28)
Flatten            : (1, 448)
Output             : (1, 4)
```
## Step 17 --- Verify DPU Compatibility with Vitis AI Inspector

### 1. Objective

Verify that the final EEGNet architecture can be mapped to the target
KV260 DPU.

### 2. DPU target

``` text
DPUCZDX8G_ISA1_B4096
```

### 3. Run Inspector

``` bash
python scripts/07_inspect_eegnet_dpu.py
```

### 4. Required result

The final architecture has been verified successfully by the Vitis AI
Inspector.

The decisive result is:

``` text
[VAIQ_NOTE]: All the operators are assigned to the DPU
[VAIQ_NOTE]: =>Finish inspecting.
Inspection completed.
```

Therefore:

``` text
DPUCZDX8G_ISA1_B4096
        │
        ▼
Final EEGNet
        │
        ▼
All operators → DPU
```

This architecture is now **frozen for deployment**.

## Step 18 --- Train the Final DPU-Compatible EEGNet

### 1. Objective

Train the exact architecture that passed the Vitis AI Inspector.

The frozen dataset split remains:

``` text
X_train : (2073, 1, 22, 1000)
y_train : (2073,)

X_test  : (519, 1, 22, 1000)
y_test  : (519,)
```

The model is trained using:

``` text
datasets/processed/EEGNet_train_test_split.npz
```

No new train/test split is created.

### 2. Training script

Use:

``` text
training/train_eegnet_dpu.py
```

### 3. Model output

Save the trained FP32 model as:

``` text
models/EEGNetDPU_FP32.pth
```

### 4. Recorded FP32 result

The final training run produced:

  Metric                Result
  --------------- ------------
  Test accuracy     **46.82%**
  Precision         **47.64%**
  Recall            **46.82%**
  F1-score          **47.11%**

This accuracy is recorded as the **FP32 software baseline for the
deployment demonstration**. The objective of this project is the Vitis
AI/KV260 deployment workflow rather than further EEGNet accuracy
optimization.

## Step 19: Inspect Trained FP32 Model for DPU Compatibility
**Purpose**

Verify that the trained FP32 model is compatible with the target KV260 DPU before INT8 quantization.

**Input model:**
```
models/EEGNetDPU_FP32.pth
```
**Target DPU:**
```
DPUCZDX8G_ISA1_B4096
```
**Script**

File:
```
scripts/08_inspect_trained_eegnet_dpu.py
```
The script:
 - Reconstructs EEGNetDPU.
 - Loads models/EEGNetDPU_FP32.pth.
 - Creates a dummy input of (1, 1, 22, 1000).
 - Runs the Vitis AI Inspector against DPUCZDX8G_ISA1_B4096.

**Run**

Run inside the Vitis AI PyTorch container:
```
cd /workspace/EEGNet-KV260-VitisAI
python scripts/08_inspect_trained_eegnet_dpu.py
```

**Expected Result**
Parameters       : 37188

Trained FP32 model loaded successfully.

[VAIQ_NOTE]: All the operators are assigned to the DPU
[VAIQ_NOTE]: =>Finish inspecting.

Inspection completed.
Result
```
Inspection successful.
```
```
Trained FP32 model loaded: ✓
Parameters: 37,188
Input: (1, 1, 22, 1000)
Target: DPUCZDX8G_ISA1_B4096
All operators assigned to DPU: ✓
```
The trained model is therefore ready for the next stage: Vitis AI INT8 quantization.










