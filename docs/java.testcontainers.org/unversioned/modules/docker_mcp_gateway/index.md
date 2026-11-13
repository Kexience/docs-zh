---
source_url: https://java.testcontainers.org/modules/docker_mcp_gateway/
source_hash: sha256:8017fcf56e453fd1c914e536c4a8336bcdd52122be67a53c1f152f84e21fc42b
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Docker MCP Gateway

[Docker MCP Gateway](https://hub.docker.com/r/docker/mcp-gateway) 的 Testcontainers 模块。

## DockerMcpGatewayContainer 使用示例

你可以在任意 Java 应用中使用以下方式启动 Docker MCP Gateway 容器实例：

**创建 DockerMcpGatewayContainer**

```java
DockerMcpGatewayContainer gateway = new DockerMcpGatewayContainer("docker/mcp-gateway:latest")
    .withServer("curl", "curl")
    .withServer("brave", "brave_local_search", "brave_web_search")
    .withServer("github-official", Collections.singletonList("add_issue_comment"))
    .withSecret("brave.api_key", "test_key")
    .withSecrets(Collections.singletonMap("github.personal_access_token", "test_token"))
```

## 将此模块添加到项目依赖

*Docker MCP Gateway 支持是核心 Testcontainers 库的一部分。*

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
