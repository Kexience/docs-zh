---
source_url: https://java.testcontainers.org/modules/pinecone/
source_hash: sha256:68496f1ddcba2fb9b9070f9f4b419b67467c902216c382f470c4c9385f0afb7f
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Pinecone 模块

用于 [Pinecone Local](https://github.com/orgs/pinecone-io/packages/container/package/pinecone-local) 的 Testcontainers 模块。

## PineconeLocalContainer 的使用示例

你可以在任何 Java 应用程序中使用以下方式启动 Pinecone 容器实例：

**Pinecone 容器**

```java
PineconeLocalContainer container = new PineconeLocalContainer("ghcr.io/pinecone-io/pinecone-local:v0.7.0")
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-pinecone:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-pinecone</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
