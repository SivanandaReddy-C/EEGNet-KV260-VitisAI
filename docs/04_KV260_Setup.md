# KV260 Setup

## 1. Objective

This document records the complete setup and verification of the AMD Kria KV260 Vision AI Starter Kit for the EEGNet deployment project.

The target workflow is:

```text
EEGNet Model
    ↓
ONNX Model
    ↓
Vitis AI Quantization
    ↓
Vitis AI Compilation
    ↓
KV260 DPU
    ↓
Inference
    ↓
Performance Benchmarking
```
The KV260 target system will be configured and verified before beginning the Vitis AI deployment workflow.

## 2. Target Hardware

The target hardware for this project is:

AMD Kria KV260 Vision AI Starter Kit
K26 SOM
KV260 Vision Carrier Card
microSD card
Ethernet connection
USB-UART connection to the host PC
12 V power supply

The KV260 contains two boot devices:

QSPI memory on the SOM
microSD card interface on the carrier card

For this setup, the microSD card will contain the runtime Ubuntu operating system.

The QSPI boot firmware will not be manually reprogrammed during the initial setup unless a later compatibility or firmware requirement makes this necessary.

## 3. Target Operating System

Ubuntu 22.04 LTS was selected as the target operating system for this project.

The KV260 Linux documentation identifies Ubuntu 22.04 as the supported environment for KV260 applications, while the current documentation notes that KV260 applications are not yet supported on Ubuntu 24.04.

Therefore, Ubuntu 22.04 will be used for the initial KV260 setup and Vitis AI deployment workflow.

## 4. SD Card Preparation
### 4.1 Required Components

The following are required:

microSD card
Host PC
microSD card reader
Internet connection
KV260 Ubuntu 22.04 image
SD-card imaging software

AMD's KV260 documentation specifies a 16 GB UHS-1 microSD card as the basic requirement.

For this project, a larger card may be used to provide additional space for Docker images, models, datasets, logs, and other development files.

### 4.2 Download the KV260 Ubuntu 22.04 Image

The appropriate KV260 Ubuntu 22.04 image will be downloaded from the official AMD/Ubuntu distribution source.

The image must be selected specifically for:
```
AMD Kria K26 SOM
KV260 Vision AI Starter Kit
Ubuntu 22.04
```

### 4.3 Download the SD Card Imaging Tool

Raspberry Pi Imager is the recommended image flashing tool in the AMD KV260 documentation.

The imaging tool will be installed on the Windows host PC.

### 4.4 Flash the microSD Card

The downloaded Ubuntu image will be written to the microSD card using the image flashing tool.

The procedure is:

Insert the microSD card into the Windows host PC.
Start Raspberry Pi Imager.
Select the option to use a custom image.
Select the downloaded KV260 Ubuntu 22.04 image.
Select the correct microSD card as the storage device.
Verify that the selected storage device is the intended microSD card.
Start the write operation.
Wait for the write and verification process to complete.
Safely eject the microSD card from Windows.

The SD card will then be inserted into the KV260.

## 5. KV260 Hardware Connections

Before powering the board, the required connections will be made.

### 5.1 microSD Card

Insert the flashed microSD card into the KV260 microSD card slot.

### 5.2 USB-UART Connection

Connect a data-capable USB-A to micro-USB cable between:
```
KV260 USB-UART connector
        ↓
Host PC
```
The USB connection will be used to access the Linux serial console.

### 5.3 Ethernet

Connect the KV260 Ethernet port to the local network.

Internet connectivity is required for system updates and later software installation.

### 5.4 Display

A monitor may be connected using HDMI or DisplayPort.

The display is optional for the server-style command-line workflow because the primary interface for this project will be the UART console and SSH.

### 5.5 Power

Connect the supplied 12 V power adapter to the KV260 power connector.

The power supply will be connected to AC only after the other required connections are in place.

## 6. UART Serial Console

The KV260 Ubuntu server image provides access to the command line through the USB-UART interface.

### 6.1 Windows COM Port Detection

After connecting the USB-UART cable:

- Open Windows Device Manager.
- Expand:
```
Ports (COM & LPT)
```
- Identify the COM ports associated with the KV260.
The KV260 uses an FTDI USB-to-COM interface.

