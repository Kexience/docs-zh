---
source_url: https://java.testcontainers.org/modules/databases/influxdb/
source_hash: sha256:0749131e7f0aedde4561cb55d38bbf07c1254fee0a2cd752f9d77ea9fa33d6a9
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# InfluxData [InfluxDB](https://www.influxdata.com/products/influxdb/) 的 Testcontainers 模块

## 重要说明

InfluxDB 2.x 中存在不兼容变更。更多信息请参阅[主文档](https://docs.influxdata.com/influxdb/v2.0/upgrade/v1-to-v2/)。你可以在 [Docker Hub](https://hub.docker.com/_/influxdb) 上找到有关官方 InfluxDB 镜像的更多信息。

## InfluxDB 2.x 使用示例

在测试中将 `InfluxDBContainer` 作为 InfluxDB 的替代运行：

**创建 InfluxDB 容器**

```java
final InfluxDBContainer<?> influxDBContainer = new InfluxDBContainer<>(
    DockerImageName.parse("influxdb:2.0.7")
)
```

InfluxDB 实例将使用以下数据进行设置：

| 属性 | 默认值 |
| --- | --- |
| username | test-user |
| password | test-password |
| organization | test-org |
| bucket | test-bucket |
| retention | 0（无限） |
| adminToken | - |

有关 InfluxDB 设置的更多详细信息，请访问官方 [InfluxDB 文档](https://docs.influxdata.com/influxdb/v2.0/upgrade/v1-to-v2/docker/#influxdb-2x-initialization-credentials)。

可以覆盖默认属性值。创建带有 InfluxDB 管理员令牌的容器：

**创建带有管理员令牌的 InfluxDB 容器**

```java
final InfluxDBContainer<?> influxDBContainer = new InfluxDBContainer<>(
    DockerImageName.parse("influxdb:2.0.7")
)
    .withAdminToken(ADMIN_TOKEN)
```

或者创建一个具有自定义用户名、密码、bucket、组织和保留时间的容器：

**创建具有自定义设置的 InfluxDB 容器**

```java
final InfluxDBContainer<?> influxDBContainer = new InfluxDBContainer<>(
    DockerImageName.parse("influxdb:2.0.7")
)
    .withUsername(USERNAME)
    .withPassword(PASSWORD)
    .withOrganization(ORG)
    .withBucket(BUCKET)
    .withRetention(RETENTION);
```

以下代码片段展示了如何创建 InfluxDB Java 客户端：

**创建 InfluxDB Java 客户端**

```java
public static InfluxDBClient createClient(final InfluxDBContainer<?> influxDBContainer) {
    final InfluxDBClientOptions influxDBClientOptions = InfluxDBClientOptions
        .builder()
        .url(influxDBContainer.getUrl())
        .authenticate(influxDBContainer.getUsername(), influxDBContainer.getPassword().toCharArray())
        .bucket(influxDBContainer.getBucket())
        .org(influxDBContainer.getOrganization())
        .build();
    return InfluxDBClientFactory.create(influxDBClientOptions);
}
```

> **提示**
>
> 你可以在[此处](https://github.com/influxdata/influxdb-client-java)找到有关 InfluxDB 2.x Java 客户端的最新文档。

## InfluxDB 1.x 使用示例

在测试中将 `InfluxDBContainer` 作为 InfluxDB 的替代运行，并使用默认环境变量：

**创建 InfluxDB 容器**

```java
final InfluxDBContainer<?> influxDBContainer = new InfluxDBContainer<>(
    DockerImageName.parse("influxdb:1.4.3")
)
```

InfluxDB 实例将使用以下数据进行设置：

| 属性 | 默认值 |
| --- | --- |
| username | test-user |
| password | test-password |
| authEnabled | true |
| admin | admin |
| adminPassword | password |
| database | - |

可以覆盖默认值。例如，创建一个具有自定义用户名、密码和数据库名称的 InfluxDB 容器：

**创建具有自定义设置的 InfluxDB 容器**

```java
final InfluxDBContainer<?> influxDBContainer = new InfluxDBContainer<>(
    DockerImageName.parse("influxdb:1.4.3")
)
    .withDatabase(DATABASE)
    .withUsername(USER)
    .withPassword(PASSWORD)
```

在以下示例中，你将找到使用官方 Java 客户端创建 InfluxDB 客户端的代码片段：

**创建 InfluxDB Java 客户端**

```java
public static InfluxDB createInfluxDBWithUrl(final InfluxDBContainer<?> container) {
    InfluxDB influxDB = InfluxDBFactory.connect(
        container.getUrl(),
        container.getUsername(),
        container.getPassword()
    );
    influxDB.setDatabase(container.getDatabase());
    return influxDB;
}
```

> **提示**
>
> 你可以在[此处](https://github.com/influxdata/influxdb-java)找到有关 InfluxDB 1.x Java 客户端的最新文档。

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-influxdb:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-influxdb</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **提示**
>
> 添加此 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你应确保项目中也包含合适的数据库驱动作为依赖。
