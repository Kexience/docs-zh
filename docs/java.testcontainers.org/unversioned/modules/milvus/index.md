---
source_url: https://java.testcontainers.org/modules/milvus/
source_hash: sha256:57bde3e0e06768fc2943e3a6bf38922a4228848ddde0519793d1ca33cbba129f
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Milvus

用于 [Milvus](https://hub.docker.com/r/milvusdb/milvus) 的 Testcontainers 模块。

## Milvus 使用示例

你可以在任何 Java 应用程序中通过以下方式启动 Milvus 容器实例：

**默认配置**

```java
MilvusContainer milvus = new MilvusContainer("milvusdb/milvus:v2.3.9")
```

使用外部 Etcd：

**外部 Etcd**

```java
Network network = Network.newNetwork();
GenericContainer<?> etcd = new GenericContainer<>("quay.io/coreos/etcd:v3.5.5")
    .withNetwork(network)
    .withNetworkAliases("etcd")
    .withCommand(
        "etcd",
        "-advertise-client-urls=http://127.0.0.1:2379",
        "-listen-client-urls=http://0.0.0.0:2379",
        "--data-dir=/etcd"
    )
    .withEnv("ETCD_AUTO_COMPACTION_MODE", "revision")
    .withEnv("ETCD_AUTO_COMPACTION_RETENTION", "1000")
    .withEnv("ETCD_QUOTA_BACKEND_BYTES", "4294967296")
    .withEnv("ETCD_SNAPSHOT_COUNT", "50000")
    .waitingFor(Wait.forLogMessage(".*ready to serve client requests.*", 1));
MilvusContainer milvus = new MilvusContainer("milvusdb/milvus:v2.3.9")
    .withNetwork(network)
    .withEtcdEndpoint("etcd:2379")
    .dependsOn(etcd)
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-milvus:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-milvus</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
