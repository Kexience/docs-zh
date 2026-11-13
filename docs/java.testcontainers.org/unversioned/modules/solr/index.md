---
source_url: https://java.testcontainers.org/modules/solr/
source_hash: sha256:93feadc42c72c0c8904e6339e36c6b2aaaee7aed94019d87dcd4861690ba40f9
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Solr 模块

此模块帮助使用 Testcontainers 运行 [Solr](https://solr.apache.org/)。

请注意，它基于[官方 Docker 镜像](https://hub.docker.com/_/solr/)。

## 使用示例

你可以在任何 Java 应用程序中使用以下方式启动 Solr 容器实例：

**使用 Solr 容器**

```java
// Create the solr container.
SolrContainer container = new SolrContainer(solrImage);

// Start the container. This step might take some time...
container.start();

// Do whatever you want with the client ...
SolrClient client = new Http2SolrClient.Builder(
    "http://" + container.getHost() + ":" + container.getSolrPort() + "/solr"
)
    .build();
SolrPingResponse response = client.ping("dummy");

// Stop the container.
container.stop();
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-solr:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-solr</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
