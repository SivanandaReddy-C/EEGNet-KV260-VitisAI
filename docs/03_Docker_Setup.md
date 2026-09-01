### Docker Installation Verification

Docker Desktop was installed on the Windows host using the WSL 2 backend.

The Docker installation was verified from Windows Command Prompt using:

```cmd
docker --version
```
The installed Docker version is:

```text
Docker version 29.7.2, build a7dca6
```

### Docker Engine Verification

After starting Docker Desktop, the Docker Engine was verified from Windows Command Prompt using:

```cmd
docker info
```

The Docker Engine was successfully detected and returned the following relevant information:

```text
Server Version: 29.7.2
Operating System: Docker Desktop
OSType: linux
Architecture: x86_64
CPUs: 28
Total Memory: 31.18GiB
Kernel Version: 6.6.114.1-microsoft-standard-WSL2
```

### Initial Docker Engine Verification

Immediately after Docker Desktop installation, `docker --version` worked, but the first `docker info` attempt failed because the Docker Engine had not yet been started.

The error indicated that the Docker Desktop Linux engine could not be reached.

Docker Desktop was then launched manually. Its status subsequently showed:

```text
Engine running
```

### WSL Distribution Verification

Before configuring Docker Desktop WSL integration, the installed WSL distributions were verified from Windows Command Prompt using:

```cmd
wsl --list --verbose
```
The result was:
```text
NAME            STATE      VERSION
* Ubuntu-22.04  Running    2
  docker-desktop Running   2
```

The asterisk (*) indicates that Ubuntu-22.04 is the default WSL distribution.

This confirmed that Ubuntu 22.04 was running under WSL 2 and was the default distribution for the system.

### Docker Desktop WSL Integration

Docker Desktop provides WSL integration so that Docker commands can be used directly from the Ubuntu WSL environment.

The WSL integration settings were opened from:
```text
Docker Desktop
→ Settings
→ Resources
→ WSL Integration
```
The option:
```text
Enable integration with my default WSL distro
```
was enabled.

Since Ubuntu-22.04 was already the default WSL distribution, it was not necessary to select it separately under the additional distributions.

The Docker Engine was then restarted using:
```text
Apply & Restart Engine
```
After the restart, Docker Desktop continued to show:
```text
Engine running
```

### Initial Docker Access from WSL

After enabling WSL integration, Docker was tested from the Ubuntu WSL terminal.

The Docker version was checked using:
```bash
docker --version
```
The result was:
```text
Docker version 29.7.2, build a7dca6
```
This confirmed that the Docker CLI was available inside the WSL Ubuntu environment.

The Docker Engine was then tested using:
```bash
docker info
```
The initial attempt returned a permission error:
```text
permission denied while trying to connect to the Docker API
at unix:///var/run/docker.sock
```
This indicated that the Docker CLI was available, but the current WSL user did not yet have effective permission to access the Docker socket.

### Diagnose Docker Socket Permission

The Docker socket was inspected using:
```bash
ls -l /var/run/docker.sock
```
The result showed:
```text
srw-rw---- 1 root docker ... /var/run/docker.sock
```
This showed that the Docker socket was owned by:
```text
root:docker
```
with permissions allowing access to the owner and the docker group.

The current user's groups were checked using:
```bash
id
```
The docker group was not present in the active session's supplementary groups.

The existence and membership of the Docker group were then checked using:
```bash
getent group docker
```
The result was:
```text
docker:x:1001:vitisdev
```
This confirmed that the vitisdev user was already a member of the docker group, but the existing WSL session had not yet picked up the updated group membership.

### Restart WSL to Apply Docker Group Membership

The WSL environment was completely stopped from Windows Command Prompt using:
```cmd
wsl --shutdown
```
Ubuntu 22.04 was then started again using:
```cmd
wsl -d Ubuntu-22.04
```
After starting a new WSL session, the user's group membership was refreshed.

The Docker Engine was tested again using:
```bash
docker info
```
This time the command completed successfully.

The relevant Docker Engine information was:
```text
Server Version: 29.7.2
Operating System: Docker Desktop
OSType: linux
Architecture: x86_64
CPUs: 28
Total Memory: 31.18GiB
Kernel Version: 6.6.114.1-microsoft-standard-WSL2
```
This confirmed that the vitisdev user could access the Docker Engine directly from WSL without using sudo.

### Final Docker Installation Test

The Docker installation and WSL integration were finally tested by running a Docker container:
```bash
docker run hello-world
```
Docker successfully downloaded the hello-world:latest image from Docker Hub and created a container from the image.

The command returned:
```text
Hello from Docker!
```
This message shows that your installation appears to be working correctly.

The successful execution confirmed that:
```text
Docker CLI is available from WSL.
WSL can communicate with the Docker Engine.
Docker can access Docker Hub.
Docker can pull container images.
Docker can create and run containers.
Docker Desktop WSL 2 integration is functioning correctly.
```