---
source_url: https://java.testcontainers.org/modules/databases/cassandra/
source_hash: sha256:a73b4305b7317599fb65f5a0b8f20a9493557822067d966652f0fb6e8794efbd
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Cassandra

## 使用示例

本示例连接到 Cassandra 集群：

1. 定义一个容器：

   **容器定义**

   ```java
   CassandraContainer cassandraContainer = new CassandraContainer(CASSANDRA_IMAGE)
   ```
2. 构建一个 `CqlSession`：

   **构建 CqlSession**

   ```java
   final CqlSession cqlSession = CqlSession
       .builder()
       .addContactPoint(cassandraContainer.getContactPoint())
       .withLocalDatacenter(cassandraContainer.getLocalDatacenter())
       .build();
   ```
3. 定义一个容器，其自定义的 `cassandra.yaml` 位于 `cassandra-auth-required-configuration` 目录中：

   **运行需要认证的初始化脚本**

   ```java
   CassandraContainer cassandraContainer = new CassandraContainer(CASSANDRA_IMAGE)
       .withConfigurationOverride("cassandra-auth-required-configuration")
       .withInitScript("initial.cql")
   ```

## 使用安全连接（TLS）

如果你用一个将属性 `client_encryption_options.optional` 设置为 `false` 的版本覆盖默认的 `cassandra.yaml`，那么在初始化容器时必须提供有效的客户端证书和密钥（PEM 格式）：

**SSL 配置**

```java
CassandraContainer cassandraContainer = new CassandraContainer(CASSANDRA_IMAGE)
    .withConfigurationOverride("cassandra-ssl-configuration")
    .withSsl("client-ssl/cassandra.cer.pem", "client-ssl/cassandra.key.pem")
```

> **提示**
>
> 如需生成客户端证书和密钥，请参阅[该文档](https://docs.datastax.com/en/cassandra-oss/3.x/cassandra/configuration/secureSSLCertificates.html)。

## 将本模块添加到项目依赖中

在你的 `pom.xml`/`build.gradle` 文件中添加以下依赖：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-cassandra:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-cassandra</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
