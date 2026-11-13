---
source_url: https://java.testcontainers.org/features/networking/
source_hash: sha256:3ee557fe333eb76551aaf78cf16c1137b186bf37a5d0f752614a53814bcf2c46
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# 网络与容器通信

## 将容器端口暴露给主机

通常，你会希望从运行在测试“主机”机器上的测试进程连接到容器。例如，你可能正在测试一个需要连接后端或数据存储容器的类。

一般来说，每个需要的端口都必须显式暴露。例如，我们可以按如下方式指定一个或多个端口：

**暴露端口**

```java
public GenericContainer<?> container = new GenericContainer<>(
    DockerImageName.parse("testcontainers/helloworld:1.1.0")
)
    .withExposedPorts(8080, 8081)
    .withLogConsumer(new Slf4jLogConsumer(log));
```

请注意，这个暴露的端口号是从*容器的视角*来看的。

*从主机的视角*来看，Testcontainers 实际上会把它暴露在一个随机的空闲端口上。这是设计使然，目的是避免与本地运行的软件发生端口冲突，也避免并行测试运行之间的端口冲突。

由于存在这一层间接映射，因此有必要在运行时向 Testcontainers 查询实际映射的端口。可以使用 `getMappedPort` 方法来完成，它接收原始（容器）端口作为参数：

**在运行时获取实际端口**

```java
Integer firstMappedPort = container.getMappedPort(8080);
Integer secondMappedPort = container.getMappedPort(8081);
```

> **Warning**
>
> 由于随机端口映射发生在容器启动期间，因此调用 `getMappedPort` 时容器必须已经处于运行状态。你可能需要确保测试中各组件的启动顺序能够满足这一点。

为了方便起见，还提供了 `getFirstMappedPort` 方法，适用于容器只暴露一个端口这种相当常见的场景：

**获取第一个映射端口**

```java
Integer firstMappedPort = container.getFirstMappedPort();
```

## 获取容器主机地址

在使用本地 Docker 守护进程运行时，暴露的端口通常可以通过 `localhost` 访问。不过，在某些 CI 环境中，它们可能需要通过其他主机地址访问。

因此，Testcontainers 提供了一个便捷方法，用于获取主机机器应当用来访问容器的地址。

**获取容器主机地址**

```java
String ipAddress = container.getHost();
```

在构造地址时，通常建议将 `getHost` 和 `getMappedPort` 一起使用——例如：

**获取容器主机地址和映射端口**

```java
String address = container.getHost() + ":" + container.getMappedPort(8080);
```

> **Tip**
>
> `getHost()` 是 `getContainerIpAddress()` 的替代方法，并返回相同的结果。`getContainerIpAddress()` 的命名被认为容易引起混淆，最终将被弃用。

## 将主机端口暴露给容器

在某些情况下，需要从容器向主机机器上正在监听的套接字发起网络连接。原生 Docker 在跨平台支持这种模式方面能力有限。不过，Testcontainers 可以实现这一点。

在这个示例中，假设 `localServerPort` 是我们测试主机机器上的一个端口，该端口上运行着一个服务器（例如 Web 应用）。

我们需要告诉 Testcontainers 准备将这个端口暴露给容器：

**暴露主机端口**

```java
Testcontainers.exposeHostPorts(localServerPort);
```

> **Warning**
>
> 请注意，上述命令应当在容器启动*之前*调用，但要在主机上的服务器启动*之后*调用。
> 另外，也可以使用 `container.withAccessToHost(true)` 来强制启用主机访问机制（你仍然需要调用 `exposeHostPorts` 来让端口可用）。

完成上述操作后，我们就可以从启动的任何容器中访问这个端口。从容器的视角来看，主机名将是 `host.testcontainers.internal`，端口值与 `localServerPort` 相同。

例如，这里我们为本地 Web 应用构造一个 HTTP URL，并让 Selenium 容器从中获取页面：

**从容器访问已暴露的主机端口**

```java
final String rootUrl = String.format("http://host.testcontainers.internal:%d/", localServerPort);

final RemoteWebDriver webDriver = new RemoteWebDriver(this.browser.getSeleniumAddress(), new ChromeOptions());
webDriver.get(rootUrl);
```

## 高级网络

Docker 允许你创建自定义网络，并将容器放置在一个或多个网络中。这样，联网的容器之间可以直接通信，而无需通过主机暴露端口。在 Testcontainers 中，你同样可以做到这一点。

> **Warning**
>
> 请注意，Testcontainers 目前只允许一个容器加入单个网络。

**创建自定义网络**

```java
try (
    Network network = Network.newNetwork();
    GenericContainer<?> foo = new GenericContainer<>(TestImages.TINY_IMAGE)
        .withNetwork(network)
        .withNetworkAliases("foo")
        .withCommand(
            "/bin/sh",
            "-c",
            "while true ; do printf 'HTTP/1.1 200 OK\\n\\nyay' | nc -l -p 8080; done"
        );
    GenericContainer<?> bar = new GenericContainer<>(TestImages.TINY_IMAGE)
        .withNetwork(network)
        .withCommand("top")
) {
    foo.start();
    bar.start();

    String response = bar.execInContainer("wget", "-O", "-", "http://foo:8080").getStdout();
    assertThat(response).as("received response").isEqualTo("yay");
}
```
