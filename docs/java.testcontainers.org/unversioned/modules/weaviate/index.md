---
source_url: https://java.testcontainers.org/modules/weaviate/
source_hash: sha256:985cd23ab511dcf18c015fc233b9b6500f42f441ca8c0a5bdadc71c07a232c35
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Weaviate 模块

用于 [Weaviate](https://hub.docker.com/r/semitechnologies/weaviate) 的 Testcontainers 模块。

## WeaviateContainer 的使用示例

你可以在任何 Java 应用程序中使用以下方式启动 Weaviate 容器实例：

**默认 Weaviate 容器**

```java
WeaviateContainer weaviate = new WeaviateContainer("cr.weaviate.io/semitechnologies/weaviate:1.32.0")
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-weaviate:2.0.5"
```

**Maven**

```xml
<dependency>
<groupId>org.testcontainers</groupId>
<artifactId>testcontainers-weaviate</artifactId>
<version>2.0.5</version>
<scope>test</scope>
</dependency>
```
