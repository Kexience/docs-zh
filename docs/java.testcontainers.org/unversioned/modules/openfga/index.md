---
source_url: https://java.testcontainers.org/modules/openfga/
source_hash: sha256:a949ee51f6953b942408fe2601d3ce02a4fb5b1cb23c25d86011c957af0fc042
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# OpenFGA

用于 [OpenFGA](https://hub.docker.com/r/openfga/openfga) 的 Testcontainers 模块。

## OpenFGAContainer 使用示例

你可以在任何 Java 应用程序中通过以下方式启动 OpenFGA 容器实例：

**OpenFGA 容器**

```java
OpenFGAContainer openfga = new OpenFGAContainer("openfga/openfga:v1.4.3")
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-openfga:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-openfga</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
