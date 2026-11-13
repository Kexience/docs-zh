---
source_url: https://java.testcontainers.org/modules/databases/databend/
source_hash: sha256:2a05c33a452da7cbe76dd77327740237c957a3f7540ef4e16ceb65ec72a6a268
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# [Databend](https://hub.docker.com/r/datafuselabs/databend) 的 Testcontainers 模块

## 使用示例

你可以使用以下方式从任何 Java 应用程序启动一个 Databend 容器实例：

**容器定义**

```java
DatabendContainer databend = new DatabendContainer("datafuselabs/databend:v1.2.615")
```

### Testcontainers JDBC URL

`jdbc:tc:databend:v1.2.615:///databasename`

相关文档请参阅 [JDBC](../jdbc/index.md)。

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-databend:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-databend</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **提示**
>
> 添加此 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你应确保项目中也包含合适的数据库驱动作为依赖。
