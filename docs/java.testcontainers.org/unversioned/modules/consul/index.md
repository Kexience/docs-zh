---
source_url: https://java.testcontainers.org/modules/consul/
source_hash: sha256:9382433bca28d1416387843c444790e31fd8e2a739904e4d39f8da4ac298139d
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Consul

[Consul](https://github.com/hashicorp/consul) 的 Testcontainers 模块。Consul 是一个用于管理键值属性的工具。更多关于 Consul 的信息请参见[此处](https://www.consul.io/)。

## 使用示例

**在 Junit 测试中运行 Consul**

```java
package org.testcontainers.consul;

import com.ecwid.consul.v1.ConsulClient;
import com.ecwid.consul.v1.Response;
import com.ecwid.consul.v1.kv.model.GetValue;
import io.restassured.RestAssured;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.testcontainers.containers.GenericContainer;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

class ConsulContainerTest {

    private static ConsulContainer consul = new ConsulContainer("hashicorp/consul:1.15")
        .withConsulCommand("kv put config/testing1 value123");

    @BeforeAll
    static void setup() {
        consul.start();
    }

    @AfterAll
    static void teardown() {
        consul.stop();
    }

    @Test
    void readFirstPropertyPathWithCli() throws IOException, InterruptedException {
        GenericContainer.ExecResult result = consul.execInContainer("consul", "kv", "get", "config/testing1");
        final String output = result.getStdout().replaceAll("\\r?\\n", "");
        assertThat(output).contains("value123");
    }

    @Test
    void readFirstSecretPathOverHttpApi() {
        io.restassured.response.Response response = RestAssured
            .given()
            .when()
            .get("http://" + getHostAndPort() + "/v1/kv/config/testing1")
            .andReturn();

        assertThat(response.body().jsonPath().getString("[0].Value"))
            .isEqualTo(Base64.getEncoder().encodeToString("value123".getBytes(StandardCharsets.UTF_8)));
    }

    @Test
    void writeAndReadMultipleValuesUsingClient() {
        final ConsulClient consulClient = new ConsulClient(consul.getHost(), consul.getFirstMappedPort());

        final Map<String, String> properties = new HashMap<>();
        properties.put("value", "world");
        properties.put("other_value", "another world");

        // Write operation
        properties.forEach((key, value) -> {
            Response<Boolean> writeResponse = consulClient.setKVValue(key, value);
            assertThat(writeResponse.getValue()).isTrue();
        });

        // Read operation
        properties.forEach((key, value) -> {
            Response<GetValue> readResponse = consulClient.getKVValue(key);
            assertThat(readResponse.getValue().getDecodedValue()).isEqualTo(value);
        });
    }

    private String getHostAndPort() {
        return consul.getHost() + ":" + consul.getMappedPort(8500);
    }
}
```

## 为什么在 Junit 测试中使用 Consul？

随着 Consul 和配置外部化的日益普及，应用程序现在需要从 Consul 获取属性。在开发阶段，如果手边没有正在运行的 Consul 实例，这可能会带来挑战。该库旨在解决你的应用与 Consul 的集成测试问题。你还可以通过在 Junit 中编写不同的测试场景，来测试你的应用在 Consul 环境下的行为。

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-consul:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-consul</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
