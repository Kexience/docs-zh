---
source_url: https://java.testcontainers.org/modules/databases/r2dbc/
source_hash: sha256:c22a040a3caf5552f9b28a3353b75dfe3f1ffb1ab060e03c233ab1af6720a127
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# R2DBC 支持

你可以通过以下两种方式之一获得一个临时数据库：

- **使用经过特殊处理的 R2DBC URL**：只需对你的系统的 R2DBC URL 字符串做非常简单的修改，Testcontainers 就会提供一个一次性的替代数据库，无需修改应用程序代码即可使用。
- **JUnit @Rule/@ClassRule**：该模式会在你的测试开始前在容器内启动一个数据库，并在测试结束后将其销毁。

## 通过 R2DBC URL scheme 启动的数据库容器

只要 classpath 上有 Testcontainers 以及相应的 R2DBC 驱动，你只需修改常规的 R2DBC 连接 URL，即可在应用程序每次启动时获得一个全新的容器化数据库实例。

当 `ConnectionFactory` 关闭时，已启动的容器将被终止。

> **警告**
>
> 
> 数据库模块（例如 `org.testcontainers:testcontainers-mysql`）**和** `org.testcontainers:testcontainers-r2dbc` 都必须位于应用程序运行时的 classpath 上。

**原始 URL**：`r2dbc:mysql://localhost:3306/databasename`

1. 在 `r2dbc:` 之后插入 `tc:`，如下所示。请注意，主机名、端口和数据库名都将被忽略；你可以保持原样，也可以将它们设为任意值。
2. 使用 `TC_IMAGE_TAG` 查询参数指定你想要的数据库官方镜像的必需 Docker 标签。

**请注意，与 Testcontainers 的 JDBC URL 支持不同，无法在 URL 的 'scheme' 部分指定镜像标签，必须始终使用 `TC_IMAGE_TAG` 来指定标签。**

这样 URL 就变为：
 `r2dbc:tc:mysql:///databasename?TC_IMAGE_TAG=8.0.36`

> **注意**
>
> 
> 从现在起我们将使用 `///`（不含主机的 URI），以强调 `host:port` 这一对信息无关紧要。
>  从 Testcontainers 的角度看，`r2dbc:mysql://localhost:3306/databasename` 与 `r2dbc:mysql:///databasename` 是同一个 URI。

> **警告**
>
> 
> 如果你使用 R2DBC URL 支持，就无需实例化容器实例 —— Testcontainers 会自动完成。

### R2DBC URL 示例

#### 使用 ClickHouse

`r2dbc:tc:clickhouse:///databasename?TC_IMAGE_TAG=21.11.11-alpine`

#### 使用 MySQL

`r2dbc:tc:mysql:///databasename?TC_IMAGE_TAG=8.0.36`

#### 使用 MariaDB

`r2dbc:tc:mariadb:///databasename?TC_IMAGE_TAG=10.3.39`

#### 使用 PostgreSQL

`r2dbc:tc:postgresql:///databasename?TC_IMAGE_TAG=9.6.8`

#### 使用 MSSQL：

`r2dbc:tc:sqlserver:///?TC_IMAGE_TAG=2017-CU12`

#### 使用 Oracle：

`r2dbc:tc:oracle:///?TC_IMAGE_TAG=21-slim-faststart`

## 从数据库容器对象获取 `ConnectionFactoryOptions`

如果你已经拥有了一个数据库容器实例，可以从中获取一个 `ConnectionFactoryOptions` 实例：

**从实例创建 ConnectionFactoryOptions）**

```java
ConnectionFactoryOptions options = PostgreSQLR2DBCDatabaseContainer.getOptions(
    container
);
```
