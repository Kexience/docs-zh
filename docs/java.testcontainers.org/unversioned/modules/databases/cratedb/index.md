---
source_url: https://java.testcontainers.org/modules/databases/cratedb/
source_hash: sha256:dd2298b677cdad3a32c82bb13856c3a7b13dc343e1bfc14437ecf702432ceab9
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# CrateDB

用于 [CrateDB](https://hub.docker.com/_/crate) 的 Testcontainers 模块

## 使用示例

你可以在任意 Java 应用中通过以下方式启动一个 CrateDB 容器实例：

**容器定义**

```java
CrateDBContainer cratedb = new CrateDBContainer("crate:5.2.5")
```

有关所有关系型数据库容器类型通用的文档和用法，请参阅 [数据库容器](../index.md)。

### Testcontainers JDBC URL

`jdbc:tc:cratedb:5.2.3:///databasename`

有关文档请参阅 [JDBC](../jdbc/index.md)。

## 将本模块添加到项目依赖中

在你的 `pom.xml`/`build.gradle` 文件中添加以下依赖：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-cratedb:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-cratedb</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **提示**
>
> 添加此 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你需要确保项目中还包含合适的数据库驱动作为依赖。