The UART interface is the second enumerated COM port according to the AMD documentation.

### 6.2 UART Configuration

A serial terminal application such as PuTTY or Tera Term will be used.

The UART parameters are:
```
Baud rate:    115200
Data bits:    8
Stop bits:    1
Parity:       None
Flow control: None
```
The correct COM port identified in Device Manager will be selected.

## 7. First Boot

After the SD card and UART connection are ready:

Start the serial terminal.
Select the KV260 UART COM port.
Apply the UART configuration.
Connect the KV260 power supply to AC.
Observe the UART console.

The KV260 powers on immediately when the power supply is connected.

The QSPI boot firmware loads the boot components and the system boots the Linux image from the microSD card.

The UART console should display the Linux boot messages.

## 8. Initial Login

The default Ubuntu credentials for the initial login are:
```
Username: ubuntu
Password: [Not recorded for security]
```
At the first login, Ubuntu normally requires the default password to be changed.

A new password will be configured during the first login.

Record the First Login
Initial username: ubuntu

Initial password: [Not recorded for security]

New password: [Not recorded for security]

## 9. Verify Basic Linux Operation

After logging into the KV260, verify the operating system.

Run:
```bash
uname -a
```
Then:
``` bash
cat /etc/os-release
```
Then:
``` bash
hostname
```
Then:
``` bash
whoami
```

The results are:
| Item                 | Value                                  |
| -------------------- | -------------------------------------- |
| **Kernel**           | `Linux 5.15.0-1027-xilinx-zynqmp`      |
| **Operating System** | `Ubuntu 22.04.4 LTS (Jammy Jellyfish)` |
| **Hostname**         | `kria`                                 |
| **Current User**     | `ubuntu`                               |

## 10. Network Configuration

The KV260 was connected to the local network using the Ethernet interface.

The Ethernet interface was identified as `eth0`.

The interface status and IP configuration were checked using:

```bash
ip addr
```
The observed configuration was:
| Parameter        | Value             |
| ---------------- | ----------------- |
| **Interface**    | `eth0`            |
| **Status**       | `UP`              |
| **IPv4 Address** | `172.18.160.17`   |
| **Subnet**       | `/24`             |
| **Network**      | `172.18.160.0/24` |
| **Broadcast**    | `172.18.160.255`  |
The IP address was assigned dynamically through DHCP.

### 10.1 Routing Configuration

The routing table was checked using:
```bash
ip route
```
The observed default route was:
```
default via 172.18.160.1 dev eth0 proto dhcp metric 100
```
Therefore, the default gateway was identified as:
```
172.18.160.1
```
The complete relevant routing configuration was:
```
default via 172.18.160.1 dev eth0 proto dhcp metric 100
172.18.160.0/24 dev eth0 proto kernel scope link src 172.18.160.17 metric 100
```
### 10.2 Gateway Connectivity
The local network gateway was tested using:
```bash
ping -c 4 172.18.160.1
```
The test was successful:
```
4 packets transmitted, 4 received, 0% packet loss
```
Therefore, connectivity between the KV260 and the local network gateway was verified successfully.
### 10.3 Internet Connectivity

Internet connectivity was initially tested using:
```bash
ping -c 4 8.8.8.8
```
The test resulted in:
```
4 packets transmitted, 0 received, 100% packet loss
```
Since ICMP traffic may be blocked by the network, Internet connectivity was verified using DNS resolution and HTTPS instead.

DNS resolution was tested using:
```bash
getent hosts google.com
```
The command successfully resolved google.com.

HTTPS connectivity was tested using:
```bash
curl -I --connect-timeout 10 https://google.com
```
The request successfully returned an HTTP redirect:
```
HTTP/2 301
location: https://www.google.com/
```
Therefore, normal Internet access from the KV260 was verified.

The network verification status is:
| Test                         | Status |
| ---------------------------- | ------ |
| **Ethernet interface**       | PASS   |
| **DHCP address assignment**  | PASS   |
| **Default gateway**          | PASS   |
| **Gateway connectivity**     | PASS   |
| **DNS resolution**           | PASS   |
| **HTTPS Internet access**    | PASS   |
| **ICMP access to `8.8.8.8`** | FAIL   |
The ICMP failure is not considered a blocker because DNS resolution and HTTPS Internet access were successfully verified.

