---
source_url: https://java.testcontainers.org/modules/docker_model_runner/
source_hash: sha256:37323fc995140caff1d5387af33a06d9bdb755317aeb9dc90c558056e3e8642a
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Docker Model Runner

该模块可帮助连接由 Docker Desktop 4.40.0 提供的 [Docker Model Runner](https://docs.docker.com/desktop/features/model-runner/)。

## DockerModelRunner 使用示例

你可以在任意 Java 应用中使用以下方式启动 Docker Model Runner 代理容器实例：

**创建 DockerModelRunnerContainer**

```java
DockerModelRunnerContainer dmr = new DockerModelRunnerContainer("alpine/socat:1.7.4.3-r0")
```

### 拉取模型

拉取模型非常简单：

**拉取模型**

```java
DockerModelRunnerContainer dmr = new DockerModelRunnerContainer("alpine/socat:1.7.4.3-r0")
    .withModel(modelName)
```

## 将此模块添加到项目依赖

*Docker Model Runner 支持是核心 Testcontainers 库的一部分。*

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
