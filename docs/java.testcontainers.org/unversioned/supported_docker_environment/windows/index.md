---
source_url: https://java.testcontainers.org/supported_docker_environment/windows/
source_hash: sha256:e3a139ce146f912ef9d62993001a5c86899b16907d8fbf7491124f8b623f8282
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Windows

## 前提条件

- 需要安装 [Docker for Windows](https://docs.docker.com/docker-for-windows/)
- 已确认 Docker 版本 17.06 可在带有 Hyper-V 的 Windows 10 上正常工作。
- Testcontainers 支持通过命名管道与 Docker for Windows 上的 Docker 进行通信。
- 从 Windows 10 2004 开始支持 WSL2 后端。（**Beta**）
- Windows Server 2019 上的 Docker 目前**不受支持**（另请参见[此 issue](https://github.com/testcontainers/testcontainers-java/issues/2960)）。

## 限制

以下功能不可用或无法正常工作，因此请确保不要使用它们，或谨慎使用。此列表可能并不完整。

### MySQL 容器

- 由于安全措施，MySQL 服务器会阻止加载自定义配置文件（ini-script）（[功能说明链接](../../modules/databases/index.md#using-an-init-script-from-a-file)）

### Windows Container on Windows (WCOW)

- 目前不支持 WCOW，因为 Testcontainers 在某些任务中使用辅助 Linux 容器，而在撰写本文时，Docker for Windows 不支持混合引擎模式。

## WSL2 后端

使用带有 WSL2 后端的 Docker for Windows 应该可以开箱即用。

但是，WSL/WSL2 中存在一个[已知问题](https://github.com/microsoft/WSL/issues/4694)，会影响某些较旧的 Docker 镜像。目前建议的解决方法是在 WSL2 内核中启用 vsyscall 模拟：

```
[wsl2]
kernelCommandLine = vsyscall=emulate
```

## Windows Subsystem for Linux (WSL)

Testcontainers 支持在 Windows Subsystem for Linux（*[**WSL**](https://docs.microsoft.com/en-us/windows/wsl/about)*）中与 Docker for Windows 通信。需要以下额外配置步骤：

- 在不使用 **TLS** 的情况下，通过 tcp 端口 `2375` 暴露 Docker for Windows 守护进程。*（右键单击任务栏上的 Docker for Windows 图标，点击设置并进入 `General`）*。
- 在 **WSL** shell 中将 `DOCKER_HOST` 环境变量设置为 `tcp://localhost:2375`。建议将此添加到你的 `~/.bashrc` 文件中，以便每次打开终端时都可用。
- **可选** - 仅在需要卷时：
   在 **WSL** shell 中，修改 `/ect/wsl.conf` 文件，将 Windows 驱动器挂载到 `/` 而不是 `/mnt/`。*（此步骤后需要重启）*。
   请记得在 Docker for Windows 中共享你将用于存储卷的驱动器。*（右键单击任务栏上的 Docker for Windows 图标，点击设置并进入 `Shared Drives`）*。

有关在 **WSL** 中运行 Docker 的更多信息，请参见[此处](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly)。

## 报告问题

请在[此处](https://github.com/testcontainers/testcontainers-java/issues)报告与 Testcontainers Windows 构建相关的任何问题，并务必注明你是在 Windows 上使用的。
