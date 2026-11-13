---
source_url: https://java.testcontainers.org/modules/databases/postgres/
source_hash: sha256:b27ab526197c7cd8a55cd43522aa14e1a3e762e1c4214443a31db6f27a7bd047
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# PostgreSQL 模块

用于 [PostgreSQL](https://hub.docker.com/_/postgres) 的 Testcontainers 模块

## 使用示例

你可以在任何 Java 应用中通过以下方式启动 PostgreSQL 容器实例：

**创建容器**

```java
PostgreSQLContainer postgres = new PostgreSQLContainer("postgres:9.6.12")
```

有关所有关系型数据库容器类型通用的文档和用法，请参阅[数据库容器](../index.md)。

### Testcontainers JDBC URL

- PostgreSQL: `jdbc:tc:postgresql:9.6.8:///databasename`
- PostGIS: `jdbc:tc:postgis:9.6-2.5:///databasename`
- TimescaleDB: `jdbc:tc:timescaledb:2.1.0-pg13:///databasename`
- PGvector: `jdbc:tc:pgvector:pg16:///databasename`

相关文档请参阅 [JDBC](../jdbc/index.md)。

## 兼容镜像

`PostgreSQLContainer` 也可以与以下镜像一起使用：

- [pgvector/pgvector](https://hub.docker.com/r/pgvector/pgvector)

**使用 pgvector**

```java
PostgreSQLContainer pgvector = new PostgreSQLContainer("pgvector/pgvector:pg16")
```

- [postgis/postgis](https://registry.hub.docker.com/r/postgis/postgis)

**使用 PostGIS**

```java
PostgreSQLContainer postgis = new PostgreSQLContainer(
    DockerImageName.parse("postgis/postgis:16-3.4-alpine").asCompatibleSubstituteFor("postgres")
)
```

- [timescale/timescaledb](https://hub.docker.com/r/timescale/timescaledb)

**使用 TimescaleDB**

```java
PostgreSQLContainer timescaledb = new PostgreSQLContainer(
    DockerImageName.parse("timescale/timescaledb:2.14.2-pg16").asCompatibleSubstituteFor("postgres")
)
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-postgresql:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-postgresql</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **Hint**
>
> 添加这个 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你应确保项目中还包含合适的数据库驱动作为依赖。
