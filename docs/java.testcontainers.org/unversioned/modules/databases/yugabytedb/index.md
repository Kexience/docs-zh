---
source_url: https://java.testcontainers.org/modules/databases/yugabytedb/
source_hash: sha256:92d6f1cd6b7fa59bd64e69774fd105c8f034509a1182ae66ebe0993f522a028a
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# YugabyteDB 模块

用于 [YugabyteDB](https://hub.docker.com/r/yugabytedb/yugabyte) 的 Testcontainers 模块

有关所有数据库容器类型通用的文档和用法，请参阅[数据库容器](../index.md)。

YugabyteDB 支持两种 API。

- Yugabyte Structured Query Language [YSQL](https://docs.yugabyte.com/latest/api/ysql/) 是一个完全关系型的 API，基于 PostgreSQL 代码构建
- Yugabyte Cloud Query Language [YCQL](https://docs.yugabyte.com/latest/api/ycql/) 是一个半关系型 SQL API，起源于 Cassandra Query Language

## 使用示例

### YSQL API

**创建 YSQL 容器**

```java
final YugabyteDBYSQLContainer ysqlContainer = new YugabyteDBYSQLContainer(
    "yugabytedb/yugabyte:2.14.4.0-b26"
)
```

### Testcontainers JDBC URL

`jdbc:tc:yugabyte:2.14.4.0-b26:///databasename`

相关文档请参阅 [JDBC](../jdbc/index.md)。

### YCQL API

**创建 YCQL 容器**

```java
final YugabyteDBYCQLContainer ycqlContainer = new YugabyteDBYCQLContainer(
    "yugabytedb/yugabyte:2.14.4.0-b26"
)
    .withUsername("cassandra")
    .withPassword("cassandra")
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-yugabytedb:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-yugabytedb</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **Hint**
>
> 添加这个 Testcontainers 库 JAR 不会自动为你的项目添加 Yugabytedb 驱动 JAR。如果你计划使用它，应确保项目中包含 Yugabytedb 驱动作为依赖。有关说明，请参阅驱动页面 [YSQL](https://docs.yugabyte.com/latest/integrations/jdbc-driver/) 和 [YCQL](https://docs.yugabyte.com/latest/reference/drivers/ycql-client-drivers/)。
