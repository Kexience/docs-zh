---
source_url: https://java.testcontainers.org/modules/databases/timeplus/
source_hash: sha256:1b7a27ee730aaa8e3e81aaef6772c032bb3be0a6939ce0dfc5acd3f27138b24f
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Timeplus 模块

用于 [Timeplus](https://hub.docker.com/r/timeplus/timeplusd) 的 Testcontainers 模块

## 使用示例

你可以在任何 Java 应用中通过以下方式启动 Timeplus 容器实例：

**创建容器**

```java
TimeplusContainer timeplus = new TimeplusContainer("timeplus/timeplusd:2.3.21")
```

### Testcontainers JDBC URL

`jdbc:tc:timeplus:2.3.21:///databasename`

相关文档请参阅 [JDBC](../jdbc/index.md)。

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-timeplus:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-timeplus</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **Hint**
>
> 添加这个 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你应确保项目中还包含合适的数据库驱动作为依赖。
