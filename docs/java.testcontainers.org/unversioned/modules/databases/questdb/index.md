---
source_url: https://java.testcontainers.org/modules/databases/questdb/
source_hash: sha256:c639afc9f0d3e431e8dbe74f19a8dc99c66a5cb6d47a36c7e6bbd27c89e38d15
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# QuestDB 模块

用于 [QuestDB](https://hub.docker.com/r/questdb/questdb) 的 Testcontainers 模块

## 使用示例

你可以在任何 Java 应用中通过以下方式启动 QuestDB 容器实例：

**创建容器**

```java
QuestDBContainer questDB = new QuestDBContainer("questdb/questdb:9.2.2")
```

有关所有关系型数据库容器类型通用的文档和用法，请参阅[数据库容器](../index.md)。

### Testcontainers JDBC URL

`jdbc:tc:questdb:6.5.3:///databasename`

相关文档请参阅 [JDBC](../jdbc/index.md)。

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-questdb:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-questdb</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
