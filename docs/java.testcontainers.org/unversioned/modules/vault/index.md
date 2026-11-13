---
source_url: https://java.testcontainers.org/modules/vault/
source_hash: sha256:f4d4b2afb2d8d953dcdaded8b60513483e68b528f82c8a8fd4194ff24ca5b724
translated_at: 2026-11-13T12:18:06+08:00
translation_version: 1
---

# Vault 模块

用于 [Vault](https://github.com/hashicorp/vault) 的 Testcontainers 模块。Vault 是一个用于管理密钥的工具。有关 Vault 的更多信息，请参见[这里](https://www.vaultproject.io/)。

## 使用示例

你可以在任何 Java 应用程序中使用以下方式启动 Vault 容器实例：

**启动 Vault 容器**

```java
public static VaultContainer<?> vaultContainer = new VaultContainer<>("hashicorp/vault:1.13")
    .withVaultToken(VAULT_TOKEN)
    .withInitCommand(
        "secrets enable transit",
        "write -f transit/keys/my-key",
        "kv put secret/testing1 top_secret=password123",
        "kv put secret/testing2 secret_one=password1 secret_two=password2 secret_three=password3 secret_three=password3 secret_four=password4"
    );
```

使用 CLI 从 Vault 容器读取数据：

**使用 CLI 读取数据**

```java
GenericContainer.ExecResult result = vaultContainer.execInContainer(
    "vault",
    "kv",
    "get",
    "-format=json",
    "secret/testing1"
);
assertThat(result.getStdout()).contains("password123");
```

使用 HTTP API 从 Vault 容器读取数据：

**使用 HTTP API 读取数据**

```java
Response response = given()
    .header("X-Vault-Token", VAULT_TOKEN)
    .when()
    .get(vaultContainer.getHttpHostAddress() + "/v1/secret/data/testing1")
    .thenReturn();
assertThat(response.body().jsonPath().getString("data.data.top_secret")).isEqualTo("password123");
```

## 将此模块添加到项目依赖

将以下依赖添加到你的 `pom.xml`/`build.gradle` 文件中：

**Gradle**

```groovy
testImplementation "org.testcontainers:testcontainers-vault:2.0.5"
```

**Maven**

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>testcontainers-vault</artifactId>
    <version>2.0.5</version>
    <scope>test</scope>
</dependency>
```

## 许可证

参见 [LICENSE](https://raw.githubusercontent.com/testcontainers/testcontainers-java/main/modules/vault/LICENSE)。

## 版权

Copyright (c) 2017 Capital One Services, LLC and other authors.

贡献者请参见 [AUTHORS](https://raw.githubusercontent.com/testcontainers/testcontainers-java/main/modules/vault/AUTHORS)。
