---
source_url: https://java.testcontainers.org/features/configuration/
source_hash: sha256:1c6c825bfd3cdb29f84b1783ba3c5608a6492409c8a6bc6f389679f98b4c5bc6
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 自定义配置

如果你的环境需要，可以覆盖部分默认属性。

## 配置位置

配置会从多个位置加载。属性按以下顺序生效：

1. 环境变量
2. 用户主目录下的 `.testcontainers.properties`。示例位置：
   **Linux:**`/home/myuser/.testcontainers.properties`
   **Windows:**`C:/Users/myuser/.testcontainers.properties`
   **macOS:**`/Users/myuser/.testcontainers.properties`
3. classpath 上的 `testcontainers.properties`。

请注意，使用环境变量时，配置属性名应全部大写并以下划线分隔，且以 `TESTCONTAINERS_` 开头——例如 `checks.disable` 会变成 `TESTCONTAINERS_CHECKS_DISABLE`。

classpath 上的 `testcontainers.properties` 文件可能存在于本地代码库中（例如 `src/test/resources` 目录下），也可能存在于你使用的库依赖中。所有这类配置文件的内容都会被合并。如果存在键冲突，则取值依据是以下顺序中第一个找到的值：

- 'local' classpath（即文件在 classpath 上的 URL 以 `file:` 开头），然后
- 其他 classpath 位置（即 JAR 文件）——按*路径的字母顺序*处理，以保证顺序确定。

## 禁用启动检查

> **checks.disable = [true|false]**

在运行任何容器之前，Testcontainers 会执行一组启动检查，以确保你的环境配置正确。通常它们看起来像这样：

```
        ℹ︎ Checking the system...
        ✔ Docker version should be at least 1.6.0
        ✔ File should be mountable
        ✔ A port exposed by a docker container should be accessible
```

这需要几秒钟，但如果你想加快测试速度，在一切配置妥当之后可以禁用这些检查。在 `$HOME/.testcontainers.properties` 中加入 `checks.disable=true` 即可完全禁用它们。

## 自定义镜像

> **注意**
>
> 这种做法不推荐且已废弃，此处记录仅为完整起见。通过配置覆盖单个镜像名的做法可能会在 2021 年被移除。有关从其他镜像仓库拉取镜像的其他替换策略，请参见[镜像名替换](../image_name_substitution/index.md)。

Testcontainers 使用公共 Docker 镜像来执行启动检查、VNC 录制等操作。有些公司不允许使用 Docker Hub，你可以覆盖 `*.image` 属性，改用私有镜像仓库中的镜像来绕过这一限制。

> **ryuk.container.image = testcontainers/ryuk:0.3.3** 用于对容器执行故障安全清理，且始终为必需（除非[禁用了 Ryuk](#disabling-ryuk)）
>
> **tinyimage.container.image = alpine:3.17**
>  用于检查启动时能否拉取镜像，且始终为必需（除非[禁用了启动检查](#disabling-the-startup-checks)）
>
> **sshd.container.image = testcontainers/sshd:1.4.0**
>  当[将主机端口暴露给容器](../networking/index.md#exposing-host-ports-to-the-container)时为必需
>
> **vncrecorder.container.image = testcontainers/vnc-recorder:1.3.0** 被 Testcontainers 的 Selenium 集成中的 VNC 录制器使用
>
> **socat.container.image = alpine/socat**
>  **compose.container.image = docker/compose:1.8.0**
>  使用 [Docker Compose](../../modules/docker_compose/index.md) 时为必需
>
> **kafka.container.image = confluentinc/cp-kafka**
>  被 KafkaContainer 使用
>
> **localstack.container.image = localstack/localstack**
>  被 LocalStack 使用
>
> **pulsar.container.image = apachepulsar/pulsar:2.2.0**
>  被 Apache Pulsar 使用

## 自定义 Ryuk 资源回收器

> **ryuk.container.image = testcontainers/ryuk:0.3.3** 资源回收器负责移除容器，并在 JVM 关闭时自动清理已停止的容器
>
> **ryuk.container.privileged = true** 在某些环境中 ryuk 必须以特权模式启动才能正常工作（--privileged 标志）

### 禁用 Ryuk

Ryuk 必须以特权容器方式启动。
 如果你的环境已经在执行结束后自动清理容器，但不允许启动特权容器，可以把 `TESTCONTAINERS_RYUK_DISABLED` **环境变量**设置为 `true`，从而关闭 Ryuk 容器。

> **提示**
>
> 请注意，除非你用 `kill -9` 终止 JVM 进程，否则 Testcontainers 仍会在 JVM 关闭时执行清理。

## 自定义镜像拉取行为

> **pull.timeout = 120** 默认情况下，如果拉取耗时超过该时长（秒），Testcontainers 会超时
>
> **pull.pause.timeout = 30** 默认情况下，如果拉取看起来停滞（没有数据传输）超过该时长（秒），Testcontainers 会中止镜像的拉取。

## 自定义客户端 ping 行为

> **client.ping.timeout = 10** 指定 Testcontainers 在放弃当前策略并尝试下一种策略（如适用）之前，尝试连接 Docker 客户端以获取有效客户端信息的最长时间（秒）。

## 自定义 Docker 主机检测

Testcontainers 会尝试检测 Docker 环境，并自动完成全部配置。

但有时需要进行定制。Testcontainers 会遵循以下**环境变量**：

> **DOCKER_HOST** = unix:///var/run/docker.sock
>  参见 [Docker 环境变量](https://docs.docker.com/engine/reference/commandline/cli/#environment-variables)
>
> **TESTCONTAINERS_DOCKER_SOCKET_OVERRIDE**
>  Docker socket 的路径。被 Ryuk、Docker Compose 以及其他一些需要执行 Docker 操作的容器使用。
>  示例：`/var/run/docker-alt.sock`
>
> **TESTCONTAINERS_HOST_OVERRIDE**
>  暴露端口所使用的 Docker 主机。
>  示例：`docker.svc.local`

对于高级用户，可以通过 `~/.testcontainers.properties` 中的**配置**来设置 Docker 主机连接。请注意，这些设置要求使用 `EnvironmentAndSystemPropertyClientProviderStrategy`。下面的示例展示了具体用法：

```properties
docker.client.strategy=org.testcontainers.dockerclient.EnvironmentAndSystemPropertyClientProviderStrategy
docker.host=tcp\://my.docker.host\:1234     # Equivalent to the DOCKER_HOST environment variable. Colons should be escaped.
docker.tls.verify=1                         # Equivalent to the DOCKER_TLS_VERIFY environment variable
docker.cert.path=/some/path                 # Equivalent to the DOCKER_CERT_PATH environment variable
```

此外，你可以通过指定以下内容来停用该行为：

```properties
dockerconfig.source=autoIgnoringUserProperties # 'auto' by default
```
