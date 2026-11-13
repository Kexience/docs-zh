---
source_url: https://java.testcontainers.org/modules/activemq/
source_hash: sha256:76a986e9de628dcd0153ca021d16b1d2f14a68ae8e3e38bbf3f692d34a64ee1d
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# ActiveMQ

[ActiveMQ](https://hub.docker.com/r/apache/activemq) 和 [Artemis](https://hub.docker.com/r/apache/artemis) 的 Testcontainers 模块。

## ActiveMQContainer 使用示例

你可以在任意 Java 应用中使用以下方式启动 ActiveMQ Classic 容器实例：

**默认 ActiveMQ 容器**

```java
ActiveMQContainer activemq = new ActiveMQContainer("apache/activemq:5.18.7")
```

使用自定义凭据：

**设置自定义凭据**

```java
ActiveMQContainer activemq = new ActiveMQContainer("apache/activemq:5.18.7")
    .withUser("testcontainers")
    .withPassword("testcontainers")
```

## ArtemisContainer 使用示例

你可以在任意 Java 应用中使用以下方式启动 ActiveMQ Artemis 容器实例：

**默认 Artemis 容器**

```java
ArtemisContainer artemis = new ArtemisContainer("apache/activemq-artemis:2.32.0-alpine")
```

使用自定义凭据：

**设置自定义凭据**

```java
ArtemisContainer artemis = new ArtemisContainer("apache/activemq-artemis:2.32.0-alpine")
    .withUser("testcontainers")
    .withPassword("testcontainers")
```

允许匿名登录：

**允许匿名登录**

```java
ArtemisContainer artemis = new ArtemisContainer("apache/activemq-artemis:2.32.0-alpine")
    .withEnv("ANONYMOUS_LOGIN", "true")
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-activemq:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-activemq</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
