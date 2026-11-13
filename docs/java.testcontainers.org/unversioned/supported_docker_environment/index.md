---
source_url: https://java.testcontainers.org/supported_docker_environment/
source_hash: sha256:cbb73e8aee598c53153d0ee39246a297e13c4c17863fc83e2b537a38f0052499
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 支持的 Docker 环境

## 概述

要运行基于 Testcontainers 的测试，你需要一个与 Docker API 兼容的容器运行时，例如使用 [Testcontainers Cloud](https://www.testcontainers.cloud/) 或在本地安装 Docker。在开发过程中，Testcontainers 会针对 Linux 上较新版本的 Docker，以及 Mac 和 Windows 上的 Docker Desktop 进行积极测试。这些 Docker 环境会被 Testcontainers 自动检测并使用，无需任何额外配置。

也可以将 Testcontainers 配置为与其他容器运行时配合使用。使用免费的 [Testcontainers Desktop](https://testcontainers.com/desktop/) 应用可以处理大部分手动配置。如果在不使用 Testcontainers Desktop 的情况下使用这些替代方案，有时可能需要进行一些手动配置（有关特定运行时的说明请参见下文，通用配置机制请参见[自定义 Docker 主机检测](../features/configuration/index.md#customizing-docker-host-detection)）。替代容器运行时不会在主要开发流程中进行积极测试，因此并非所有 Testcontainers 功能都可用。如果你对自己环境的配置细节或其是否支持运行基于 Testcontainers 的测试有更多疑问，请通过 [Slack](https://slack.testcontainers.org/) 联系 Testcontainers 团队及 Testcontainers 社区的其他用户。

## Colima

为了让 testcontainers 与 [colima](https://github.com/abiosoft/colima) 配合运行，需要设置以下环境变量

```bash
colima start --network-address
export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock
export TESTCONTAINERS_HOST_OVERRIDE=$(colima ls -j | jq -r '.address')
export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"
```

## Podman

为了让 testcontainers 与 [podman](https://podman.io/) 配合运行，需要设置以下环境变量

MacOS：

```bash
export DOCKER_HOST=unix://$(podman machine inspect --format '{{.ConnectionInfo.PodmanSocket.Path}}')
export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock
```

Linux：

```bash
export DOCKER_HOST=unix://${XDG_RUNTIME_DIR}/podman/podman.sock
```

如果你在 rootless 模式下运行 Podman，请确保添加以下行以禁用 Ryuk：

```bash
export TESTCONTAINERS_RYUK_DISABLED=true
```

> **Note**
>

> 在 1.19.0 版本之前，rootful 模式需要 `export TESTCONTAINERS_RYUK_PRIVILEGED=true`。从 1.19.0 开始，这不再是必需的。

## Rancher Desktop

为了让 testcontainers 与 [Rancher Desktop](https://rancherdesktop.io/) 配合运行，需要设置以下环境变量。

如果你在 MacOS (M1) 机器上以管理员身份运行 Rancher Desktop：

使用 QEMU 模拟

```bash
export TESTCONTAINERS_HOST_OVERRIDE=$(rdctl shell ip a show rd0 | awk '/inet / {sub("/.*",""); print $2}')
```

使用 VZ 模拟

```bash
export TESTCONTAINERS_HOST_OVERRIDE=$(rdctl shell ip a show vznat | awk '/inet / {sub("/.*",""); print $2}')
```

如果你在 MacOS (M1) 机器上未以管理员身份运行 Rancher Desktop：

使用 VZ 模拟

```bash
export DOCKER_HOST=unix://$HOME/.rd/docker.sock
export TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE=/var/run/docker.sock
export TESTCONTAINERS_HOST_OVERRIDE=$(rdctl shell ip a show vznat | awk '/inet / {sub("/.*",""); print $2}')
```

## Docker 环境发现

Testcontainers 将按以下顺序尝试使用不同策略连接到 Docker 守护进程：

- 环境变量：
  - `DOCKER_HOST`
  - `DOCKER_TLS_VERIFY`
  - `DOCKER_CERT_PATH`
- 默认值：
  - `DOCKER_HOST=https://localhost:2376`
  - `DOCKER_TLS_VERIFY=1`
  - `DOCKER_CERT_PATH=~/.docker`
- 如果安装了 Docker Machine，则使用找到的*第一个*机器的 docker machine 环境。要使此方式生效，Docker Machine 需要在 PATH 中。
- 如果你要在容器内运行测试，请先阅读[在 Docker 容器内运行测试的模式](./continuous_integration/dind_patterns/index.md)。

## Docker 镜像仓库认证

Testcontainers 将按以下顺序尝试使用所提供的配置对镜像仓库进行认证：

- 环境变量：
  - `DOCKER_AUTH_CONFIG`
- Docker 配置
  - 位于 `DOCKER_CONFIG` 指定的位置，或 `{HOME}/.docker/config.json`
