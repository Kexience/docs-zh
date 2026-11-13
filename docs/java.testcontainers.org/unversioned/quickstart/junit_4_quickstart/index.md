---
source_url: https://java.testcontainers.org/quickstart/junit_4_quickstart/
source_hash: sha256:53836cf48f4986c656616212783a246f495c6f5adb059eaffe48e74b7edf9d26
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# JUnit 4 快速入门

将 Testcontainers 添加到你的项目非常容易——让我们通过一个简单的示例来看看具体怎么做。

假设我们有一个依赖 Redis 的简单程序，并且希望为它添加一些测试。在这个假想的程序中，有一个 `RedisBackedCache` 类，它把数据存储在 Redis 中。

你可以看到一个在不使用 Testcontainers 的情况下可能为它编写的示例测试：

**使用 Testcontainers 之前的测试代码**

```java
public class RedisBackedCacheIntTestStep0 {

    private RedisBackedCache underTest;

    @Before
    public void setUp() {
        // Assume that we have Redis running locally?
        underTest = new RedisBackedCache("localhost", 6379);
    }

    @Test
    public void testSimplePutAndGet() {
        underTest.put("test", "example");

        String retrieved = underTest.get("test");
        assertThat(retrieved).isEqualTo("example");
    }
}
```

请注意，现有测试存在一个问题——它依赖于本地安装的 Redis，这对测试可靠性来说是一个危险信号。如果我们能确保每个开发者和 CI 机器都安装了 Redis，这样或许可行，但否则就会失败。如果我们尝试并行运行测试，也可能遇到问题，例如测试之间的状态泄漏或端口冲突。

让我们从这里开始，看看如何使用 Testcontainers 来改进这个测试：

## 1. 将 Testcontainers 添加为 test 作用域的依赖

首先，按如下方式将 Testcontainers 添加为依赖：

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

## 2. 让 Testcontainers 在测试期间运行一个 Redis 容器

只需将以下内容添加到测试类的主体中：

**JUnit 4 Rule**

```java
@Rule
public GenericContainer redis = new GenericContainer(DockerImageName.parse("redis:6-alpine"))
    .withExposedPorts(6379);
```

`@Rule` 注解会告诉 JUnit 在测试生命周期中的各个事件发生时通知该字段。在这个例子中，我们的 rule 对象是一个 Testcontainers `GenericContainer`，它被配置为使用 Docker Hub 上的特定 Redis 镜像，并暴露一个端口。

如果我们按原样运行测试，那么无论实际测试结果如何，我们都会看到日志显示 Testcontainers：

- 在测试方法运行前被激活
- 发现并快速检测了本地 Docker 环境
- 在必要时拉取镜像
- 启动一个新容器并等待其就绪
- 在测试结束后关闭并删除容器

## 3. 确保我们的代码能够与容器通信

在使用 Testcontainers 之前，我们可能会在测试中硬编码类似 `localhost:6379` 的地址。

Testcontainers 会为它启动的每个容器使用*随机端口*，但在运行时很容易获取实际端口。我们可以在测试的 `setUp` 方法中完成这件事，用来配置被测组件：

**获取映射端口**

```java
String address = redis.getHost();
Integer port = redis.getFirstMappedPort();

// Now we have an address and port for Redis, no matter where it is running
underTest = new RedisBackedCache(address, port);
```

> **Tip**
>
> 请注意，我们还通过 `redis.getHost()` 向 Testcontainers 获取容器的实际地址，而不是硬编码 `localhost`。`localhost` 在某些环境中可能有效，但在其他环境中可能无效——例如在你当前或未来的 CI 环境中可能无法使用。因此，**避免硬编码**地址，改用 `getHost()`。

## 4. 运行测试！

就是这样！

让我们看看完整的测试类，了解为了使用 Testcontainers 并运行起来，我们只需要添加多么少的代码：

**RedisBackedCacheIntTest**

```java
public class RedisBackedCacheIntTest {

    private RedisBackedCache underTest;

    // rule {
    @Rule
    public GenericContainer redis = new GenericContainer(DockerImageName.parse("redis:6-alpine"))
        .withExposedPorts(6379);

    // }

    @Before
    public void setUp() {
        String address = redis.getHost();
        Integer port = redis.getFirstMappedPort();

        // Now we have an address and port for Redis, no matter where it is running
        underTest = new RedisBackedCache(address, port);
    }

    @Test
    public void testSimplePutAndGet() {
        underTest.put("test", "example");

        String retrieved = underTest.get("test");
        assertThat(retrieved).isEqualTo("example");
    }
}
```
