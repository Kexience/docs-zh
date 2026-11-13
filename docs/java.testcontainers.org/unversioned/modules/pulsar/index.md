---
source_url: https://java.testcontainers.org/modules/pulsar/
source_hash: sha256:550e7d73729dfc3ccb7e1901719a98c1e823275d213df7b67dac453dfd60cd1c
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Pulsar 模块

Testcontainers 可用于自动创建 [Apache Pulsar](https://pulsar.apache.org) 容器，无需依赖外部服务。

它基于官方的 Apache Pulsar Docker 镜像，建议阅读[官方指南](https://pulsar.apache.org/docs/next/getting-started-docker/)。

## 示例

创建一个 `PulsarContainer` 以在测试中使用：

**创建 Pulsar 容器**

```java
PulsarContainer pulsar = new PulsarContainer("apachepulsar/pulsar:3.0.0");
```

然后你可以获取 broker 和 admin URL：

**获取 broker 和 admin URL**

```java
final String pulsarBrokerUrl = pulsar.getPulsarBrokerUrl();
final String httpServiceUrl = pulsar.getHttpServiceUrl();
```

## 选项

### 配置

如果需要设置 Pulsar 配置变量，你可以使用原生 API，并以 `PULSAR_PREFIX_` 作为前缀来设置每个变量。

例如，如果你想启用 `brokerDeduplicationEnabled`：

**设置配置变量**

```java
PulsarContainer pulsar = new PulsarContainer(PULSAR_IMAGE)
    .withEnv("PULSAR_PREFIX_brokerDeduplicationEnabled", "true");
```

### Pulsar IO

如果需要测试 Pulsar IO 框架，你可以启用 Pulsar Functions Worker：

**创建带有 Functions Worker 的 Pulsar 容器**

```java
PulsarContainer pulsar = new PulsarContainer(DockerImageName.parse("apachepulsar/pulsar:3.0.0"))
    .withFunctionsWorker();
```

### Pulsar 事务

如果需要测试 Pulsar 事务，你可以启用事务功能：

**创建启用事务的 Pulsar 容器**

```java
PulsarContainer pulsar = new PulsarContainer(PULSAR_IMAGE).withTransactions();
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-pulsar:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-pulsar</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
