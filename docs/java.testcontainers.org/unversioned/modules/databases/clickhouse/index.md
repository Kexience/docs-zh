---
source_url: https://java.testcontainers.org/modules/databases/clickhouse/
source_hash: sha256:5ee7154726693f3306d80e239e6df0c0c13301b96f996d717a36c559bd51fa1d
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# ClickHouse

用于 [ClickHouse](https://hub.docker.com/r/clickhouse/clickhouse-server) 的 Testcontainers 模块

## 使用示例

你可以在任意 Java 应用中通过以下方式启动一个 ClickHouse 容器实例：

**容器定义**

```java
ClickHouseContainer clickhouse = new ClickHouseContainer("clickhouse/clickhouse-server:21.11-alpine")
```

### Testcontainers JDBC URL

`jdbc:tc:clickhouse:18.10.3:///databasename`

有关文档请参阅 [JDBC](../jdbc/index.md)。

## 将本模块添加到项目依赖中

在你的 `pom.xml`/`build.gradle` 文件中添加以下依赖：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-clickhouse:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-clickhouse</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **提示**
>
> 添加此 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你需要确保项目中还包含合适的数据库驱动作为依赖。
