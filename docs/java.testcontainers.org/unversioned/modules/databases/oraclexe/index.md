---
source_url: https://java.testcontainers.org/modules/databases/oraclexe/
source_hash: sha256:9f708cd4148a32695f8ea3eede2f3b36c45c7edab1f5a2a45bedde8639f22e4e
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Oracle XE 模块

用于 [Oracle XE](https://hub.docker.com/r/gvenzl/oracle-xe) 的 Testcontainers 模块

## 使用示例

你可以在任何 Java 应用中通过以下方式启动 Oracle-XE 容器实例：

**创建容器**

```java
OracleContainer oracle = new OracleContainer("gvenzl/oracle-xe:21-slim-faststart")
```

有关所有关系型数据库容器类型通用的文档和用法，请参阅[数据库容器](../index.md)。

### Testcontainers JDBC URL

`jdbc:tc:oracle:21-slim-faststart:///databasename`

相关文档请参阅 [JDBC](../jdbc/index.md)。

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-oracle-xe:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-oracle-xe</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **Hint**
>
> 添加这个 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你应确保项目中还包含合适的数据库驱动作为依赖。
