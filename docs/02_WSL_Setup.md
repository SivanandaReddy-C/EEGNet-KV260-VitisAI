# WSL2 and Ubuntu 22.04 Setup

## 1. Objective

Set up Windows Subsystem for Linux 2 (WSL2) with Ubuntu 22.04 LTS to provide the Linux development environment required for the Vitis AI project.

WSL2 will be used as the primary Linux environment for:

- Python development
- PyTorch
- ONNX
- Docker
- Vitis AI tools
- Model compilation
- Development and deployment scripts
---
## 2. Host System

| Component | Configuration |
|---|---|
| Operating System | Windows 11 Enterprise |
| Windows Version | 25H2 |
| OS Build | 26200.8655 |
| Processor | Intel Core i7-14700 |
| RAM | 64 GB |
| Hardware Virtualization | Enabled |
---
## 3. Target Environment

The target environment for this stage is:

```text
Windows 11
    │
    ▼
   WSL2
    │
    ▼
Ubuntu 22.04 LTS
```
---
## 4. Enable Windows Subsystem for Linux

The Windows Subsystem for Linux feature was enabled using an elevated VS Code terminal.

### Administrator Privilege Verification

Administrator privileges were verified using:

```cmd 
net session
```
The command completed without an access-denied error, confirming that the terminal was running with administrator privileges.

Command:
```cmd
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

Result:

The operation completed successfully.
---
## 5. Enable Virtual Machine Platform

The Virtual Machine Platform Windows feature was enabled using an elevated VS Code terminal.

### Command

```
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

Result:

The operation completed successfully.
---
## 6. Verify Required Windows Features

### 6.1 Windows Subsystem for Linux

Command:

```cmd
dism.exe /online /get-featureinfo /featurename:Microsoft-Windows-Subsystem-Linux
```

Result:

State : Enabled

### 6.2 Virtual Machine Platform

Command:

```cmd
dism.exe /online /get-featureinfo /featurename:VirtualMachinePlatform
```

Result:

State : Enable Pending

The feature was successfully enabled, but Windows has marked it as Enable Pending because a system restart is required to complete the configuration.
---
## 7. Post-Restart Verification

After enabling the required Windows features, the system was restarted.

The Virtual Machine Platform feature was checked after the restart using:

```cmd
dism.exe /online /get-featureinfo /featurename:VirtualMachinePlatform
```

The feature reported:
State : Enabled
---
## 8. Verify WSL Installation

### 8.1 Check WSL Status

The WSL configuration was checked using:

```bash
wsl --status
```
Result:
Default Version: 2
This confirms that WSL 2 is configured as the default version for new Linux distributions.

### 8.2 Check WSL Version
The installed WSL components were checked using:
```bash
wsl --version
```
The system reported:
| Component | Version                             |
| --------- | ----------------------------------- |
| WSL       | 2.7.3.0                             |
| Kernel    | 6.6.14.1-1                          |
| WSLg      | 1.0.73                              |
| MSRDC     | 1.2.6676                            |
| Direct3D  | 1.611.1-81528511                    |
| DXCore    | 10.0.26100.1-240331-1435.ge-release |
| Windows   | 10.0.26200.8655                     |

---
## 9. Check Available Linux Distributions

Before installing Ubuntu, the available WSL distributions were checked using:

```bash
wsl --list --online
```
Distribution Selected:
``` text
Ubuntu-22.04
```
Reason for Selection:
Ubuntu 22.04 LTS was selected as the Linux development environment for this project to provide a stable and reproducible environment for the subsequent Vitis AI workflow.

---

## 10. Install Ubuntu 22.04 LTS

Ubuntu 22.04 LTS was installed using:

```bash
wsl --install -d Ubuntu-22.04
```

## 11. First Launch and Ubuntu User Configuration

The installed Ubuntu 22.04 distribution was launched using:

```bash
wsl -d Ubuntu-22.04
```

The first-launch process performed the initial provisioning of the Ubuntu 22.04 WSL instance.

