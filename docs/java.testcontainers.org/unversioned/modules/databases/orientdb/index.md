---
source_url: https://java.testcontainers.org/modules/databases/orientdb/
source_hash: sha256:cdf58a676318c8a1fe0f37f8691466535a50ca5fa610bda8faf2c4a4f07548bf
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# OrientDB 模块

用于 [OrientDB](https://hub.docker.com/_/orientdb/) 的 Testcontainers 模块

## 使用示例

你可以在任何 Java 应用中通过以下方式启动 OrientDB 容器实例：

**创建容器**

```java
OrientDBContainer orientdb = new OrientDBContainer("orientdb:3.2.0-tp3")
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-orientdb:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-orientdb</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **Hint**
>
> 如果你计划访问该 Testcontainer，请添加 OrientDB Java 客户端：
>
> **Gradle**
>
> **Maven**

```groovy
compile "com.orientechnologies:orientdb-client:3.0.24"
```

```xml
<dependency>
    <groupId>com.orientechnologies</groupId>
    <artifactId>orientdb-client</artifactId>
    <version>3.0.24</version>
</dependency>
```