### 10.4 DHCP Address Variation

The KV260 obtains its IPv4 address dynamically through DHCP.

During the initial network verification, the address was:

```text
172.18.160.17/24
```

After a subsequent reboot and reconnection of the Ethernet cable, the KV260 received:
```
172.18.180.11/24
```
This confirms that the IPv4 address is dynamically assigned and may change between boots or network reconnections.

The current IP address should therefore be determined using:
```
ip addr show eth0
```
rather than being assumed to be fixed.



## 11. System Package Repository Update

The Ubuntu package repository information was refreshed using:

```bash
sudo apt update
```
The initial attempt failed because the Ethernet cable was disconnected from the KV260. As a result, the eth0 interface was unavailable and DNS resolution for the Ubuntu repositories failed.

After reconnecting the Ethernet cable, the network connection was verified using:

```bash
nmcli device status
```
The result showed:
```
DEVICE  TYPE      STATE      CONNECTION
eth0    ethernet  connected  Wired connection 1
lo      loopback  unmanaged  --
```
The KV260 subsequently obtained an IPv4 address through DHCP:
```
172.18.180.11/24
```
DNS resolution was verified using:
```
getent hosts ports.ubuntu.com
```
The Ubuntu repository hostname resolved successfully.
The package repository update was then repeated:
```
sudo apt update
```
The operation completed successfully:
```
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
```
The system reported that 597 packages could be upgraded.

A full system package upgrade was intentionally not performed because it is not required for the initial KV260/Vitis AI environment setup.

Package Repository Verification
| Test                     | Status        |
| ------------------------ | ------------- |
| Ethernet connection      | PASS          |
| DHCP address assignment  | PASS          |
| DNS resolution           | PASS          |
| Ubuntu repository access | PASS          |
| `sudo apt update`        | PASS          |
| Full system upgrade      | NOT PERFORMED |


## 12. XRT Verification

The KV260 software environment was checked for the AMD/Xilinx XRT utilities.

### 12.1 XRT Utility

The `xbutil` utility was located using:

```bash
which xbutil
```
The result was:
```bash
/usr/bin/xbutil
```
The installed XRT version was checked using:
```bash
xbutil --version
```
The result was:
```
Version : 2.13.0
Branch  :
Hash    :
Hash Date : 2022-09-15 17:01:20
ZOCI    : 2.13.0
```
Therefore, XRT 2.13.0 is installed on the KV260.
### 12.2 DFX Manager Utility

The `xmutil` utility was located using:
```bash
which xmutil
```
The result was:
```
/usr/bin/xmutil
```
An initial attempt to list the installed accelerator applications using:
```bash
xmutil listapps
```
resulted in a permission error:
```
DFX-MGRD: ERROR: connect(/tmp/dfx-mgrd.socket): Permission denied
```
The command was subsequently executed with elevated privileges:
```bash
sudo xmutil listapps
```
The command successfully returned:
```
Accelerator       Accelerator type   Base             Base type   #Slots(PL+AI)   Active slot

k26-starter-kits  XRT_FLAT            k26-starter-kits XRT_FLAT    (0+0)           0
```
This confirms that the k26-starter-kits accelerator environment is present and that the base XRT flat-shell configuration is active. 
No additional dynamic accelerator slot is currently loaded.

## 13. XRT Platform Examination

After verifying the XRT utilities and the active `k26-starter-kits` XRT flat-shell configuration, the KV260 platform was examined using:

```bash
sudo xbutil examine
```
The command was used to inspect the Linux environment, KV260 hardware, XRT installation, and available XRT accelerator devices.

### 13.1 System Configuration

The xbutil examine command reported the following system configuration:
```
System Configuration

OS Name        : Linux
Release        : 5.15.0-1027-xilinx-zynqmp
Version        : #31-Ubuntu SMP Wed Feb 21 04:33:09 UTC 2024
Machine        : aarch64
CPU Cores      : 4
Memory         : 3911 MB
Distribution   : Ubuntu 22.04.4 LTS
GLIBC          : 2.35
Model          : ZynqMP KV260 revB
```

The results confirm that the KV260 is running the expected ARM64 (aarch64) Linux environment with the Ubuntu 22.04.4 LTS operating system.

