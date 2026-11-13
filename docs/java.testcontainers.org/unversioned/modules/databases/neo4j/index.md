---
source_url: https://java.testcontainers.org/modules/databases/neo4j/
source_hash: sha256:5ab192434472e2b1532fca3c280db80932abc0b7aa997296be523da899389519
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Neo4j 模块

该模块帮助使用 Testcontainers 运行 [Neo4j](https://neo4j.com/download/)。

请注意，它基于 Neo4j, Inc. 提供的[官方 Docker 镜像](https://hub.docker.com/_/neo4j/)。

尽管本文档示例中使用的是 Neo4j 4.4 的最新 LTS 版本，但 Testcontainers 集成也支持 Neo4j 的较新 5.x 镜像。

## 使用示例

你可以在任何 Java 应用中通过以下方式启动 Neo4j 容器实例：

**Neo4j 容器**

```java
Neo4jContainer neo4j = new Neo4jContainer("neo4j:4.4")
```

## 其他功能

### 自定义密码

可以提供自定义密码：

**自定义密码**

```java
Neo4jContainer neo4j = new Neo4jContainer("neo4j:4.4").withAdminPassword("verySecret");
```

### 禁用认证

可以禁用认证：

**禁用认证**

```java
Neo4jContainer neo4j = new Neo4jContainer("neo4j:4.4")
    .withoutAuthentication()
```

### 随机密码

可以设置一个随机（基于 `UUID`）密码：

**随机密码**

```java
Neo4jContainer neo4j = new Neo4jContainer("neo4j:4.4").withRandomPassword();
```

### Neo4j 配置

Neo4j 的 Docker 镜像需要以专用格式提供 Neo4j 配置选项。容器会处理这一点，你可以像下面这样使用标准选项来配置数据库：

**Neo4j 配置**

```java
Neo4jContainer neo4j = new Neo4jContainer("neo4j:4.4")
    .withNeo4jConfig("dbms.security.procedures.unrestricted", "apoc.*,algo.*")
    .withNeo4jConfig("dbms.tx_log.rotation.size", "42M");
```

### 添加自定义插件

可以像下面这样，将自定义插件（例如 APOC）从任何 classpath 或主机资源复制到容器中：

**插件 jar**

```java
Neo4jContainer neo4j = new Neo4jContainer("neo4j:4.4")
    .withPlugins(MountableFile.forClasspathResource("/custom-plugins/hello-world.jar"))
```

整个目录同样也可以：

**插件文件夹**

```java
Neo4jContainer neo4j = new Neo4jContainer("neo4j:4.4")
    .withPlugins(MountableFile.forClasspathResource("/custom-plugins"))
```

### 添加 Neo4j Docker Labs 插件

可以添加 [Neo4j 4.4 Docker Labs 插件列表](https://neo4j.com/docs/operations-manual/4.4/docker/operations/#docker-neo4jlabs-plugins) 或 [Neo4j 5 插件列表](https://neo4j.com/docs/operations-manual/5/configuration/plugins/)中的任意 Neo4j Labs 插件。

> **Note**
>
> 方法 `withLabsPlugins(Neo4jLabsPlugin...)` 和 `withLabsPlugins(String... plugins)` 已弃用。请使用方法 `withPlugins(String... plugins)`。

**配置 Neo4j Labs 插件**

```java
Neo4jContainer neo4j = new Neo4jContainer("neo4j:4.4") //
    .withPlugins("apoc", "bloom");
```

### 使用预定义数据库启动容器

如果你有希望使用的现有数据库（`graph.db`），可以像下面这样将其复制到容器中：

**复制数据库**

```java
Neo4jContainer neo4j = new Neo4jContainer("neo4j:3.5.30")
    .withDatabase(MountableFile.forClasspathResource("/test-graph.db"))
```

> **Note**
>
> `withDatabase` 方法仅适用于 Neo4j 3.5，与较新版本一起使用时会抛出异常。

## 选择你的 Neo4j 许可证

如果你需要 Neo4j 企业版许可证，可以像下面这样声明 Neo4j 容器：

**企业版**

```java
Neo4jContainer neo4j = new Neo4jContainer("neo4j:4.4-enterprise")
    .acceptLicense()
```

这会基于使用 Neo4j 4.4 企业版构建的 Docker 镜像创建一个 Testcontainers 容器。对 `withEnterpriseEdition` 的调用会添加所需的环境变量，表示你已接受企业版的条款和条件。你需要在 classpath 根目录下添加一个名为 `container-license-acceptance.txt` 的文件，并在其中写入一行文本 `neo4j:4.4-enterprise` 来表示接受。

如果你计划运行较新的 Neo4j 5.x 企业版镜像，则必须手动指定正确的企业版镜像（例如 `neo4j:5-enterprise`），并通过在容器定义中添加 `.withEnv("NEO4J_ACCEPT_LICENSE_AGREEMENT", "yes")` 来设置环境变量 `NEO4J_ACCEPT_LICENSE_AGREEMENT`。

你可以在这里找到有关 Neo4j 许可的更多信息：[About Neo4j Licenses](https://neo4j.com/licensing/)。

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-neo4j:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-neo4j</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **Hint**
>
> 如果你计划通过 Bolt 访问 Testcontainers，请添加 Neo4j Java 驱动：
>
> **Gradle**
>
> **Maven**

```groovy
compile "org.neo4j.driver:neo4j-java-driver:4.4.13"
```

```xml
<dependency>
    <groupId>org.neo4j.driver</groupId>
    <artifactId>neo4j-java-driver</artifactId>
    <version>4.4.13</version>
</dependency>
```
