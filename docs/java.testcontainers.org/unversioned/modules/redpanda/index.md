---
source_url: https://java.testcontainers.org/modules/redpanda/
source_hash: sha256:f2f695759de8c2159d40047b1c0711be19daef54daf8bd0ce5e59a4163152d18
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Redpanda 模块

Testcontainers 可用于自动实例化和管理 [Redpanda](https://redpanda.com/) 容器。更确切地说，Testcontainers 使用 [Redpanda](https://hub.docker.com/r/redpandadata/redpanda) 的官方 Docker 镜像。

> **Note**
>

> 此模块使用 `docker.redpanda.com/redpandadata/redpanda` 提供的功能。

## 示例

创建一个 `Redpanda` 以在测试中使用：

**创建 Redpanda**

```java
RedpandaContainer container = new RedpandaContainer("docker.redpanda.com/redpandadata/redpanda:v23.1.2")
```

现在，你的测试或在机器上运行的任何其他进程都可以使用以下 bootstrap server 地址访问正在运行的 Redpanda broker：

**Bootstrap Servers**

```java
container.getBootstrapServers()
```

Redpanda 还提供了 schema registry 实现。与 Redpanda broker 类似，你可以使用以下 schema registry 地址进行访问：

**Schema Registry**

```java
container.getSchemaRegistryAddress()
```

你还可以通过以下方式启用 Redpanda 的安全功能：

**启用安全功能**

```java
RedpandaContainer redpanda = new RedpandaContainer("docker.redpanda.com/redpandadata/redpanda:v23.1.7")
    .enableAuthorization()
    .enableSasl()
    .withSuperuser("superuser-1")
```

可以通过以下方式创建超级用户：

**注册超级用户**

```java
String adminUrl = String.format("%s/v1/security/users", redpanda.getAdminAddress());
RestAssured
    .given()
    .contentType("application/json")
    .body("{\"username\": \"superuser-1\", \"password\": \"test\", \"algorithm\": \"SCRAM-SHA-256\"}")
    .post(adminUrl)
    .then()
    .statusCode(200);
```

下面是创建 `AdminClient` 的示例：

**创建 Admin Client**

```java
AdminClient adminClient = AdminClient.create(
    ImmutableMap.of(
        AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG,
        bootstrapServer,
        AdminClientConfig.SECURITY_PROTOCOL_CONFIG,
        "SASL_PLAINTEXT",
        SaslConfigs.SASL_MECHANISM,
        "SCRAM-SHA-256",
        SaslConfigs.SASL_JAAS_CONFIG,
        "org.apache.kafka.common.security.scram.ScramLoginModule required username=\"superuser-1\" password=\"test\";"
    )
);
```

在某些场景下需要额外的监听器，因为消费者/生产者可能是同一网络中的另一个容器，或是连接端口与默认暴露端口 `9092` 不同的其他进程。例如 [Toxiproxy](../toxiproxy/index.md)。

**注册额外的监听器**

```java
RedpandaContainer kafka = new RedpandaContainer("docker.redpanda.com/redpandadata/redpanda:v23.1.7")
    .withListener("kafka:19092")
    .withNetwork(network);

    ⋯

RedpandaContainer kafka = new RedpandaContainer("docker.redpanda.com/redpandadata/redpanda:v23.1.7")
    .withListener("kafka:19092", () -> socat.getHost() + ":" + socat.getMappedPort(2000))
    .withNetwork(network)
```

定义在同一网络中的容器：

**创建 kcat 容器**

```java
GenericContainer<?> kcat = new GenericContainer<>("confluentinc/cp-kcat:7.9.0")
    .withCreateContainerCmdModifier(cmd -> {
        cmd.withEntrypoint("sh");
    })
    .withCopyToContainer(Transferable.of("Message produced by kcat"), "/data/msgs.txt")
    .withNetwork(network)
    .withCommand("-c", "tail -f /dev/null")
```

使用新注册的监听器的客户端：

**通过新监听器进行生产/消费**

```java
kcat.execInContainer("kcat", "-b", "kafka:19092", "-t", "msgs", "-P", "-l", "/data/msgs.txt");
String stdout = kcat
    .execInContainer("kcat", "-b", "kafka:19092", "-C", "-t", "msgs", "-c", "1")
    .getStdout();

    ⋯

String bootstrapServers = String.format("%s:%s", socat.getHost(), socat.getMappedPort(2000));
testKafkaFunctionality(bootstrapServers);
```

以下示例展示了如何在 `RedpandaContainer` 中将代理注册为新的监听器：

使用 `SocatContainer` 创建代理

**创建代理**

```java
SocatContainer socat = new SocatContainer().withNetwork(network).withTarget(2000, "kafka", 19092);
```

注册监听器和广播监听器

**注册监听器**

```java
RedpandaContainer kafka = new RedpandaContainer("docker.redpanda.com/redpandadata/redpanda:v23.1.7")
    .withListener("kafka:19092", () -> socat.getHost() + ":" + socat.getMappedPort(2000))
    .withNetwork(network)
```

使用新注册的监听器的客户端：

**通过新监听器进行生产/消费**

```java
String bootstrapServers = String.format("%s:%s", socat.getHost(), socat.getMappedPort(2000));
testKafkaFunctionality(bootstrapServers);
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-redpanda:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-redpanda</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