The detected hardware model is:
```
ZynqMP KV260 revB
```
### 13.2 XRT Configuration

The XRT section of the examination reported:
```
XRT

Version        : 2.13.0
Branch         :
Hash           :
Hash Date      : 2022-09-15 17:01:20
ZOCL           : 2.13.0
```
This confirms that XRT version 2.13.0 is installed and that the corresponding ZOCL component is also version 2.13.0.

### 13.3 Accelerator Device Detection

The examination also reported:
```
Devices present
0 devices found
```
Therefore, no XRT accelerator device was detected in the current configuration.

At this stage, the KV260 is using the default:
```
k26-starter-kits
XRT_FLAT
```
configuration identified previously using:
```bash
sudo xmutil listapps
```

The current configuration does not yet provide the DPU accelerator device required for Vitis AI inference.

Therefore, the 0 devices found result is recorded as the current platform state rather than as a failure of the basic XRT installation.

### 13.4 XRT Platform Examination Summary

The results of the platform examination are summarized below:

| Parameter               | Observed Value            | Status            |
| ----------------------- | ------------------------- | ----------------- |
| Operating System        | Ubuntu 22.04.4 LTS        | PASS              |
| Kernel                  | 5.15.0-1027-xilinx-zynqmp | PASS              |
| Architecture            | aarch64                   | PASS              |
| KV260 Model             | ZynqMP KV260 revB         | PASS              |
| CPU Cores               | 4                         | PASS              |
| Memory                  | 3911 MB                   | PASS              |
| XRT Version             | 2.13.0                    | PASS              |
| ZOCL Version            | 2.13.0                    | PASS              |
| XRT Accelerator Devices | 0 detected                | NOT YET AVAILABLE |

The XRT software environment is therefore installed and operational at the base platform level. The DPU accelerator environment has not yet been installed or activated.

## 14. Xilinx/Kria Package Inspection

The KV260 Ubuntu image was inspected to determine which Xilinx/Kria software components were already installed.

The installed Xilinx-related packages were listed using:

```bash
dpkg -l | grep -E 'xlnx|xilinx|kria'
```
The system was found to contain several Xilinx/Kria-specific packages, including:
```
dfx-mgr
libdfx-mgr
libdfx
fpga-manager-xlnx
flash-kernel-xlnx
linux-firmware-xilinx
linux-image-xilinx-zynqmp
linux-modules-xilinx-zynqmp
xlnx-default-bitstreams
xlnx-platformstats
```
These packages confirm that the installed Ubuntu image is a Kria/Xilinx-enabled image rather than a generic Ubuntu installation.

### 14.1 Xilinx Runtime and DFX Components

The installed XRT and DFX-related packages were verified as part of the package inspection.

The important components include:
| Component            | Purpose                                                     |
| -------------------- | ----------------------------------------------------------- |
| `xrt`                | Xilinx Runtime used to communicate with accelerator devices |
| `dfx-mgr`            | Dynamic Function eXchange management                        |
| `libdfx-mgr`         | Library support for DFX management                          |
| `libdfx`             | Xilinx DFX library                                          |
| `fpga-manager-xlnx`  | Xilinx FPGA Manager support                                 |
| `xlnx-platformstats` | Platform statistics utility                                 |

### 14.2 Default KV260 Bitstream Package

The installed default bitstream package was identified as:
```
xlnx-default-bitstreams
```
The installed package version is:
```
2022.1-0ubuntu1~22.04.1
```
The package contents were inspected using:
```
dpkg -L xlnx-default-bitstreams
```
The package provides the default KV260 starter-kit firmware under:
```
/lib/firmware/xilinx/k26-starter-kits/
```
The directory contains:
```
K26_starter_kits.bit.bin
k26_starter_kits.dtbo
shell.json
```
The default starter-kit firmware therefore exists on the KV260 and is currently available to the system.

### 14.3 Current DFX Firmware Status
The specific DFX firmware package required for the K26 2RP DFX platform was checked using:
```bash
apt-cache policy xlnx-firmware-k26-dfx-2rp
```
The result was:
```
N: Unable to locate package `xlnx-firmware-k26-dfx-2rp`
```

Therefore, the `xlnx-firmware-k26-dfx-2rp` package is not available through the currently configured APT package sources.

