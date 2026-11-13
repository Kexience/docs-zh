---
source_url: https://java.testcontainers.org/modules/kafka/
source_hash: sha256:69d507e5c1d19c235a82878f4c95050c3d4613e0b66b2c801b366a3f72a569ae
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Kafka

Testcontainers 可用于自动实例化和管理 [Apache Kafka](https://kafka.apache.org) 容器。

目前支持两种不同的 Kafka 镜像：

- `org.testcontainers.kafka.ConfluentKafkaContainer` 支持 [confluentinc/cp-kafka](https://hub.docker.com/r/confluentinc/cp-kafka/)
- `org.testcontainers.kafka.KafkaContainer` 支持 [apache/kafka](https://hub.docker.com/r/apache/kafka/) 和 [apache/kafka-native](https://hub.docker.com/r/apache/kafka-native/)

> **注意**
>

> `org.testcontainers.containers.KafkaContainer` 已弃用。请根据所使用的镜像，改用 `org.testcontainers.kafka.ConfluentKafkaContainer` 或 `org.testcontainers.kafka.KafkaContainer`。

## 优势

- 只需一行代码即可运行单节点 Kafka 实例
- 无需管理 Kafka 所需的外部 Zookeeper 安装

## 示例

### 使用 org.testcontainers.kafka.KafkaContainer

创建一个 `KafkaContainer` 以在测试中使用：

**创建 KafkaContainer**

```java
KafkaContainer kafka = new KafkaContainer("apache/kafka-native:3.8.0")
```

现在，你的测试或运行在你机器上的任何其他进程都可以通过以下 bootstrap server 地址访问正在运行的 Kafka broker：

**Bootstrap Servers**

```java
kafka.getBootstrapServers()
```

### 使用 org.testcontainers.kafka.ConfluentKafkaContainer

> **注意**
>

> 与版本为 `7.4.0` 及更高版本的 `confluentinc/cp-kafka` 镜像兼容。

创建一个 `ConfluentKafkaContainer` 以在测试中使用：

**创建 ConfluentKafkaContainer**

```java
ConfluentKafkaContainer kafka = new ConfluentKafkaContainer("confluentinc/cp-kafka:7.4.0")
```

## 选项

### 使用 Kraft 模式

> **注意**
>

> 仅适用于 `org.testcontainers.containers.KafkaContainer`

KRaft 模式在 3.3.1（confluentinc/cp-kafka:7.3.x）中被宣布为可用于生产环境。

**Kraft 模式**

```java
KafkaContainer kafka = new KafkaContainer(DockerImageName.parse("confluentinc/cp-kafka:7.4.0")).withKraft()
```

有关更多详细信息，请参阅[版本互操作性矩阵](https://docs.confluent.io/platform/current/installation/versions-interoperability.html)。

### 注册监听器

在某些场景下需要额外的监听器，因为 consumer/producer 可能位于同一网络中的另一个容器中，或位于另一个进程中，其连接端口与默认暴露端口不同。例如 [Toxiproxy](../toxiproxy/index.md)。

**注册额外监听器**

```java
KafkaContainer kafka = new KafkaContainer("apache/kafka-native:3.8.0")
    .withListener("kafka:19092")
    .withNetwork(network);
```

在同一网络中定义的容器：

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

使用新注册监听器的客户端：

**通过新监听器生产/消费**

```java
kcat.execInContainer("kcat", "-b", "kafka:19092", "-t", "msgs", "-P", "-l", "/data/msgs.txt");
String stdout = kcat
    .execInContainer("kcat", "-b", "kafka:19092", "-C", "-t", "msgs", "-c", "1")
    .getStdout();
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-kafka:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-kafka</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
