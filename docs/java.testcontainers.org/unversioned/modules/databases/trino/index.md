---
source_url: https://java.testcontainers.org/modules/databases/trino/
source_hash: sha256:2919cd48a78a8a471d0665b96411afd06c6736fd5eb1c6afdca7e0fb5d51d658
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Trino 模块

用于 [Trino](https://hub.docker.com/r/trinodb/trino) 的 Testcontainers 模块

## 使用示例

你可以在任何 Java 应用中通过以下方式启动 Trino 容器实例：

**创建容器**

```java
TrinoContainer trino = new TrinoContainer("trinodb/trino:352")
```

有关所有数据库容器类型通用的文档和用法，请参阅[数据库容器](../index.md)。

### Testcontainers JDBC URL

`jdbc:tc:trino:352:///defaultname`

相关文档请参阅 [JDBC](../jdbc/index.md)。

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-trino:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-trino</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **Hint**
>
> 添加这个 Testcontainers 库 JAR 不会自动为你的项目添加 Trino JDBC 驱动 JAR。如果你计划使用它，应确保项目中包含 Trino JDBC 驱动作为依赖。有关说明，请参阅 [Trino 项目下载页面](https://trino.io/download.html)。
