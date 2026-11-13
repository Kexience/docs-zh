---
source_url: https://java.testcontainers.org/modules/elasticsearch/
source_hash: sha256:e68a1febd4c3a1b76eaf1b22a415ace060e3d6d9876e44b699b649b1589e2bda
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Elasticsearch

该模块帮助使用 Testcontainers 运行 [elasticsearch](https://www.elastic.co/products/elasticsearch)。

请注意，它基于 elastic 提供的[官方 Docker 镜像](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html)。

## 使用示例

在以下示例中，我们将使用以下版本：

**Version 9（推荐）**

```java
static final String ELASTICSEARCH_VERSION_9 = "9.5.2";

static final DockerImageName ELASTICSEARCH_IMAGE_9 = DockerImageName
    .parse("docker.elastic.co/elasticsearch/elasticsearch")
    .withTag(ELASTICSEARCH_VERSION_9);
```

**Version 8（维护中）**

```java
static final String ELASTICSEARCH_VERSION_8 = "8.19.20";

static final DockerImageName ELASTICSEARCH_IMAGE_8 = DockerImageName
    .parse("docker.elastic.co/elasticsearch/elasticsearch")
    .withTag(ELASTICSEARCH_VERSION_8);
```

**Version 7（已弃用）**

```java
static final String ELASTICSEARCH_VERSION_7 = "7.17.29";

static final DockerImageName ELASTICSEARCH_IMAGE_7 = DockerImageName
    .parse("docker.elastic.co/elasticsearch/elasticsearch")
    .withTag(ELASTICSEARCH_VERSION_7);
```

从 Elasticsearch 8 开始，默认启用安全和 HTTPS。你可以按如下方式启动容器并使用 REST 客户端与其通信：

**HttpClient**

```java
// Create the elasticsearch container.
try (ElasticsearchContainer container = new ElasticsearchContainer(ELASTICSEARCH_IMAGE_LATEST)) {
    // Start the container. This step might take some time...
    container.start();

    // Do whatever you want with the rest client ...
    final CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
    credentialsProvider.setCredentials(
        AuthScope.ANY,
        new UsernamePasswordCredentials(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
    );

    client =
        RestClient
            .builder(HttpHost.create("https://" + container.getHttpHostAddress()))
            .setHttpClientConfigCallback(httpClientBuilder -> {
                httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
                // SSL is activated by default in Elasticsearch 8+
                httpClientBuilder.setSSLContext(container.createSslContextFromCa());
                return httpClientBuilder;
            })
            .build();

    Response response = client.performRequest(new Request("GET", "/_cluster/health"));

    ⋯

}
```

### 禁用 TLS

如果你不需要 HTTPS，可以将其关闭：

**禁用 TLS 的 HttpClient**

```java
// Create the elasticsearch container.
try (
    ElasticsearchContainer container = new ElasticsearchContainer(ELASTICSEARCH_IMAGE_LATEST)
        // disable SSL
        .withEnv("xpack.security.transport.ssl.enabled", "false")
        .withEnv("xpack.security.http.ssl.enabled", "false")
) {
    // Start the container. This step might take some time...
    container.start();

    // Do whatever you want with the rest client ...
    final CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
    credentialsProvider.setCredentials(
        AuthScope.ANY,
        new UsernamePasswordCredentials(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
    );

    client =
        RestClient
            .builder(HttpHost.create(container.getHttpHostAddress()))
            .setHttpClientConfigCallback(httpClientBuilder -> {
                return httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
            })
            .build();

    Response response = client.performRequest(new Request("GET", "/_cluster/health"));

    ⋯

}
```

### Elasticsearch 7（已弃用）

Elasticsearch 7 监听 HTTP，并且除非你通过 `withPassword()` 主动启用，否则不会开启安全功能。

**HttpClient**

```java
// Create the elasticsearch container.
try (ElasticsearchContainer container = new ElasticsearchContainer(ELASTICSEARCH_IMAGE_7)) {
    // Start the container. This step might take some time...
    container.start();

    client = RestClient.builder(HttpHost.create(container.getHttpHostAddress())).build();

    Response response = client.performRequest(new Request("GET", "/_cluster/health"));

    ⋯

}

⋯

// Create the elasticsearch container.
try (
    ElasticsearchContainer container = new ElasticsearchContainer(ELASTICSEARCH_IMAGE_7)
        // With a password
        .withPassword(ELASTICSEARCH_PASSWORD)
) {
    // Start the container. This step might take some time...
    container.start();

    // Create the secured client.
    final CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
    credentialsProvider.setCredentials(
        AuthScope.ANY,
        new UsernamePasswordCredentials(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
    );

    client =
        RestClient
            .builder(HttpHost.create(container.getHttpHostAddress()))
            .setHttpClientConfigCallback(httpClientBuilder -> {
                return httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
            })
            .build();

    Response response = client.performRequest(new Request("GET", "/_cluster/health"));

    ⋯

}
```

**启用安全的 HttpClient**

```java
// Create the elasticsearch container.
try (
    ElasticsearchContainer container = new ElasticsearchContainer(ELASTICSEARCH_IMAGE_7)
        // With a password
        .withPassword(ELASTICSEARCH_PASSWORD)
) {
    // Start the container. This step might take some time...
    container.start();

    // Create the secured client.
    final CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
    credentialsProvider.setCredentials(
        AuthScope.ANY,
        new UsernamePasswordCredentials(ELASTICSEARCH_USERNAME, ELASTICSEARCH_PASSWORD)
    );

    client =
        RestClient
            .builder(HttpHost.create(container.getHttpHostAddress()))
            .setHttpClientConfigCallback(httpClientBuilder -> {
                return httpClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
            })
            .build();

    Response response = client.performRequest(new Request("GET", "/_cluster/health"));

    ⋯

}
```

[TransportClient](https://www.elastic.co/guide/en/elasticsearch/client/java-api/current/transport-client.html) 已在 Elasticsearch 8 中移除。但它仍可用于 7.x 容器。默认集群名称为 `docker-cluster`，因此你需要更改 `cluster.name` 设置，或将 `client.transport.ignore_cluster_name` 设置为 `true`。

**TransportClient**

```java
// Create the elasticsearch container.
try (ElasticsearchContainer container = new ElasticsearchContainer(ELASTICSEARCH_IMAGE_7)) {
    // Start the container. This step might take some time...
    container.start();

    // Do whatever you want with the transport client
    TransportAddress transportAddress = new TransportAddress(container.getTcpHost());
    String expectedClusterName = "docker-cluster";
    Settings settings = Settings.builder().put("cluster.name", expectedClusterName).build();
    try (
        TransportClient transportClient = new PreBuiltTransportClient(settings)
            .addTransportAddress(transportAddress)
    ) {
        ClusterHealthResponse healths = transportClient.admin().cluster().prepareHealth().get();
        String clusterName = healths.getClusterName();

        ⋯

    }
}
```

### OSS 发行版

最后一个 OSS 镜像是 `elasticsearch-oss:7.10.2`。它不包含 Elastic License 下的功能，并且 `withPassword()` 会被拒绝：

**OSS 镜像**

```java
ElasticsearchContainer container = new ElasticsearchContainer(
    "docker.elastic.co/elasticsearch/elasticsearch-oss:7.10.2"
)
```

## Kibana 容器

该模块还提供了用于与 [Kibana](https://www.elastic.co/kibana) 进行测试的 `KibanaContainer`。Kibana 需要连接到 Elasticsearch，`KibanaContainer` 支持两种模式：托管模式和外部模式。

### 托管模式

在托管模式下，`KibanaContainer` 会自动连接到 `ElasticsearchContainer`：

**Kibana 与 Elasticsearch**

```java
// managedModeReachesElasticsearchOnSharedNetwork {
try (
    Network network = Network.newNetwork();
    ElasticsearchContainer es = new ElasticsearchContainer(ELASTICSEARCH_IMAGE_LATEST).withNetwork(network);
    KibanaContainer kibana = new KibanaContainer(es).withNetwork(network)
) {
    es.start();
    kibana.start();

    assertKibanaIsAvailable(kibana);
}
// }
```

当在托管模式下使用显式网络时，两个容器必须共享同一个 `Network` 实例。或者，你也可以完全省略网络配置，`KibanaContainer` 会尽力自动创建一个共享的临时网络。

### 外部模式

在外部模式下，`KibanaContainer` 通过 URL 并使用提供的凭据连接到外部 Elasticsearch 实例：

**Kibana 与外部 Elasticsearch**

```java
final String esHostname = "elasticsearch";

// externalModeReachesElasticsearchWithUsernamePassword {
try (
    Network network = Network.newNetwork();
    ElasticsearchContainer es = new ElasticsearchContainer(ELASTICSEARCH_IMAGE_LATEST)
        .withNetwork(network)
        .withNetworkAliases(esHostname)
        .withEnv("xpack.security.http.ssl.enabled", "false")
) {
    es.start();
    String kibanaSystemPassword = setKibanaSystemPassword(es);

    try (
        KibanaContainer kibana = new KibanaContainer(KIBANA_IMAGE)
            .withNetwork(network)
            .withElasticsearchUrl("http://" + esHostname + ":9200")
            .withKibanaSystemPassword(kibanaSystemPassword)
    ) {
        kibana.start();
        assertKibanaIsAvailable(kibana);
    }
}
// }
```

对于使用 HTTPS 的外部模式，请使用 `withElasticsearchCaCertificate()` 提供 CA 证书。你可以使用用户名/密码（`withElasticsearchCredentials()`）或服务账户令牌（`withElasticsearchServiceAccountToken()`）进行身份验证。

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-elasticsearch:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-elasticsearch</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
