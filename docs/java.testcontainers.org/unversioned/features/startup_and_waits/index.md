---
source_url: https://java.testcontainers.org/features/startup_and_waits/
source_hash: sha256:5df4a367e1654a400e9fa35f3d47d9d6dfa0c3fed6b659d8e65e048d898189be
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 启动与等待

> **Wait strategies vs Startup strategies**
>
> **Wait strategy（等待策略）：** 容器是否处于对测试有用的状态。通常可以粗略理解为“我们能否通过网络与这个容器通信”。不过，其中有不少变体和细微差别。
>
> **Startup strategy（启动策略）：** 容器是否达到了期望的运行状态。*几乎在所有情况下*，这仅仅意味着“等待容器进入运行状态”——对于容器中的守护进程来说，这就是目标。有时我们需要等待容器进入运行状态后再退出——这就是“一次性启动”策略，只用于那些需要在容器中执行一次性命令而不是运行守护进程的场景。

## 等待策略

通常情况下，Testcontainers 会等待最多 60 秒，让容器的第一个已映射网络端口开始监听。

这个简单的检查提供了一个基础判断：容器是否已准备好可用。

**等待第一个暴露端口开始监听**

```java
public GenericContainer nginx = new GenericContainer(DockerImageName.parse("nginx:1.27.0-alpine3.19-slim")) //
    .withExposedPorts(80);
```

如果默认的 60 秒超时不够，可以使用 `withStartupTimeout()` 方法进行修改。

如果等待 TCP 端口监听不足以判断容器是否就绪，你可以将 `waitingFor()` 方法与其他 [`WaitStrategy`](http://static.javadoc.io/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/wait/strategy/WaitStrategy.html) 实现一起使用，如下所示。

### HTTP 等待策略示例

你可以选择等待某个 HTTP(S) 端点返回特定的状态码。

#### 等待 200 OK

```java
public GenericContainer nginxWithHttpWait = new GenericContainer(
    DockerImageName.parse("nginx:1.27.0-alpine3.19-slim")
)
    .withExposedPorts(80)
    .waitingFor(Wait.forHttp("/"));
```

HTTP 等待策略还支持多种变体，包括：

#### 等待多种可能的状态码

```java
Wait.forHttp("/")
    .forStatusCode(200)
    .forStatusCode(301);
```

#### 等待匹配谓词的状态码

**等待匹配谓词的状态码**

```java
Wait.forHttp("/all")
    .forStatusCodeMatching(it -> it >= 200 && it < 300 || it == 401);
```

#### 使用 TLS

```java
Wait.forHttp("/all")
    .usingTls();
```

### 健康检查等待策略示例

如果所使用的镜像支持 Docker 的 [Healthcheck](https://docs.docker.com/engine/reference/builder/#healthcheck) 特性，你可以直接利用容器的 `healthy` 状态作为等待条件：

```java
Wait.forHealthcheck();
```

### 日志输出等待策略

在某些情况下，容器的日志输出是判断其是否就绪的一种简单方式。例如，我们可以按如下方式等待容器日志中出现 `Ready` 消息：

```java
public GenericContainer containerWithLogWait = new GenericContainer(DockerImageName.parse("redis:6-alpine"))
    .withExposedPorts(6379)
    .waitingFor(Wait.forLogMessage(".*Ready to accept connections.*\\n", 1));
```

### 其他等待策略

更多选项请查看 [`Wait`](http://static.javadoc.io/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/wait/strategy/Wait.html) 便捷类，或 [`WaitStrategy`](http://static.javadoc.io/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/wait/strategy/WaitStrategy.html) 的各个子类。

如果这些选项都不能满足你的需求，你可以创建自己的 [`AbstractWaitStrategy`](http://static.javadoc.io/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/wait/strategy/AbstractWaitStrategy.html) 子类，并在 `waitUntilReady()` 中实现合适的等待机制。`GenericContainer.waitingFor()` 方法接受任何有效的 [`WaitStrategy`](http://static.javadoc.io/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/wait/strategy/WaitStrategy.html)。

## 启动检查策略

通常情况下，Testcontainers 会检查容器是否已进入运行状态且尚未退出。为此，它会对容器执行 inspect 操作并提取 state 参数。

所有逻辑都在 [`StartupCheckStrategy`](http://static.javadoc.io/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/startupcheck/StartupCheckStrategy.html) 的子类中实现。

### 运行中启动策略示例

这是默认使用的策略。Testcontainers 只检查容器是否正在运行。

由 [`IsRunningStartupCheckStrategy`](http://static.javadoc.io/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/startupcheck/IsRunningStartupCheckStrategy.html) 类实现。

### 一次性启动策略示例

该策略适用于只会短暂运行并自行退出的容器。因此，当容器以退出码 0 停止时，即视为成功。

**使用一次性启动策略**

```java
public GenericContainer<?> bboxWithOneShot = new GenericContainer<>(DockerImageName.parse("busybox:1.31.1"))
    .withCommand(String.format("echo %s", HELLO_TESTCONTAINERS))
    .withStartupCheckStrategy(
        new OneShotStartupCheckStrategy().withTimeout(Duration.ofSeconds(3))
    );
```

### 无限等待的一次性启动策略示例

一次性启动策略的一个变体，不设置超时限制。适用于容器启动过程包含长时间运行任务的场景。

这里需要假定容器最终会自行停止，并以成功或失败的退出码结束。

**使用无限等待的一次性启动策略**

```java
public GenericContainer<?> bboxWithIndefiniteOneShot = new GenericContainer<>(
    DockerImageName.parse("busybox:1.31.1")
)
    .withCommand("sh", "-c", String.format("sleep 5 && echo \"%s\"", HELLO_TESTCONTAINERS))
    .withStartupCheckStrategy(
        new IndefiniteWaitOneShotStartupCheckStrategy()
    );
```

### 最短运行时长启动策略示例

检查容器正在运行，并且已经运行了指定的最短时间。

**使用最短运行时长策略**

```java
public GenericContainer<?> bboxWithMinimumDuration = new GenericContainer<>(
    DockerImageName.parse("busybox:1.31.1")
)
    .withCommand("sh", "-c", String.format("sleep 5 && echo \"%s\"", HELLO_TESTCONTAINERS))
    .withStartupCheckStrategy(
        new MinimumDurationRunningStartupCheckStrategy(Duration.ofSeconds(1))
    );
```

### 其他启动策略

如果这些选项都不能满足你的需求，你可以创建自己的 [`StartupCheckStrategy`](http://static.javadoc.io/org.testcontainers/testcontainers/2.0.5/org/testcontainers/containers/startupcheck/StartupCheckStrategy.html) 子类，并在 `waitUntilStartupSuccessful()` 中实现合适的启动检查机制。或者你也可以保持原样，只实现 `checkStartupState(DockerClient dockerClient, String containerId)`，如果你仍希望周期性地检查状态的话。

## 依赖另一个容器

有时，一个容器依赖另一个容器先就绪，然后它自己才能启动。例如，数据库可能需要先启动，你的应用容器才能连接到它。你可以使用 `dependsOn` 方法声明一个容器依赖另一个容器：

**依赖另一个容器**

```java
public GenericContainer<?> redis = new GenericContainer<>("redis:6-alpine").withExposedPorts(6379);

@Rule
public GenericContainer<?> nginx = new GenericContainer<>("nginx:1.27.0-alpine3.19-slim")
    .dependsOn(redis)
    .withExposedPorts(80);
```
