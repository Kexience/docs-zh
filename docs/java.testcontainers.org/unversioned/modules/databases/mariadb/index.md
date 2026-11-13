---
source_url: https://java.testcontainers.org/modules/databases/mariadb/
source_hash: sha256:acb85264fc475879448b4c7f370421091de14eef1ffd6245123ac0a52ed004e5
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# [MariaDB](https://hub.docker.com/_/mariadb) 的 Testcontainers 模块

## 使用示例

你可以使用以下方式从任何 Java 应用程序启动一个 MariaDB 容器实例：

**容器定义**

```java
MariaDBContainer mariadb = new MariaDBContainer("mariadb:10.3.39")
```

有关所有关系型数据库容器类型通用的文档和用法，请参阅[数据库容器](../index.md)。

### Testcontainers JDBC URL

`jdbc:tc:mariadb:10.3.39:///databasename`

相关文档请参阅 [JDBC](../jdbc/index.md)。

## MariaDB `root` 用户密码

如果未指定自定义密码，容器也会为 `root` 用户使用默认用户密码 `test`。当你为数据库用户指定自定义密码时，该密码也会自动作为 MariaDB `root` 用户的密码。

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-mariadb:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-mariadb</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **提示**
>
> 添加此 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你应确保项目中也包含合适的数据库驱动作为依赖。
