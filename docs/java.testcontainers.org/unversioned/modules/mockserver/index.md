---
source_url: https://java.testcontainers.org/modules/mockserver/
source_hash: sha256:b2b97f14a236c6bfe58faf8d9ac26512b5e39e96c71e15bab3b1b2be51cda5cc
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# MockServer

Mock Server 可用于通过将请求与用户定义的期望进行匹配来模拟 HTTP 服务。

## 使用示例

以下示例展示了如何启动 Mockserver。

**创建 MockServer 容器**

```java
MockServerContainer mockServer = new MockServerContainer(MOCKSERVER_IMAGE)
```

以及如何使用 Java MockServerClient 设置一个简单的期望。

**设置一个简单的期望**

```java
package org.testcontainers.mockserver;

import io.restassured.config.RestAssuredConfig;
import io.restassured.config.SSLConfig;
import org.apache.http.conn.ssl.SSLSocketFactory;
import org.junit.jupiter.api.Test;
import org.mockserver.client.MockServerClient;
import org.mockserver.configuration.Configuration;
import org.mockserver.logging.MockServerLogger;
import org.mockserver.socket.tls.KeyStoreFactory;
import org.testcontainers.utility.DockerImageName;

import static io.restassured.RestAssured.given;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockserver.model.HttpRequest.request;
import static org.mockserver.model.HttpResponse.response;

class MockServerContainerTest {

    public static final DockerImageName MOCKSERVER_IMAGE = DockerImageName
        .parse("mockserver/mockserver")
        .withTag("mockserver-" + MockServerClient.class.getPackage().getImplementationVersion());

    @Test
    void shouldCallActualMockserverVersion() {
        try ( // creatingProxy {
            MockServerContainer mockServer = new MockServerContainer(MOCKSERVER_IMAGE)
            // }
        ) {
            mockServer.start();

            String expectedBody = "Hello World!";

            try (MockServerClient client = new MockServerClient(mockServer.getHost(), mockServer.getServerPort())) {
                assertThat(client.hasStarted()).as("Mockserver running").isTrue();

                client.when(request().withPath("/hello")).respond(response().withBody(expectedBody));

                assertThat(given().when().get(mockServer.getEndpoint() + "/hello").then().extract().body().asString())
                    .as("MockServer returns correct result")
                    .isEqualTo(expectedBody);
            }
        }
    }

    @Test
    void shouldCallMockserverUsingTlsProtocol() {
        try (MockServerContainer mockServer = new MockServerContainer(MOCKSERVER_IMAGE)) {
            mockServer.start();

            String expectedBody = "Hello World!";

            try (
                MockServerClient client = new MockServerClient(mockServer.getHost(), mockServer.getServerPort())
                    .withSecure(true)
            ) {
                assertThat(client.hasStarted()).as("Mockserver running").isTrue();

                client.when(request().withPath("/hello")).respond(response().withBody(expectedBody));

                assertThat(secureResponseFromMockserver(mockServer))
                    .as("MockServer returns correct result")
                    .isEqualTo(expectedBody);
            }
        }
    }

    @Test
    void shouldCallMockserverUsingMutualTlsProtocol() {
        try (
            MockServerContainer mockServer = new MockServerContainer(MOCKSERVER_IMAGE)
                .withEnv("MOCKSERVER_TLS_MUTUAL_AUTHENTICATION_REQUIRED", "true")
        ) {
            mockServer.start();

            String expectedBody = "Hello World!";

            try (
                MockServerClient client = new MockServerClient(mockServer.getHost(), mockServer.getServerPort())
                    .withSecure(true)
            ) {
                assertThat(client.hasStarted()).as("Mockserver running").isTrue();

                client.when(request().withPath("/hello")).respond(response().withBody(expectedBody));

                assertThat(secureResponseFromMockserver(mockServer))
                    .as("MockServer returns correct result")
                    .isEqualTo(expectedBody);
            }
        }
    }

    @Test
    void newVersionStartsWithDefaultWaitStrategy() {
        try (MockServerContainer mockServer = new MockServerContainer(MOCKSERVER_IMAGE)) {
            mockServer.start();
        }
    }

    private static String secureResponseFromMockserver(MockServerContainer mockServer) {
        return given()
            .config(
                RestAssuredConfig
                    .config()
                    .sslConfig(
                        SSLConfig
                            .sslConfig()
                            .sslSocketFactory(
                                new SSLSocketFactory(
                                    new KeyStoreFactory(Configuration.configuration(), new MockServerLogger())
                                        .sslContext()
                                )
                            )
                    )
            )
            .baseUri(mockServer.getSecureEndpoint())
            .get("/hello")
            .body()
            .asString();
    }
}
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-mockserver:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-mockserver</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

此外，不要忘记添加[客户端依赖 `org.mock-server:mockserver-client-java`](https://search.maven.org/search?q=mockserver-client-java)，以便能够设置期望，该依赖不由 testcontainers 模块提供。客户端版本应与容器标签中的版本匹配。
