---
source_url: https://java.testcontainers.org/modules/chromadb/
source_hash: sha256:21aba92c9b6ca2c9beab6c0269c109d3f82ecc48ec8173a29c19b5e9e381e5f0
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# ChromaDB

[ChromaDB](https://registry.hub.docker.com/r/chromadb/chroma) 的 Testcontainers 模块。

## ChromaDB 使用示例

你可以在任意 Java 应用中使用以下方式启动 ChromaDB 容器实例：

**默认 ChromaDB 容器**

```java
ChromaDBContainer chroma = new ChromaDBContainer("chromadb/chroma:0.4.23")
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-chromadb:2.0.5"
```

**Maven**

```xml
<dependency>
<groupId>org.testcontainers</groupId>
<artifactId>testcontainers-chromadb</artifactId>
<version>2.0.5</version>
<scope>test</scope>
</dependency>
```
