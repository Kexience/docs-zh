---
source_url: https://java.testcontainers.org/modules/solace/
source_hash: sha256:e6faaa7b2573404fcb17b5a713ff0159fb94a994b4cce7a3a7e16c2ce80ada9d
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Solace 模块

此模块帮助使用 Testcontainers 运行 [Solace PubSub+](https://solace.com/products/event-broker/software/)。

请注意，它基于[官方 Docker 镜像](https://hub.docker.com/r/solace/solace-pubsub-standard)。

## 使用示例

你可以在任何 Java 应用程序中使用以下方式启动 Solace 容器实例：

**使用简单认证配置 Solace 容器**

```java
SolaceContainer solaceContainer = new SolaceContainer("solace/solace-pubsub-standard:10.25.0")
    .withCredentials("user", "pass")
    .withTopic(TOPIC.getName(), Service.SMF)
    .withVpn("test_vpn")
```

**使用 SSL 配置 Solace 容器**

```java
SolaceContainer solaceContainer = new SolaceContainer("solace/solace-pubsub-standard:10.25.0")
    .withClientCert(
        MountableFile.forClasspathResource("solace.pem"),
        MountableFile.forClasspathResource("rootCA.crt")
    )
    .withTopic(TOPIC.getName(), Service.SMF_SSL)
```

**使用 Solace 容器**

```java
Session session = createSession(
    solaceContainer.getUsername(),
    solaceContainer.getPassword(),
    solaceContainer.getOrigin(Service.AMQP)
);
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-solace:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-solace</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
