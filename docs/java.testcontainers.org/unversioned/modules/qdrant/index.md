---
source_url: https://java.testcontainers.org/modules/qdrant/
source_hash: sha256:631edbab146e55d113e95fe99cf821e9214fdbb454cd7a501888dc9bb6d7ed3b
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Qdrant 模块

用于 [Qdrant](https://registry.hub.docker.com/r/qdrant/qdrant) 的 Testcontainers 模块。

## Qdrant 的使用示例

你可以在任何 Java 应用程序中使用以下方式启动 Qdrant 容器实例：

**默认 QDrant 容器**

```java
QdrantContainer qdrant = new QdrantContainer("qdrant/qdrant:v1.7.4")
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-qdrant:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-qdrant</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