### 11.1 Linux User Creation

Ubuntu requested creation of a default Unix user account.

The following Linux user was created:

```text
vitisdev
```
The password was configured successfully.

The password is not recorded in the project documentation.

### 11.2 Ubuntu Version

The first-launch screen reported:
```
Ubuntu 22.04.5 LTS
```
The WSL2 Linux kernel reported:
```
6.6.114.1-microsoft-standard-WSL2
```

### 11.3 Initial Provisioning Messages
During the first launch, the following messages were displayed:
```
/usr/lib/wsl/wsl-setup: line 106:
/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0/powershell.exe:
cannot execute binary file: Exec format error

/usr/lib/wsl/wsl-setup: line 76:
/mnt/c/WINDOWS/System32/WindowsPowerShell/v1.0/powershell.exe:
cannot execute binary file: Exec format error
```
Despite these messages, the Ubuntu provisioning process continued successfully and the default Unix user was created.

The Windows PowerShell issue was already present on the host Windows system before configuring this WSL environment. Therefore, PowerShell was treated as a separate host-system issue and was not considered a requirement for the WSL setup.

### 11.4 Ubuntu Shell
After the first-launch configuration was completed, Ubuntu successfully provided a Linux shell prompt similar to:
```
vitisdev@Researchpc1:~$
```
The Ubuntu WSL environment was therefore successfully initialized.

--- 
## 12. Ubuntu Environment Verification

The newly initialized Ubuntu environment was verified using standard Linux commands.

### 12.1 Verify Current User

Command:

```bash
whoami
```
Result:
```
vitisdev
```
This confirms that the Ubuntu environment is running under the newly created Linux user.

### 12.2 Verify Ubuntu Version
Command:
```bash
lsb_release -a
```
Result:
```
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.5 LTS
Release:        22.04
Codename:       jammy
```
Ubuntu 22.04.5 LTS is installed.
### 12.3 Verify WSL2 Kernel
Command:
```bash
uname -a
```
The output included:
```
6.6.114.1-microsoft-standard-WSL2
```
This confirms that Ubuntu is running under WSL2.

### 12.4 Verify Linux Home Directory
Command:
```bash
echo $HOME
```
Result:
```
/home/vitisdev
```
### 12.5 Verify System Architecture
Command:
```bash
uname -m
```
Result:
```
x86_64
```
The WSL environment is running as a 64-bit x86 Linux environment.

### 12.6 Verify Windows Drive Access

Command:
```bash
ls /mnt
```
The following mount points were available:
```
c
d
wsl
wslg
```
This confirms that the Windows filesystems are accessible from WSL.

Verification Summary:
| Verification         | Result                            |
| -------------------- | --------------------------------- |
| Linux user           | `vitisdev`                        |
| Ubuntu version       | Ubuntu 22.04.5 LTS                |
| WSL kernel           | 6.6.114.1-microsoft-standard-WSL2 |
| Architecture         | x86_64                            |
| Home directory       | `/home/vitisdev`                  |
| Windows drive access | Available                         |


## 13. WSL-to-Windows Executable Interoperability

### 13.1 Initial Problem

During the initial Ubuntu provisioning, Windows executables could not be executed from the WSL environment.

For example, attempting to execute Windows `cmd.exe` from Ubuntu resulted in:

```text
cannot execute binary file: Exec format error
```
The same type of error was observed when the WSL setup process attempted to invoke Windows PowerShell.

### 13.2 Investigation

The WSL configuration was inspected using:
```bash
cat /etc/wsl.conf
```
The initial configuration contained:
```
[boot]
systemd=true

[user]
default=vitisdev
```
The Linux binary-format registration mechanism was checked using:
```bash
cat /proc/sys/fs/binfmt_misc/status
```
The result was:
```
enabled
```
However, the WSL interoperability registration was initially absent from:
```bash
ls -la /proc/sys/fs/binfmt_misc/
```
The expected:
```
WSLInterop
```
entry was not present.

