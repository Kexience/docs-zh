---
source_url: https://java.testcontainers.org/supported_docker_environment/continuous_integration/dind_patterns/
source_hash: sha256:dd60a268c9afc9c2e7ad6d643e403254c608d91037b9056d75d6a5ee7c500352
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Docker-in-Docker 与 Docker wormhole 模式

## “Docker wormhole”模式 - 同级 Docker 容器

Testcontainers 本身可以在容器内部使用。这对于不同的 CI 场景非常有用，例如在 Jenkins 上在容器中运行所有内容，或使用基于 Docker 的 CI 工具（如 Drone）。

Testcontainers 会自动检测自己是否在容器内，如果是，它将使用默认网关的 IP，而不是“localhost”。

但是，如果你使用[卷映射](../../../features/files/index.md)，则需要额外配置。需要考虑以下几点：

- 必须通过卷挂载提供 docker socket
- “本地”源代码目录必须在运行 Testcontainers 的容器内以*相同路径*进行卷挂载，以便 Testcontainers 能够为其启动的容器设置正确的卷挂载。

### 仅使用 Docker 的示例

如果你仅使用 `docker run ...` 运行测试，请确保在命令中添加 `-v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock`，如下所示：

```bash
$ tree .
.
├── pom.xml
└── src
    └── test
        └── java
            └── MyTestWithTestcontainers.java

$ docker run -it --rm -v $PWD:$PWD -w $PWD -v /var/run/docker.sock:/var/run/docker.sock maven:3 mvn test
```

其中：

- `-v $PWD:$PWD` 会将当前目录作为卷添加到容器内
- `-w $PWD` 会将当前目录设置为该卷
- `-v /var/run/docker.sock:/var/run/docker.sock` 会映射 Docker socket

> **Note**
>

> 如果你使用的是 Docker Desktop，需要配置 `TESTCONTAINERS_HOST_OVERRIDE` 环境变量，使用 Docker Desktop 提供的特殊 DNS 名称 `host.docker.internal` 从容器内访问主机：`-e TESTCONTAINERS_HOST_OVERRIDE=host.docker.internal`

### Docker Compose 示例

使用 Docker Compose 也可以实现同样的效果：

```yaml
tests:
  image: maven:3
  stop_signal: SIGKILL
  stdin_open: true
  tty: true
  working_dir: $PWD
  volumes:
    - $PWD:$PWD
    - /var/run/docker.sock:/var/run/docker.sock
    # Maven cache (optional)
    - ~/.m2:/root/.m2
  command: mvn test
```

## Docker-in-Docker

虽然 Docker-in-Docker (DinD) 通常被认为是不得已而为之的手段，但在某些 CI 环境中它是必需的。

[Drone CI](../drone/index.md) 就是这样一个例子。Testcontainers 提供了一个用于 Drone 的 Docker-in-Docker 插件（构建镜像），可作为使用 DinD 设置其他类似测试的参考。
