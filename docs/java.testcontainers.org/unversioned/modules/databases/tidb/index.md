---
source_url: https://java.testcontainers.org/modules/databases/tidb/
source_hash: sha256:a902c18dec92a72bfbab21cc876905db34c674f9c3abe8b904dc2be807598c21
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# TiDB 模块

用于 [TiDB](https://hub.docker.com/r/pingcap/tidb) 的 Testcontainers 模块

## 使用示例

你可以在任何 Java 应用中通过以下方式启动 TiDB 容器实例：

**创建容器**

```java
TiDBContainer tidb = new TiDBContainer("pingcap/tidb:v6.1.0")
```

有关所有关系型数据库容器类型通用的文档和用法，请参阅[数据库容器](../index.md)。

### Testcontainers JDBC URL

`jdbc:tc:tidb:v6.1.0:///databasename`

相关文档请参阅 [JDBC](../jdbc/index.md)。

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-tidb:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-tidb</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **Hint**
>
> 添加这个 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你应确保项目中还包含合适的数据库驱动作为依赖。
