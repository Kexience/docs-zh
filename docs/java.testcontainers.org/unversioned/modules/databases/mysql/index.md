---
source_url: https://java.testcontainers.org/modules/databases/mysql/
source_hash: sha256:6ed875165f2eacc524bc0353a0cd0c0b74123fc2539c37524029f5253c48ffb0
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# MySQL 模块

用于 [MySQL](https://hub.docker.com/_/mysql) 的 Testcontainers 模块

## 使用示例

你可以在任何 Java 应用中通过以下方式启动 MySQL 容器实例：

**容器定义**

```java
MySQLContainer mysql = new MySQLContainer("mysql:8.0.36")
```

有关所有关系型数据库容器类型通用的文档和用法，请参阅[数据库容器](../index.md)。

### Testcontainers JDBC URL

`jdbc:tc:mysql:8.0.36:///databasename`

相关文档请参阅 [JDBC](../jdbc/index.md)。

## 覆盖 MySQL my.cnf 设置

对于 MySQL 数据库，可以使用 classpath 上的资源来覆盖配置设置。假设 `somepath/mysql_conf_override` 是 classpath 上包含 `.cnf` 文件的目录，则可以使用以下 URL：

`jdbc:tc:mysql:8.0.36://hostname/databasename?TC_MY_CNF=somepath/mysql_conf_override`

该 classpath 目录中的任何 `.cnf` 文件都会被映射到数据库容器的 `/etc/mysql/conf.d` 目录中，并能够在容器启动时覆盖服务器设置。

## MySQL `root` 用户密码

如果未指定自定义密码，容器也会为 `root` 用户使用默认用户密码 `test`。当你为数据库用户指定自定义密码时，该密码也会自动作为 MySQL `root` 用户的密码。

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-mysql:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-mysql</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **Hint**
>
> 添加这个 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你应确保项目中还包含合适的数据库驱动作为依赖。
