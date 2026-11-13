---
source_url: https://java.testcontainers.org/modules/docker_compose/
source_hash: sha256:6de93a05dacef9db3b0ab3be17fd895ba7939015bb2d537b43850025904af081
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Docker Compose

## 优势

与通用容器支持类似，也可以运行在 `docker-compose.yml` 文件中指定的一组自定义服务。

这对于那些在开发或其他环境中已经使用 Docker Compose 来定义应用所依赖服务的项目尤其有用。

`ComposeContainer` 利用了 [Compose V2](https://www.docker.com/blog/announcing-compose-v2-general-availability/)，使得在测试中使用与开发环境相同的依赖变得非常容易。

## 示例

一个基于 `docker-compose.yml` 文件定义的 `ComposeContainer` 类，应该就足以启动测试所需的任意数量的服务：

**创建 ComposeContainer**

```java
public ComposeContainer environment = new ComposeContainer(
    DockerImageName.parse("docker:25.0.5"),
    new File("src/test/resources/composev2/compose-test.yml")
)
    .withExposedService("redis-1", REDIS_PORT)
    .withExposedService("db-1", 3306);
```

> **注意**
>
> 请确保服务名称使用 `-` 而不是 `_` 作为分隔符。

在此示例中，Docker Compose 文件应包含如下内容：

```yaml
services:
  redis:
    image: redis
  db:
    image: mysql:8.0.36
```

请注意，无需在 YAML 文件中定义要暴露的端口，因为这会妨碍该文件在其他上下文中的复用或引入。

相反，Testcontainers 会启动一个小型的 `ambassador` 容器，用于在由 Compose 管理的容器与测试可访问的端口之间进行代理。

## ComposeContainer 与 DockerComposeContainer

到目前为止，我们讨论的是支持 Docker Compose [version 2](https://www.docker.com/blog/announcing-compose-v2-general-availability/) 的 `ComposeContainer`。

另一方面，`DockerComposeContainer` 使用的是 Compose V1，Docker 已将其标记为已弃用。

这两个 API 非常相似，本页提供的大多数示例都可以应用于它们。

## 访问容器

`ComposeContainer` 提供了一些方法，用于确定测试如何与容器交互：

- `getServiceHost(serviceName, servicePort)` 返回容器监听的 IP 地址（通过 ambassador 容器）
- `getServicePort(serviceName, servicePort)` 返回已暴露端口的 Docker 映射端口（通过 ambassador 容器）

让我们使用此 API 创建可供测试访问 Redis 服务的 URL：

**访问服务的主机和端口**

```java
String serviceHost = environment.getServiceHost("redis-1", REDIS_PORT);
int serviceWithInstancePort = environment.getServicePort("redis-1", REDIS_PORT);
```

## 等待策略与启动超时

通常情况下，Testcontainers 会等待最多 60 秒，以等待每个已暴露容器的第一个映射网络端口开始监听。这一简单措施提供了对容器是否可用的基本检查。

存在重载的 `withExposedService` 方法，它们接受一个 `WaitStrategy`，我们可以借此为每个容器指定超时策略。

我们既可以使用 fluent API 创建[自定义策略](../../features/startup_and_waits/index.md)，也可以使用 `Wait` 类的静态工厂方法提供的现有策略之一。

例如，我们可以等待暴露的端口并设置自定义超时：

**等待暴露的端口并使用自定义超时**

```java
ComposeContainer compose = new ComposeContainer(
    DockerImageName.parse("docker:25.0.5"),
    new File("src/test/resources/composev2/compose-test.yml")
)
    .withExposedService(
        "redis-1",
        REDIS_PORT,
        Wait.forListeningPort().withStartupTimeout(Duration.ofSeconds(30))
    )
```

不言而喻，我们可以为 Docker Compose 配置中的每个服务定义不同的策略。

例如，我们的 Redis 容器可以等待 redis-cli 命令成功执行，而我们的 db 服务则等待特定的日志消息：

**等待自定义命令和日志消息**

```java
ComposeContainer compose = new ComposeContainer(
    DockerImageName.parse("docker:25.0.5"),
    new File("src/test/resources/composev2/compose-test.yml")
)
    .withExposedService("redis-1", REDIS_PORT, Wait.forSuccessfulCommand("redis-cli ping"))
    .withExposedService("db-1", 3306, Wait.forLogMessage(".*ready for connections.*\\n", 1))
```

## "Local Compose" 模式

我们可以覆盖 Testcontainers 的默认行为，使其使用本机上安装的 `docker-compose` 二进制文件。

这通常会带来更接近于在本地运行 *docker compose* 的体验，但前提是开发和 CI 机器上都需要安装 Docker Compose。

**在 "Local Compose" 模式下使用 ComposeContainer**

```java
compose =
    new ComposeContainer(COMPOSE_FILE)
```

## 构建工作目录

我们可以通过 `withCopyFilesInContainer` 选择应复制哪些文件：

**在 "Local Compose" 模式下使用 ComposeContainer**

```java
ComposeContainer environment = new ComposeContainer(
    DockerImageName.parse("docker:25.0.5"),
    new File("src/test/resources/compose-file-copy-inclusions/compose-test-only.yml")
)
    .withExposedService("app", 8080)
    .withCopyFilesInContainer("Dockerfile", "EnvVariableRestEndpoint.java", "test")
```

在此示例中，只有 Docker Compose 文件和 env 文件会被复制到将运行 Docker Compose 文件的容器中。
默认情况下，compose 文件所在目录中的所有文件都会被复制。

我们可以使用文件和目录引用。它们始终相对于 compose 文件所在的目录进行解析。

> **注意**
>
> 这可与 `DockerComposeContainer` 和 `ComposeContainer` 一起使用，但**仅适用于容器化 Compose 模式（不适用于 `Local Compose` 模式）**。

## 在 Docker Compose 中使用私有仓库

当 Docker Compose 在容器模式（非本地模式）下使用时，需要让它知道私有仓库的 Docker 设置。默认情况下，这些设置位于 `$HOME/.docker/config.json`。

有 3 种方式可以为 Docker Compose 指定 `config.json` 的位置：

- 使用 `DOCKER_CONFIG_FILE` 环境变量。

  `export DOCKER_CONFIG_FILE=/some/location/config.json`
- 使用 `dockerConfigFile` Java 属性

  `java -DdockerConfigFile=/some/location/config.json`
- 不指定任何内容。在这种情况下，如果存在默认位置 `$HOME/.docker/config.json`，将会使用它。

> **Docker Compose 与 Credential Store / Credential Helpers**
>
> 现代 Docker 倾向于使用 credential store/helper 机制来存储凭据，而不是将凭据存储在 Docker 的配置文件中。因此，你的 `config.json` 可能看起来像这样：
>
> 当在容器内运行时，Docker Compose 无法访问 Keychain，从而使该配置失效。要解决此问题，有两种选择：
>
> ##### 将 auths 放入配置文件
>
> 在其他位置创建一个包含真实认证密钥的 `config.json`，如下所示：
>
> 并使用上述前两种方法中的任意一种向 Testcontainers 指定该位置。
>
> ##### 使用 "local compose" 模式
>
> 上面提到的 [Local Compose 模式](#local-compose-mode) 将允许 Compose 直接访问 Docker 的认证系统（与手动运行 `docker-compose` CLI 的效果相同）。

```json
{
  "auths" : {
    "https://index.docker.io/v1/" : {
    }
  },
  "credsStore" : "osxkeychain"
}
```

```json
{
  "auths" : {
    "https://index.docker.io/v1/" : {
     "auth": "QWEADSZXC..."
    }
  },
  "credsStore" : "osxkeychain"
}
```

## 将此模块添加到项目依赖

*Docker Compose 支持是核心 Testcontainers 库的一部分。*

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
