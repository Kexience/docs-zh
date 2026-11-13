---
source_url: https://java.testcontainers.org/supported_docker_environment/continuous_integration/gitlab_ci/
source_hash: sha256:024f9df17de9a41c79237ae5ae65d5038c0e43b70258cecf7d4deda593a4cf04
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# GitLab CI

## 使用 Docker socket 的示例

如果你安装了自己的 GitlabCI runner，使用 Docker 执行器，并且在 runner 配置中挂载了 `/var/run/docker.sock`，则适用此方式。

以下是 runner 配置示例：

```toml
[[runners]]
  name = "MACHINE_NAME"
  url = "https://gitlab.com/"
  token = "GENERATED_GITLAB_RUNNER_TOKEN"
  executor = "docker"
  [runners.docker]
    tls_verify = false
    image = "docker:latest"
    privileged = false
    disable_entrypoint_overwrite = false
    oom_kill_disable = false
    disable_cache = false
    volumes = ["/var/run/docker.sock:/var/run/docker.sock", "/cache"]
    shm_size = 0
```

另外，请在使用 Testcontainers 的 GitlabCI 流水线定义（`.gitlab-ci.yml`）中包含以下内容：

```yml
variables:
  TESTCONTAINERS_HOST_OVERRIDE: "<ip-docker-host>"
```

需要配置环境变量 `TESTCONTAINERS_HOST_OVERRIDE`，否则将使用错误的 IP 地址来解析 Docker 主机，这很可能导致测试失败。对于 Windows 和 MacOS，请使用 `host.docker.internal`。

## 使用 DinD (Docker-in-Docker) 的示例

为了在 Gitlab CI 流水线中使用 Testcontainers，你需要将作业作为 Docker 容器运行（参见[在 Docker 内运行的模式](../dind_patterns/index.md)）。因此，请编辑你的 `.gitlab-ci.yml`，加入 [Docker-In-Docker 服务](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#use-docker-in-docker-workflow-with-docker-executor)（`docker:dind`），并将 `DOCKER_HOST` 变量设置为 `tcp://docker:2375`，将 `DOCKER_TLS_CERTDIR` 设置为空字符串。

注意：当前的 docker 版本（已在 20.10.9 上验证）在 docker API 绑定到网络地址但未启用 TLS 保护时，会有意延迟启动。为避免此延迟，需要使用参数 `--tls=false` 启动 docker 进程。否则，在一开始就访问 docker API 的作业可能会失败。

以下是一个使用 gradle 执行测试的 `.gitlab-ci.yml` 示例：

```yml
# DinD service is required for Testcontainers
services:
  - name: docker:dind
    # explicitly disable tls to avoid docker startup interruption
    command: ["--tls=false"]

variables:
  # Instruct Testcontainers to use the daemon of DinD, use port 2375 for non-tls connections.
  DOCKER_HOST: "tcp://docker:2375"
  # Instruct Docker not to start over TLS.
  DOCKER_TLS_CERTDIR: ""
  # Improve performance with overlayfs.
  DOCKER_DRIVER: overlay2

test:
 image: gradle:5.0
 stage: test
 script: ./gradlew test
```