The systemd-binfmt service was also inspected:
```
systemctl status systemd-binfmt --no-pager
```
The service was inactive because its WSL virtualization condition was not met.

### 13.3 Resolution

Systemd was not required for the current project environment, so it was disabled in the Ubuntu WSL configuration.

The /etc/wsl.conf file was changed to:

```
[user]
default=vitisdev
```
WSL was then completely shut down from Windows:
```bash
wsl --shutdown
```
Ubuntu 22.04 was started again using:
```bash
wsl -d Ubuntu-22.04
```
### 13.4 Verify WSL Interoperability

After restarting Ubuntu, the Linux init process was checked:
```bash
ps -p 1 -o comm=
```
Result:
```
init
```
The WSL binary-format registrations were then checked:
```bash
ls -la /proc/sys/fs/binfmt_misc/
```
The following entry was now present:
```
WSLInterop
```
The registration was further inspected using:
```bash
cat /proc/sys/fs/binfmt_misc/WSLInterop
```
The result included:
```
enabled
interpreter /init
```

### 13.5 Test Windows Executable Execution

Windows cmd.exe was executed from Ubuntu using:
```bash
/mnt/c/Windows/System32/cmd.exe /c echo WSL-to-Windows-interoperability-OK
```
Result:
```
WSL-to-Windows-interoperability-OK
```
This confirmed that Windows executable interoperability was functioning correctly.

Note on PowerShell:

Windows PowerShell had an existing issue on the host Windows installation before this project was started.

Therefore, PowerShell was not used as the primary verification mechanism for WSL interoperability.

The WSL-to-Windows executable path was successfully verified using cmd.exe.

Result:

WSL-to-Windows executable interoperability is functioning correctly.

The WSL environment is considered operational for the next stages of the project.

## 14. WSL Resource Verification

Before installing additional development tools, the resources available to the WSL2 environment were checked.

### 14.1 Memory

Command:

```bash
free -h
```
The WSL environment reported approximately:
```
Total Memory:      31 GiB
Available Memory:  30 GiB
Swap:               8 GiB
```
The WSL environment currently has approximately 31 GiB of RAM available.

### 14.2 Storage

Command:
```bash
df -h /
```
Result:
```
Filesystem:  /dev/sdd
Size:         1007 GB
Used:           1.3 GB
Available:     955 GB
Usage:           1%
```
The WSL Linux filesystem has approximately 955 GB of available storage.

### 14.3 CPU

Command:
```bash
nproc
```
Result:
```
28
```
The WSL environment can access 28 logical processors.

### 14.4 Resource Summary
| Resource     | Available to WSL |
| ------------ | ---------------: |
| RAM          |          ~31 GiB |
| Swap         |            8 GiB |
| Storage      |          ~955 GB |
| Logical CPUs |               28 |

## 15. WSL Setup Status

The WSL2 environment has been successfully established with Ubuntu 22.04.5 LTS.

### Completed

- [x] Hardware virtualization verified
- [x] Windows Subsystem for Linux enabled
- [x] Virtual Machine Platform enabled
- [x] System restarted after enabling required Windows features
- [x] WSL 2 verified
- [x] Ubuntu 22.04 LTS installed
- [x] Linux user `vitisdev` created
- [x] Ubuntu 22.04.5 LTS verified
- [x] WSL2 kernel verified
- [x] x86_64 architecture verified
- [x] Windows filesystem access verified
- [x] WSL-to-Windows executable interoperability verified
- [x] WSL resources verified

### Current Environment

```text
Windows 11
    │
    ▼
   WSL2
    │
    ▼
Ubuntu 22.04.5 LTS
    │
    └── vitisdev
```
### Next Step

The Windows and WSL2 foundation is now complete.

The next stage is to establish the Linux-side project workspace and Git environment inside Ubuntu.

The repository will subsequently be cloned into the WSL Linux filesystem so that Linux-based development tools can operate directly on the project files.

The next documentation will cover this process before installing Docker and Vitis AI.