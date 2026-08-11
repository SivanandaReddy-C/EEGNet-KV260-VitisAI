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

## 16. Configure Git in WSL

Git was configured inside the Ubuntu WSL environment so that Git operations could be performed directly from Linux.

### 16.1 Verify Git Installation

Command:
```bash
git --version
```
The installed Git version was verified successfully.

### 16.2 Configure Git User Identity

The Git commit identity was configured using:
```bash
git config --global user.name "SivanandaReddy-C"
git config --global user.email "nanduksrmce@gmail.com"
```
The configuration was verified using:
```bash
git config --global --list
```
The resulting identity was:
```
user.name=SivanandaReddy-C
user.email=nanduksrmce@gmail.com
```
This configuration identifies the author of Git commits created from the WSL environment.

Note: Git user identity is different from GitHub authentication. The user.name and user.email settings identify commits; they do not authenticate Git operations with GitHub.

## 17. Configure GitHub SSH Authentication

SSH authentication was selected for GitHub so that Git operations could be performed from WSL without using GitHub account passwords.

The GitHub account uses two-factor authentication, and normal GitHub password authentication is not supported for Git operations.

### 17.1 Check for Existing SSH Directory

Command:
```bash
ls -la ~/.ssh
```
An SSH directory did not initially exist.

### 17.2 Generate ED25519 SSH Key

An ED25519 SSH key pair was generated using:
```
ssh-keygen -t ed25519 -C "nanduksrmce@gmail.com"
```
The key files were created as:
```
Private key:
~/.ssh/id_ed25519
```
```
Public key:
~/.ssh/id_ed25519.pub
```
The private key is kept only in the WSL environment and must not be shared or uploaded.

The public key was added to the GitHub account as an Authentication Key.

## 18. Initial SSH Connectivity Test

GitHub SSH connectivity was initially tested using:
```bash
ssh -T git@github.com
```
The connection attempted to use SSH port 22.

The connection did not complete and eventually produced:
```
ssh: connect to host github.com port 22: Connection timed out
```
This indicated that SSH port 22 was unavailable from the current network environment.

The SSH key itself was therefore not considered to be the problem.

## 19. Use GitHub SSH over Port 443

GitHub provides an SSH endpoint that can be accessed through port 443.

The connection was tested using:
```bash
ssh -T -p 443 git@ssh.github.com
```
During the first connection, SSH requested confirmation of the GitHub host identity.

The displayed ED25519 host fingerprint was verified against GitHub's published SSH fingerprint before accepting the connection.

After accepting the host key, authentication succeeded.

The following message was displayed:
```
Hi SivanandaReddy-C! You've successfully authenticated, but GitHub does not provide shell access.
```
This message confirms successful SSH authentication.

The message about shell access is expected because GitHub does not provide an interactive shell through this SSH service.

## 20. Configure SSH to Use Port 443 Automatically

To avoid specifying port 443 manually for every GitHub SSH operation, an SSH configuration file was created:
```
~/.ssh/config
```
The configuration is:
```
Host github.com
    HostName ssh.github.com
    User git
    Port 443
    IdentityFile ~/.ssh/id_ed25519
    IdentitiesOnly yes
```
The configuration file permissions were set to 600:
```
chmod 600 ~/.ssh/config
```
The permissions were verified using:
```
stat -c '%a %n' ~/.ssh/config
```
Result:
```
600 /home/vitisdev/.ssh/config
```
The configuration was verified using:
```
cat ~/.ssh/config
```
The normal GitHub SSH authentication command was then tested:
```
ssh -T git@github.com
```
Result:
```
Hi SivanandaReddy-C! You've successfully authenticated, but GitHub does not provide shell access.
```
This confirmed that the SSH configuration successfully routes GitHub SSH connections through port 443.

## 21. Configure the GitHub Remote for SSH

The project repository was initially configured with an HTTPS remote.

The remote was changed to the SSH form:
```
git remote set-url origin git@github.com:SivanandaReddy-C/EEGNet-KV260-VitisAI.git
```
The remote was verified using:
```
git remote -v
```
Expected result:
```
origin  git@github.com:SivanandaReddy-C/EEGNet-KV260-VitisAI.git (fetch)
origin  git@github.com:SivanandaReddy-C/EEGNet-KV260-VitisAI.git (push)
```