This is consistent with the current `xmutil listapps` result, which shows only:
```
Accelerator       Accelerator type   Base
k26-starter-kits  XRT_FLAT           k26-starter-kits
```

No DPU accelerator is currently listed.

### 14.4 Package Inspection Summary

The current KV260 software state is:
| Component                    | Status            |
| ---------------------------- | ----------------- |
| XRT                          | Installed         |
| DFX Manager                  | Installed         |
| Xilinx FPGA Manager          | Installed         |
| Xilinx Linux firmware        | Installed         |
| Default KV260 bitstreams     | Installed         |
| `k26-starter-kits` firmware  | Installed         |
| K26 DFX 2RP firmware package | Not installed     |
| DPU accelerator              | Not yet available |

The base Xilinx/Kria software environment is therefore present and functional. The remaining task is to obtain and install the appropriate K26 DFX 2RP firmware containing the DPU accelerator.

## 15. K26 DFX 2RP Firmware Installation and DPU Activation

The K26 Dynamic Function eXchange (DFX) firmware required for the KV260 DPU was not available through the configured Ubuntu APT repositories.

Therefore, the required K26 DFX firmware was obtained from the AMD/Xilinx Kria applications firmware repository and installed manually on the KV260.

### 15.1 K26 DFX Firmware Repository

The Kria applications firmware repository was cloned on the KV260 using:

```bash
git clone --branch xlnx_rel_v2022.1 --recursive https://github.com/Xilinx/kria-apps-firmware.git
```
The repository was checked out to the required release branch:
```bash
cd ~/kria-apps-firmware
git branch --show-current
```
The result was:
```
xlnx_rel_v2022.1
```
The repository status was also verified:
```bash
git status
```
The result indicated that the working tree was clean and synchronized with the selected release branch.
### 15.2 K26 DFX 2RP Firmware Contents

The K26 DFX 2RP firmware directory was inspected:
```bash
ls -la k26-dfx/2rp
```
The directory contains the DFX accelerator configurations required for the KV260, including:
```
AES128
AES192
DPU
FFT
FIR
PP_PIPELINE
```
The DPU-specific firmware directory was further inspected:
```bash
ls -la k26-dfx/2rp/DPU
```
The DPU configuration contains two DFX slots:
```
DPU_slot0
DPU_slot1
```
The DPU firmware artifacts include the corresponding partial bitstreams and Xilinx shell/platform files.
### 15.3 Makefile Inspection
The K26 DFX 2RP Makefile was inspected to understand the firmware generation and installation process:
```bash
cat k26-dfx/2rp/Makefile
```
The Makefile defines the generation of:
```
.bit files
.bin files
.dtbo files
.xclbin files
shell.json files
```
The installation directory is defined as:
```
/lib/firmware/xilinx/k26-dfx-2rp/
```
The Makefile therefore provides the required mechanism for generating and installing the K26 DFX 2RP firmware.
### 15.4 Bootgen Installation
The firmware generation process requires Xilinx Bootgen.
Bootgen was checked using:
```bash
which bootgen
```
The executable was available at:
```
/usr/bin/bootgen
```
The installed package was verified using:
```bash
apt-cache policy bootgen-xlnx
```
The package was already available in the configured Ubuntu repositories.
Bootgen was installed using:
```bash
sudo apt install bootgen-xlnx
```
The installed Bootgen executable reported:
```
***** Xilinx Bootgen v2022.2
```

The `bootgen -version` command itself is not supported by this Bootgen build and therefore reports a command-line syntax error after displaying the Bootgen version banner. The presence of the `/usr/bin/bootgen` executable and the `Xilinx Bootgen v2022.2` banner confirm that Bootgen is installed.

### 15.5 Generate and Install K26 DFX 2RP Firmware
The K26 DFX 2RP firmware was generated and installed using:
```bash
sudo make -C k26-dfx/2rp/ install
```
The Makefile invoked Bootgen to generate the required boot images for the available DFX accelerator configurations.

