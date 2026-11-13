---
source_url: https://java.testcontainers.org/modules/ldap/
source_hash: sha256:dd640b44dca2775141ae95f6dba24461ac007089bd1b3c40eac722a7b14f6fa9
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# LLDAP

用于 [LLDAP](https://hub.docker.com/r/lldap/lldap) 的 Testcontainers 模块。

## LLdapContainer 使用示例

你可以在任何 Java 应用程序中通过以下方式启动 LLDAP 容器实例：

**LLDAP 容器**

```java
LLdapContainer lldap = new LLdapContainer("lldap/lldap:v0.6.1-alpine")
```

## 将此模块添加到项目依赖中

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-ldap:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-ldap</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```
