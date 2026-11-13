---
source_url: https://java.testcontainers.org/modules/databases/scylladb/
source_hash: sha256:d7ec613f2e371b3172ab2fbf8cecbdab7d0ce985b118e052ba3d1ad7ba487bb1
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# ScyllaDB

用于 [ScyllaDB](https://hub.docker.com/r/scylladb/scylla) 的 Testcontainers 模块

## ScyllaDB 的使用示例

你可以通过以下方式从任意 Java 应用程序启动一个 ScyllaDB 容器实例：

**创建容器**

```java
ScyllaDBContainer scylladb = new ScyllaDBContainer("scylladb/scylla:6.2")
```

**自定义配置文件**

```java
ScyllaDBContainer scylladb = new ScyllaDBContainer("scylladb/scylla:6.2")
    .withConfigurationOverride("scylla-test-ssl")
    .withSsl(
        MountableFile.forClasspathResource("keys/scylla.cer.pem"),
        MountableFile.forClasspathResource("keys/scylla.key.pem"),
        MountableFile.forClasspathResource("keys/scylla.truststore")
    )
```

### 构建 CqlSession

**使用 CQL 端口**

```java
CqlSession session = CqlSession
    .builder()
    .addContactPoint(scylladb.getContactPoint())
    .withLocalDatacenter("datacenter1")
    .build();
```

**使用 SSL**

```java
String testResourcesDir = getClass().getClassLoader().getResource("keys/").getPath();

KeyStore keyStore = KeyStore.getInstance("PKCS12");
keyStore.load(
    Files.newInputStream(Paths.get(testResourcesDir + "scylla.keystore")),
    "scylla".toCharArray()
);

KeyStore trustStore = KeyStore.getInstance("PKCS12");
trustStore.load(
    Files.newInputStream(Paths.get(testResourcesDir + "scylla.truststore")),
    "scylla".toCharArray()
);

KeyManagerFactory keyManagerFactory = KeyManagerFactory.getInstance(
    KeyManagerFactory.getDefaultAlgorithm()
);
keyManagerFactory.init(keyStore, "scylla".toCharArray());

TrustManagerFactory trustManagerFactory = TrustManagerFactory.getInstance(
    TrustManagerFactory.getDefaultAlgorithm()
);
trustManagerFactory.init(trustStore);

SSLContext sslContext = SSLContext.getInstance("TLS");
sslContext.init(keyManagerFactory.getKeyManagers(), trustManagerFactory.getTrustManagers(), null);
```

**使用分片感知端口**

```java
CqlSession session = CqlSession
    .builder()
    .addContactPoint(scylladb.getShardAwareContactPoint())
    .withLocalDatacenter("datacenter1")
    .build();
```

### Alternator

**启用 Alternator**

```java
ScyllaDBContainer scylladb = new ScyllaDBContainer(SCYLLADB_IMAGE).withAlternator()
```

**带 Alternator 的 DynamoDbClient**

```java
DynamoDbClient client = DynamoDbClient
    .builder()
    .endpointOverride(URI.create(scylladb.getAlternatorEndpoint()))
    .credentialsProvider(StaticCredentialsProvider.create(AwsBasicCredentials.create("test", "test")))
    .region(Region.US_EAST_1)
    .build();
```

## 将本模块添加到项目依赖中

在你的 `pom.xml`/`build.gradle` 文件中添加以下依赖：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-scylladb:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-scylladb</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
