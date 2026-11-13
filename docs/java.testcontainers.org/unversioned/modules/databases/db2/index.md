---
source_url: https://java.testcontainers.org/modules/databases/db2/
source_hash: sha256:84a4e02f1b5280b31687abc736dd111810346edd0e19a0243ae61896c7dec713
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# [DB2](https://www.ibm.com/docs/en/db2/11.5.x?topic=deployments-db2-community-edition-docker) 的 Testcontainers 模块

## 使用示例

你可以使用以下方式从任何 Java 应用程序启动一个 DB2 容器实例：

**容器定义**

```java
Db2Container db2 = new Db2Container("icr.io/db2_community/db2:11.5.8.0").acceptLicense()
```

> **EULA 接受**
>
> 由于许可限制，你需要接受此容器镜像的 EULA。要表明你接受 DB2 镜像的 EULA，请调用 `acceptLicense()` 方法，或在类路径根目录下放置一个名为 `container-license-acceptance.txt` 的文件，例如 `src/test/resources/container-license-acceptance.txt`。该文件应包含以下内容：`ibmcom/db2:11.5.0.0a`（如果你覆盖了 Docker 镜像名称/标签，请相应更新）。

有关所有关系型数据库容器类型通用的文档和用法，请参阅[数据库容器](../index.md)。

### Testcontainers JDBC URL

`jdbc:tc:db2:11.5.0.0a:///databasename`

相关文档请参阅 [JDBC](../jdbc/index.md)。

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-db2:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-db2</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **提示**
>
> 添加此 Testcontainers 库 JAR 不会自动为你的项目添加数据库驱动 JAR。你应确保项目中也包含合适的数据库驱动作为依赖。
