---
source_url: https://java.testcontainers.org/modules/databases/cockroachdb/
source_hash: sha256:4091d9a3aad1d2ce7d4c17cba459fcbe47a76bd09c12e7705217408f16bc3a51
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# CockroachDB

用于 [CockroachDB](https://hub.docker.com/r/cockroachdb/cockroach) 的 Testcontainers 模块

## 使用示例

你可以在任意 Java 应用中通过以下方式启动一个 CockroachDB 容器实例：

**容器定义**

```java
CockroachContainer cockroach = new CockroachContainer("cockroachdb/cockroach:v26.1.1")
```

有关所有关系型数据库容器类型通用的文档和用法，请参阅 [数据库容器](../index.md)。

### Testcontainers JDBC URL

`jdbc:tc:cockroach:v21.2.3:///databasename`

有关文档请参阅 [JDBC](../jdbc/index.md)。

## 将本模块添加到项目依赖中

在你的 `pom.xml`/`build.gradle` 文件中添加以下依赖：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-cockroachdb:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-cockroachdb</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **提示**
>
> 添加此 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你需要确保项目中还包含合适的数据库驱动作为依赖。
