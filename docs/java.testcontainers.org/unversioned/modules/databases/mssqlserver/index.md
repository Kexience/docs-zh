---
source_url: https://java.testcontainers.org/modules/databases/mssqlserver/
source_hash: sha256:1d06145d684fe7cba40c0395e22a948879029222167842b444f60ac8f5cbc942
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# MS SQL Server 模块

面向 [MS SQL Server](https://mcr.microsoft.com/en-us/artifact/mar/mssql/server/) 的 Testcontainers 模块

## 使用示例

在任意 Java 应用中，可以按以下方式启动一个 MS SQL Server 容器实例：

**容器定义**

```java
MSSQLServerContainer mssqlServer = new MSSQLServerContainer(
    "mcr.microsoft.com/mssql/server:2022-CU20-ubuntu-22.04"
)
    .acceptLicense()
```

> **EULA 接受声明**
>
> 由于许可限制，你必须接受此容器镜像的 EULA。要表示你接受 MS SQL Server 镜像的 EULA，请调用 `acceptLicense()` 方法，或者在 classpath 根目录放置一个名为 `container-license-acceptance.txt` 的文件，例如放在 `src/test/resources/container-license-acceptance.txt`。该文件应包含一行：`mcr.microsoft.com/mssql/server:2017-CU12`（如果你覆盖了 docker 镜像名称/标签，请相应修改）。
>
> 请查看 [`microsoft-mssql-server` 镜像文档](https://hub.docker.com/_/microsoft-mssql-server#environment-variables)，其中提供了 EULA 文件的链接。

所有关系型数据库容器类型通用的文档与用法，请参见[数据库容器](../index.md)。

### Testcontainers JDBC URL

`jdbc:tc:sqlserver:2017-CU12:///databasename`

有关文档，请参见 [JDBC](../jdbc/index.md)。

## 将本模块添加到项目依赖中

在你的 `pom.xml`/`build.gradle` 文件中添加以下依赖：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-mssqlserver:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-mssqlserver</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

> **提示**
>
> 添加此 Testcontainers 库 JAR 并不会自动为你的项目添加数据库驱动 JAR。你需要确保项目中还包含合适的数据库驱动作为依赖。

## 许可证

参见 [LICENSE](https://raw.githubusercontent.com/testcontainers/testcontainers-java/main/modules/mssqlserver/LICENSE)。

## 版权

版权所有 (c) 2017 - 2019 G DATA Software AG 及其他作者。

贡献者名单请参见 [AUTHORS](https://raw.githubusercontent.com/testcontainers/testcontainers-java/main/modules/mssqlserver/AUTHORS)。
