---
source_url: https://java.testcontainers.org/modules/toxiproxy/
source_hash: sha256:91d0b64fefe1de077def44ffc4673ff426f47408e3da21e4e8087c08e49ca61f
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Toxiproxy 模块

用于 Shopify 的 [Toxiproxy](https://github.com/Shopify/toxiproxy) 的 Testcontainers 模块。此 TCP 代理可用于模拟网络故障条件。

你可以模拟以下网络故障：

- Java 代码与容器之间的故障，非常适合测试客户端代码的弹性功能
- 容器之间的故障，用于测试多容器系统的弹性和涌现行为
- 如有需要，还可以模拟 Java 代码/容器与外部资源（非 Docker 化！）之间的故障，适用于并非所有依赖都可以/已经 Docker 化的场景

Testcontainers 的 Toxiproxy 支持使弹性功能能够作为隔离的开发/CI 测试的一部分轻松验证。这使得可以更早地测试弹性功能，并覆盖更广泛的故障条件。

## 使用示例

Toxiproxy 容器可以放置在测试代码与容器之间，也可以放置在容器与容器之间。在这两种场景中，都需要在同一个 Docker 网络上创建 `ToxiproxyContainer` 实例，如下所示：

**创建 Toxiproxy 容器**

```java
// Create a common docker network so that containers can communicate
@AutoClose
public Network network = Network.newNetwork();

// The target container - this could be anything
@AutoClose
public GenericContainer<?> redis = new GenericContainer<>("redis:6-alpine")
    .withExposedPorts(6379)
    .withNetwork(network)
    .withNetworkAliases("redis");

// Toxiproxy container, which will be used as a TCP proxy
@AutoClose
public ToxiproxyContainer toxiproxy = new ToxiproxyContainer("ghcr.io/shopify/toxiproxy:2.5.0")
    .withNetwork(network);
```

接下来，需要指示 Toxiproxy 开始代理连接。如有需要，每个 `ToxiproxyContainer` 都可以代理到多个目标容器。

我们按如下方式进行：

**开始代理到目标容器的连接**

```java
final ToxiproxyClient toxiproxyClient = new ToxiproxyClient(toxiproxy.getHost(), toxiproxy.getControlPort());
final Proxy proxy = toxiproxyClient.createProxy("redis", "0.0.0.0:8666", "redis:6379");
```

要从测试代码（在主机上）通过 Toxiproxy 建立到目标容器的连接，我们需要获取 **Toxiproxy 的**代理主机 IP 和端口：

**获取代理的主机和端口**

```java
final String ipAddressViaToxiproxy = toxiproxy.getHost();
final int portViaToxiproxy = toxiproxy.getMappedPort(8666);
```

被测代码应连接到此代理的主机 IP 和端口。

> **Note**
>

> 目前，`ToxiProxyContainer` 将从 8666 开始预留 31 个端口。

其他容器应连接到此代理的主机和端口。

完成上述操作后，就可以通过 `proxy.toxics()` 对象触发故障条件（“Toxics”）：

- `bandwidth` - 将连接限制为每秒最大千字节数。
- `latency` - 为通过代理的所有数据添加延迟。延迟等于 `latency +/- jitter`。
- `slicer` - 将 TCP 数据切分成小块，可选择在每个切片“数据包”之间添加延迟。
- `slowClose` - 将 TCP 套接字的关闭延迟到经过 `delay` 毫秒之后。
- `timeout` - 阻止所有数据通过，并在 `timeout` 后关闭连接。如果 `timeout` 为 `0`，连接不会关闭，数据将被延迟直到移除该 toxic。
- `limitData` - 当传输的数据超过限制时关闭连接。

有关可用 Toxics 的完整详细信息，请参阅 [Toxiproxy 文档](https://github.com/Shopify/toxiproxy#toxics)。

作为一个示例，我们可以按如下方式为代理连接引入延迟和随机抖动：

**为连接添加延迟**

```java
proxy.toxics()
    .latency("latency", ToxicDirection.DOWNSTREAM, 1_100)
    .setJitter(100);
// from now on the connection latency should be from 1000-1200 ms.
```

此外，我们还可以禁用代理以模拟网络连接的完全中断：

**切断连接**

```java
proxy.toxics().bandwidth("CUT_CONNECTION_DOWNSTREAM", ToxicDirection.DOWNSTREAM, 0);
proxy.toxics().bandwidth("CUT_CONNECTION_UPSTREAM", ToxicDirection.UPSTREAM, 0);

// for example, expect failure when the connection is cut
assertThat(
    catchThrowable(() -> {
        jedis.get("somekey");
    })
)
    .as("calls fail when the connection is cut")
    .isInstanceOf(JedisConnectionException.class);

proxy.toxics().get("CUT_CONNECTION_DOWNSTREAM").remove();
proxy.toxics().get("CUT_CONNECTION_UPSTREAM").remove();

jedis.close();
// and with the connection re-established, expect success
assertThat(jedis.get("somekey"))
    .as("access to the container works OK after re-establishing the connection")
    .isEqualTo("somevalue");
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-toxiproxy:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-toxiproxy</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

## 致谢

此模块的灵感来自 [hotels.com 的一篇博客文章](https://medium.com/hotels-com-technology/i-dont-know-about-resilience-testing-and-so-can-you-b3c59d80012d)。
