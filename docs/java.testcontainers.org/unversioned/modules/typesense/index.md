---
source_url: https://java.testcontainers.org/modules/typesense/
source_hash: sha256:de3d7be171eb70bd7585b1f1cc0d5057809297139911215654a1b8c4f9bcfb82
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Typesense 模块

用于 [Typesense](https://hub.docker.com/r/typesense/typesense) 的 Testcontainers 模块。

## TypesenseContainer 的使用示例

你可以在任何 Java 应用程序中使用以下方式启动 Typesense 容器实例：

**Typesense 容器**

```java
TypesenseContainer typesense = new TypesenseContainer("typesense/typesense:27.1")
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-typesense:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-typesense</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
