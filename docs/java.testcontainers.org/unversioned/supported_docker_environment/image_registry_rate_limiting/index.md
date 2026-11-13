---
source_url: https://java.testcontainers.org/supported_docker_environment/image_registry_rate_limiting/
source_hash: sha256:eb68bfc7a771ddfd3d153c01d033132ca74ead9615814e18caee376c23373d8e
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 镜像仓库速率限制

自 2020 年 11 月起，Docker Hub 的拉取操作受到速率限制。由于 Testcontainers 使用 Docker Hub 上的标准镜像，部分用户可能会遇到这些速率限制，应采取相应的缓解措施。

目前建议的缓解措施记录在[此 issue](https://github.com/testcontainers/testcontainers-java/issues/3099) 中。

## Testcontainers 使用了哪些镜像？

截至当前版本的 Testcontainers（2.0.5）：

- 测试直接使用的每个镜像
- Testcontainers 自身为支持功能而拉取的镜像：
  - [`testcontainers/ryuk`](https://hub.docker.com/r/testcontainers/ryuk) - 执行容器的故障安全清理，始终需要（除非[禁用 Ryuk](../../features/configuration/index.md#disabling-ryuk)）
  - [`alpine`](https://hub.docker.com/_/alpine) - 用于在启动时检查镜像是否可以拉取，始终需要（除非[禁用启动检查](../../features/configuration/index.md#disabling-the-startup-checks)）
  - [`testcontainers/sshd`](https://hub.docker.com/r/testcontainers/sshd) - 如果[将主机端口暴露给容器](../../features/networking/index.md#exposing-host-ports-to-the-container)则需要
  - [`testcontainers/vnc-recorder`](https://hub.docker.com/r/testcontainers/vnc-recorder) - 如果使用 [Webdriver 容器](../../modules/webdriver_containers/index.md)并使用屏幕录制功能则需要
  - [`docker/compose`](https://hub.docker.com/r/docker/compose) - 如果使用 [Docker Compose](../../modules/docker_compose/index.md) 则需要
  - [`alpine/socat`](https://hub.docker.com/r/alpine/socat) - 如果使用 [Docker Compose](../../modules/docker_compose/index.md) 则需要