The generation process successfully produced boot images for configurations including:
```
OpenDXF shell wrapper
AES128
AES192
DPU
FFT
FIR
PP_PIPELINE
```
The Bootgen output repeatedly reported:
```
[INFO] : Boot image generated successfully
```
The Makefile completed and returned to the shell prompt without reporting an installation error.
### 15.6 Verify Installed DFX Firmware
The installed firmware directory was verified using:
```bash
ls -la /lib/firmware/xilinx/k26-dfx-2rp
```
The directory contained the expected DFX accelerator directories:
```
AES128
AES192
DPU
FFT
FIR
PP_PIPELINE
```
It also contained the generated platform files:
```
opendfx_shell_wrapper.bin
opendfx_shell_wrapper.dtbo
shell.json
```
The DPU firmware directory was verified using:
```bash
ls -la /lib/firmware/xilinx/k26-dfx-2rp/DPU
```
The directory contained:
```
DPU_slot0
DPU_slot1
```
Therefore, the K26 DFX 2RP firmware was successfully installed under:
```
/lib/firmware/xilinx/k26-dfx-2rp/
```
### 15.7 Verify DFX Applications with xmutil
The available accelerator applications were examined using:
```bash
sudo xmutil listapps
```
The resulting configuration showed the default starter-kit application together with the newly installed DFX accelerators.
The DFX applications included:
```
AES128
AES192
DPU
FFT
FIR
PP_PIPELINE
```
The DFX applications reported:
```
Base       : k26-dfx-2rp
Base type  : PL_DFX
```
with two programmable-logic slots:
```
#slots(PL+AI): (2+0)
```
This confirms that the K26 DFX 2RP firmware is successfully registered with the DFX manager.

### 15.8 Load the DPU Accelerator
The default starter-kit application was unloaded before activating the DPU DFX application.

The DPU accelerator was then loaded using:
```bash
sudo xmutil loadapp DPU
```

The DPU became active in DFX slot 0.

The active configuration was verified using:
```bash
sudo xmutil listapps
```
The relevant result was:
```
DPU    ...    Active_slot    0
```
while the default:
```
k26-starter-kits
```
application was no longer active.

Therefore, the DPU partial configuration was successfully loaded into DFX slot 0.

### 15.9 XRT Device Verification After DPU Activation
After loading the DPU, the XRT device was examined using:
```bash
sudo xbutil examine
```
The result changed from the earlier:
```
0 devices found
```
to:
```
Devices present

[0000:00:00.0] : edge
```
with the device reported as ready.

The device was subsequently examined explicitly using:
```bash
sudo xbutil examine --device 0000:00:00.0
```
The platform information reported:
```
XSA Name        : edge
Platform UUID   : 0x0
DDR Size        : 4294967296 Bytes
DDR Count       : 1
P2P Status      : not supported
```
The detected XRT device therefore corresponds to the edge platform and provides approximately 4 GB of DDR memory.

### 15.10 ZOCL Verification
The ZOCL kernel module was verified using:
```bash
lsmod | grep zocl
```
The result showed:
```
zocl
```
indicating that the XRT ZOCL kernel driver is loaded.
The DRM device nodes were also present:
```
/dev/dri/card0
/dev/dri/renderD128
```
The kernel log was inspected using:
```bash
sudo dmesg | grep -i -E 'zocl|dpu|xrt' | tail -50
```
The log showed ZOCL client creation and destruction events without an observed ZOCL initialization failure.

### 15.11 Final DPU/XRT Verification Status
The final KV260 DPU and XRT status is summarized below:
| Component                         | Status         |
| --------------------------------- | -------------- |
| K26 DFX 2RP repository            | PASS           |
| `xlnx_rel_v2022.1` branch         | PASS           |
| Bootgen                           | PASS           |
| K26 DFX 2RP firmware generation   | PASS           |
| K26 DFX 2RP firmware installation | PASS           |
| DPU firmware present              | PASS           |
| DFX manager registration          | PASS           |
| DPU loaded into slot 0            | PASS           |
| XRT device detected               | PASS           |
| XRT device BDF                    | `0000:00:00.0` |
| XRT platform                      | `edge`         |
| Device Ready                      | YES            |
| ZOCL kernel module                | Loaded         |
| DDR available to platform         | 4 GB           |

At this point, the KV260 hardware-side DPU environment has been successfully configured and verified.

The KV260 is now ready for the Vitis AI software/development environment and subsequent EEGNet quantization, compilation, deployment, and inference stages.
