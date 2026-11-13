---
source_url: https://java.testcontainers.org/modules/grafana/
source_hash: sha256:b82882eb024f044383d7bcf93d2f8a507f65033d4fc4a12c334dd0fe49d1834e
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Grafana OTel LGTM

[Grafana OTel LGTM](https://hub.docker.com/r/grafana/otel-lgtm) 的 Testcontainers 模块。

## LGTM 使用示例

你可以在任意 Java 应用中使用以下方式启动 Grafana OTel LGTM 容器实例：

**Grafana Otel LGTM 容器**

```java
LgtmStackContainer lgtm = new LgtmStackContainer("grafana/otel-lgtm:0.11.1")
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-grafana:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-grafana</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
