---
source_url: https://java.testcontainers.org/modules/databases/jdbc/
source_hash: sha256:939470727f84e37a2c3e5673991b2653c263e0a93d8c3892e937b1d84f1ba5b6
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# JDBC 数据库容器

你可以通过以下两种方式之一获取临时数据库：

- **使用经过特殊修改的 JDBC URL**：只需对系统的 JDBC URL 字符串进行非常简单的修改，Testcontainers 就会提供一个一次性的替代数据库，无需修改应用程序代码即可使用。
- **JUnit @Rule/@ClassRule**：此模式会在测试之前在容器中启动数据库，并在测试之后将其销毁。

## 通过 JDBC URL 方案启动的数据库容器

只要你的类路径中包含 Testcontainers 和相应的 JDBC 驱动，你就可以简单地修改常规 JDBC 连接 URL，以便在应用程序每次启动时获得一个全新的容器化数据库实例。

*注意：*

- *要使此功能正常工作，TC 需要在运行时位于应用程序的类路径中*
- *对于 Spring Boot（`2.3.0` 之前的版本），你需要手动指定驱动 `spring.datasource.driver-class-name=org.testcontainers.jdbc.ContainerDatabaseDriver`*

**原始 URL**：`jdbc:mysql://localhost:3306/databasename`

在 `jdbc:` 后插入 `tc:`，如下所示。请注意，主机名、端口和数据库名称将被忽略；你可以保持原样或将其设置为任意值。

> **注意**
>
> 从现在开始，我们将使用 `///`（无主机 URI）来强调 `host:port` 对并不重要。
>  从 Testcontainers 的角度来看，`jdbc:mysql:8.0.36://localhost:3306/databasename` 和 `jdbc:mysql:8.0.36:///databasename` 是相同的 URI。

> **警告**
>
> 如果你使用 JDBC URL 支持，则无需实例化容器实例——Testcontainers 会自动完成。

### JDBC URL 示例

#### 使用 ClickHouse

`jdbc:tc:clickhouse:18.10.3:///databasename`

#### 使用 CockroachDB

`jdbc:tc:cockroach:v21.2.3:///databasename`

#### 使用 CrateDB

`jdbc:tc:cratedb:5.2.3:///databasename`

#### 使用 DB2

`jdbc:tc:db2:11.5.0.0a:///databasename`

#### 使用 MariaDB

`jdbc:tc:mariadb:10.3.39:///databasename`

#### 使用 MySQL

`jdbc:tc:mysql:8.0.36:///databasename`

#### 使用 MSSQL Server

`jdbc:tc:sqlserver:2017-CU12:///databasename`

#### 使用 OceanBase

`jdbc:tc:oceanbasece:4.2.1-lts:///databasename`

#### 使用 Oracle

`jdbc:tc:oracle:21-slim-faststart:///databasename`

#### 使用 PostGIS

`jdbc:tc:postgis:9.6-2.5:///databasename`

#### 使用 PostgreSQL

`jdbc:tc:postgresql:9.6.8:///databasename`

#### 使用 QuestDB

`jdbc:tc:questdb:6.5.3:///databasename`

#### 使用 TimescaleDB

`jdbc:tc:timescaledb:2.1.0-pg13:///databasename`

#### 使用 PGVector

`jdbc:tc:pgvector:pg16:///databasename`

#### 使用 TiDB

`jdbc:tc:tidb:v6.1.0:///databasename`

#### 使用 Timeplus

`jdbc:tc:timeplus:2.3.21:///databasename`

#### 使用 Trino

`jdbc:tc:trino:352://localhost/memory/default`

#### 使用 YugabyteDB

`jdbc:tc:yugabyte:2.14.4.0-b26:///databasename`

### 使用类路径初始化脚本

Testcontainers 可以在数据库容器启动后、但在你的代码获得连接之前运行初始化脚本。该脚本必须位于类路径中，并按如下方式引用：

`jdbc:tc:mysql:8.0.36:///databasename?TC_INITSCRIPT=somepath/init_mysql.sql`

如果你有用于设置数据库 schema 等的固定脚本，这会很有用。

### 使用文件中的初始化脚本

如果初始化脚本路径以 `file:` 为前缀，它将从文件中加载（相对于工作目录，通常是项目根目录）。

`jdbc:tc:mysql:8.0.36:///databasename?TC_INITSCRIPT=file:src/main/resources/init_mysql.sql`

### 使用初始化函数

与运行固定的数据库设置脚本不同，调用你定义的 Java 函数可能更有用。此功能旨在允许你触发数据库 schema 迁移工具。为此，请将 `TC_INITFUNCTION` 添加到 URL 中，如下所示，传入类名和方法的完整路径：

`jdbc:tc:mysql:8.0.36:///databasename?TC_INITFUNCTION=org.testcontainers.jdbc.JDBCDriverTest::sampleInitFunction`

初始化函数必须是一个公共静态方法，且仅接受一个 `java.sql.Connection` 作为参数，例如：

```java
public class JDBCDriverTest {
    public static void sampleInitFunction(Connection connection) throws SQLException {
        // e.g. run schema setup or Flyway/liquibase/etc DB migrations here...
    }
    ...
```

### 以守护进程模式运行容器

默认情况下，数据库容器会在最后一个连接关闭后立即停止。在某些情况下，你可能需要启动容器并保持运行，直到显式停止它或 JVM 关闭。为此，请将 `TC_DAEMON` 参数添加到 URL 中，如下所示：

`jdbc:tc:mysql:8.0.36:///databasename?TC_DAEMON=true`

使用此参数，即使没有打开的连接，数据库容器也会继续运行。

### 使用 tmpfs 选项运行容器

容器可以使用 `tmpfs` 挂载将数据存储在主机内存中。如果你想加快数据库测试速度，这会很有用。请注意，当容器停止时，数据将会丢失。

要将此选项传递给容器，请将 `TC_TMPFS` 参数添加到 URL 中，如下所示：

`jdbc:tc:postgresql:9.6.8:///databasename?TC_TMPFS=/testtmpfs:rw`

如果你需要多个选项，请用逗号分隔（例如 `TC_TMPFS=key:value,key1:value1&other_parameters=foo`）。

有关 `tmpfs` 挂载的更多信息，请参阅 [Docker 官方文档](https://docs.docker.com/storage/tmpfs/)。

## 数据库容器对象

如果你无法使用 URL 支持，或者需要对容器进行微调，可以自行实例化它。

在测试类中添加 @Rule 或 @ClassRule，例如：

```java
public class SimpleMySQLTest {
    @Rule
    public MySQLContainer mysql = new MySQLContainer();
```

现在，在你的测试代码（或合适的 setup 方法）中，你可以获取连接到此数据库所需的详细信息：

- `mysql.getJdbcUrl()` 提供代码可连接的 JDBC URL
- `mysql.getUsername()` 提供代码应传递给驱动的用户名
- `mysql.getPassword()` 提供代码应传递给驱动的密码

请注意，如果你使用 `@Rule`，每个测试方法都会获得一个独立的容器。如果你使用 `@ClassRule`，测试类中的所有方法将共享一个独立的容器。

示例/测试：

- [MySQL](https://github.com/testcontainers/testcontainers-java/blob/main/modules/mysql/src/test/java/org/testcontainers/junit/mysql/SimpleMySQLTest.java)
- [PostgreSQL](https://github.com/testcontainers/testcontainers-java/blob/main/modules/postgresql/src/test/java/org/testcontainers/junit/postgresql/SimplePostgreSQLTest.java)
