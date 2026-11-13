---
source_url: https://java.testcontainers.org/modules/databases/oceanbase/
source_hash: sha256:6812f876f0a30055f02def6b44838556bb6fc75701226793688fd84dea13af69
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# OceanBase 模块

用于 [OceanBase](https://hub.docker.com/r/oceanbase/oceanbase-ce) 的 Testcontainers 模块

## 使用示例

你可以在任何 Java 应用中通过以下方式启动 OceanBase 容器实例：

**容器定义**

```java
OceanBaseCEContainer oceanbase = new OceanBaseCEContainer(
    "oceanbase/oceanbase-ce:4.2.1.8-108000022024072217"
)
```

有关所有关系型数据库容器类型通用的文档和用法，请参阅[数据库容器](../index.md)。

### Testcontainers JDBC URL

`jdbc:tc:oceanbasece:4.2.1-lts:///databasename`

相关文档请参阅 [JDBC](../jdbc/index.md)。

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-oceanbase:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-oceanbase</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **Hint**
>
> 添加这个 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你应确保项目中还包含合适的数据库驱动作为依赖。