## 22. Verify Git Push from WSL

The WSL repository was used to verify that GitHub operations were working correctly from the Linux environment.

Changes were staged using:
```
git add <file>
```
A commit was created using:
```
git commit -m "<commit message>"
```
The changes were pushed using:
```
git push origin main
```
The push completed successfully.

The repository status was then checked using:
```
git status
```
The result confirmed:
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```
This confirmed that the complete WSL-to-GitHub Git workflow was operational.

## 23. Create WSL-Native Project Workspace

Although the repository was initially available through the Windows filesystem, the project will use the Linux filesystem as the primary development location.

A Linux project directory was created using:
```
mkdir -p ~/projects
```
The directory corresponds to:
```
/home/vitisdev/projects
```
The directory was verified using:
```
ls -la ~/projects
```
At this stage, the directory was empty.

## 24. Clone the Repository into the WSL Filesystem

The repository was cloned directly from GitHub into the WSL-native filesystem.

The project directory was entered:
```
cd ~/projects
```
The repository was cloned using the SSH remote:
```
git clone git@github.com:SivanandaReddy-C/EEGNet-KV260-VitisAI.git
```
The repository was successfully cloned.

The resulting project location is:
```
/home/vitisdev/projects/EEGNet-KV260-VitisAI
```

## 25. Verify the WSL-Native Repository

The repository was opened using:
```
cd ~/projects/EEGNet-KV260-VitisAI
```
The repository location was verified using:
```
pwd
```
Result:
```
/home/vitisdev/projects/EEGNet-KV260-VitisAI
```
The GitHub remote was verified using:
```
git remote -v
```
Result:
```
origin  git@github.com:SivanandaReddy-C/EEGNet-KV260-VitisAI.git (fetch)
origin  git@github.com:SivanandaReddy-C/EEGNet-KV260-VitisAI.git (push)
```
The repository status was checked using:
```
git status
```
Result:
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```
The project directory structure was verified using:
```
ls
```
The expected project directories were present:
```
benchmarking
compilation
datasets
deployment
docs
examples
images
models
quantization
scripts
setup
training
```

## 26. Final WSL Development Architecture

The WSL-native repository is now the primary development repository for the project.

The final architecture for the Linux development environment is:
```
Windows 11
    │
    ▼
   WSL2
    │
    ▼
Ubuntu 22.04.5 LTS
    │
    ▼
/home/vitisdev/projects/
    │
    ▼
EEGNet-KV260-VitisAI
    │
    ├── training/
    ├── models/
    ├── quantization/
    ├── compilation/
    ├── deployment/
    └── benchmarking/
```
GitHub is used as the central version-control repository:
```
WSL-native repository
        │
        │ Git + SSH
        │
        ▼
GitHub
```
The Windows-side copy:
```
D:\KV260_Workspace\EEGNet-KV260-VitisAI
```
is not the primary Linux development location.

The primary development location is:
```
/home/vitisdev/projects/EEGNet-KV260-VitisAI
```
## 27. WSL Setup Final Verification

The following items have now been completed:

 - WSL2 enabled
 - Virtual Machine Platform enabled
 - Ubuntu 22.04 LTS installed
 - Ubuntu user vitisdev created
 - Ubuntu 22.04.5 LTS verified
 - WSL2 kernel verified
 - x86_64 architecture verified
 - Windows filesystem access verified
 - WSL-to-Windows executable interoperability verified
 - WSL resources verified
 - Git installed and configured inside WSL
 - GitHub SSH key generated
 - GitHub SSH authentication verified
 - SSH port 22 limitation identified
 - GitHub SSH over port 443 configured
 - SSH configuration permissions verified
 - GitHub remote changed to SSH
 - Git push from WSL verified
 - WSL-native project directory created
 - Repository cloned into WSL-native filesystem
 - WSL-native repository verified

WSL Environment Status
```
READY
```
The WSL2 Ubuntu environment and WSL-native Git repository are ready for the next stage of the project.

### Next Step

The WSL2 Linux environment has been established and verified.

The Linux-side Git environment, GitHub SSH authentication, and WSL-native project workspace are documented in Sections 16–27 of this document.

The primary project repository is now:

```text
/home/vitisdev/projects/EEGNet-KV260-VitisAI
```